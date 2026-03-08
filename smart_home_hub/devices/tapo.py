import asyncio
from typing import Any

from tapo import ApiClient

from .base import Device


def _run(coro):
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


class TapoP100(Device):
    """TP-Link Tapo P100 smart plug (LAN control via tapo library)."""

    def __init__(self, name: str, host: str, email: str, password: str, **kwargs: Any):
        super().__init__(name, host)
        self._email = email
        self._password = password
        self._device = _run(self._connect())

    async def _connect(self):
        client = ApiClient(self._email, self._password)
        return await client.p100(self.host)

    def on(self) -> None:
        _run(self._device.on())
        print(f"[{self.name}] turned ON")

    def off(self) -> None:
        _run(self._device.off())
        print(f"[{self.name}] turned OFF")

    def status(self) -> dict[str, Any]:
        info = _run(self._device.get_device_info())
        return {
            "name": self.name,
            "host": self.host,
            "device_on": info.device_on,
            "model": info.model,
            "firmware": info.fw_ver,
        }
