import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from smart_home_hub.devices.tapo import TapoP100


def _make_mock_device():
    mock_device = AsyncMock()
    mock_client_cls = MagicMock()
    mock_client = mock_client_cls.return_value
    mock_client.p100 = AsyncMock(return_value=mock_device)
    return mock_client_cls, mock_device


@patch("smart_home_hub.devices.tapo.ApiClient")
def test_tapo_on(mock_api_cls):
    mock_device = AsyncMock()
    mock_api_cls.return_value.p100 = AsyncMock(return_value=mock_device)

    device = TapoP100(name="test_plug", host="192.168.1.100", email="a@b.com", password="pw")
    device.on()

    mock_device.on.assert_called_once()


@patch("smart_home_hub.devices.tapo.ApiClient")
def test_tapo_off(mock_api_cls):
    mock_device = AsyncMock()
    mock_api_cls.return_value.p100 = AsyncMock(return_value=mock_device)

    device = TapoP100(name="test_plug", host="192.168.1.100", email="a@b.com", password="pw")
    device.off()

    mock_device.off.assert_called_once()


@patch("smart_home_hub.devices.tapo.ApiClient")
def test_tapo_status(mock_api_cls):
    mock_device = AsyncMock()
    mock_info = MagicMock()
    mock_info.device_on = True
    mock_info.model = "P100"
    mock_info.fw_ver = "1.2.3"
    mock_device.get_device_info = AsyncMock(return_value=mock_info)
    mock_api_cls.return_value.p100 = AsyncMock(return_value=mock_device)

    device = TapoP100(name="test_plug", host="192.168.1.100", email="a@b.com", password="pw")
    status = device.status()

    assert status["device_on"] is True
    assert status["model"] == "P100"
