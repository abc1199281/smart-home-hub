from typing import Any

import tinytuya

from .base import Device

# Tuya DPS mapping for ProBreeze PB-D-23W-W dehumidifier
DPS_SWITCH = "1"
DPS_MODE = "2"
DPS_TARGET_HUMIDITY = "4"
DPS_ANION = "5"
DPS_FAN_SPEED = "6"
DPS_CHILD_LOCK = "7"
DPS_FAULT = "11"
DPS_DEFROST = "102"
DPS_CURRENT_TEMP = "103"
DPS_CURRENT_HUMIDITY = "104"
DPS_TANK_FULL = "105"


class ProBreeze(Device):
    """ProBreeze PB-D-23W-W dehumidifier (Tuya protocol via tinytuya, LAN control)."""

    def __init__(
        self,
        name: str,
        host: str,
        device_id: str,
        local_key: str,
        version: float = 3.5,
        **kwargs: Any,
    ):
        super().__init__(name, host)
        self._device = tinytuya.Device(device_id, host, local_key)
        self._device.set_version(version)
        self._device.set_socketPersistent(True)

    def on(self) -> None:
        self._device.set_value(DPS_SWITCH, True)
        print(f"[{self.name}] turned ON")

    def off(self) -> None:
        self._device.set_value(DPS_SWITCH, False)
        print(f"[{self.name}] turned OFF")

    def status(self) -> dict[str, Any]:
        data = self._device.status()
        dps = data.get("dps", {})
        return {
            "name": self.name,
            "host": self.host,
            "running": dps.get(DPS_SWITCH),
            "current_humidity": dps.get(DPS_CURRENT_HUMIDITY),
            "target_humidity": dps.get(DPS_TARGET_HUMIDITY),
            "current_temp": dps.get(DPS_CURRENT_TEMP),
            "mode": dps.get(DPS_MODE),
            "fan_speed": dps.get(DPS_FAN_SPEED),
            "tank_full": dps.get(DPS_TANK_FULL),
        }

    def set_humidity(self, target: int) -> None:
        self._device.set_value(DPS_TARGET_HUMIDITY, target)
        print(f"[{self.name}] target humidity set to {target}%")
