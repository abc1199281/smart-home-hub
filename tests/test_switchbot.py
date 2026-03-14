import hashlib
import hmac
import base64
import json
from unittest.mock import patch, MagicMock

import pytest

from smart_home_hub.devices.switchbot import SwitchBotBot


def _make_device():
    return SwitchBotBot(
        name="test_bot",
        token="test_token",
        secret="test_secret",
        device_id="AABBCCDDEEFF",
    )


def _mock_response(status_code=100, body=None, message=None):
    payload = {"statusCode": status_code, "body": body or {}}
    if message is not None:
        payload["message"] = message
    resp = MagicMock()
    resp.read.return_value = json.dumps(payload).encode()
    resp.__enter__ = MagicMock(return_value=resp)
    resp.__exit__ = MagicMock(return_value=False)
    return resp


class TestMakeHeaders:
    def test_headers_contain_required_fields(self):
        device = _make_device()
        headers = device._make_headers()

        assert headers["Authorization"] == "test_token"
        assert "sign" in headers
        assert "t" in headers
        assert "nonce" in headers
        assert headers["Content-Type"] == "application/json"

    def test_signature_is_valid_hmac(self):
        device = _make_device()
        headers = device._make_headers()

        string_to_sign = "test_token" + headers["t"] + headers["nonce"]
        expected = base64.b64encode(
            hmac.new(b"test_secret", string_to_sign.encode(), hashlib.sha256).digest()
        ).decode()
        assert headers["sign"] == expected


class TestOn:
    @patch("smart_home_hub.devices.switchbot.urllib.request.urlopen")
    def test_on_sends_press_command(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response()
        device = _make_device()
        device.on()

        req = mock_urlopen.call_args[0][0]
        assert "/devices/AABBCCDDEEFF/commands" in req.full_url
        body = json.loads(req.data)
        assert body["command"] == "press"
        assert body["commandType"] == "command"


class TestOff:
    @patch("smart_home_hub.devices.switchbot.urllib.request.urlopen")
    def test_off_is_noop(self, mock_urlopen):
        device = _make_device()
        device.off()

        mock_urlopen.assert_not_called()


class TestStatus:
    @patch("smart_home_hub.devices.switchbot.urllib.request.urlopen")
    def test_status_returns_device_info(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(body={
            "power": "on",
            "battery": 85,
        })
        device = _make_device()
        status = device.status()

        assert status["name"] == "test_bot"
        assert status["power"] == "on"
        assert status["battery"] == 85


class TestErrorHandling:
    @patch("smart_home_hub.devices.switchbot.urllib.request.urlopen")
    def test_non_100_raises_runtime_error(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(
            status_code=151, message="token is invalid"
        )
        device = _make_device()

        with pytest.raises(RuntimeError, match="token is invalid"):
            device.on()

    @patch("smart_home_hub.devices.switchbot.urllib.request.urlopen")
    def test_unknown_error_message(self, mock_urlopen):
        mock_urlopen.return_value = _mock_response(status_code=999)
        device = _make_device()

        with pytest.raises(RuntimeError, match="unknown error"):
            device.status()
