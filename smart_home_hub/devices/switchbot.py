import hashlib
import hmac
import base64
import json
import time
import urllib.request
import uuid
from typing import Any

from .base import Device

API_BASE = "https://api.switch-bot.com/v1.1"


class SwitchBotBot(Device):
    """SwitchBot Bot (press mode) controlled via SwitchBot Cloud API v1.1."""

    def __init__(self, name: str, token: str, secret: str, device_id: str, **kwargs: Any):
        super().__init__(name)
        self._token = token
        self._secret = secret
        self._device_id = device_id

    def _make_headers(self) -> dict[str, str]:
        t = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4())
        sign = base64.b64encode(
            hmac.new(
                self._secret.encode(),
                (self._token + t + nonce).encode(),
                hashlib.sha256,
            ).digest()
        ).decode()
        return {
            "Authorization": self._token,
            "sign": sign,
            "t": t,
            "nonce": nonce,
            "Content-Type": "application/json",
        }

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{API_BASE}{path}"
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, method=method, headers=self._make_headers())
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        if result.get("statusCode") != 100:
            raise RuntimeError(f"SwitchBot API error: {result.get('message', 'unknown error')}")
        return result

    def on(self) -> None:
        self._request("POST", f"/devices/{self._device_id}/commands", {
            "command": "press",
            "commandType": "command",
            "parameter": "default",
        })
        print(f"[{self.name}] pressed")

    def off(self) -> None:
        pass

    def status(self) -> dict[str, Any]:
        result = self._request("GET", f"/devices/{self._device_id}/status")
        body = result.get("body", {})
        return {
            "name": self.name,
            "power": body.get("power"),
            "battery": body.get("battery"),
        }
