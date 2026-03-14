import argparse
import os
import re
import sys
from pathlib import Path

import yaml

from .devices.probreeze import ProBreeze
from .devices.switchbot import SwitchBotBot
from .devices.tapo import TapoP100

DEVICE_TYPES = {
    "tapo": TapoP100,
    "probreeze": ProBreeze,
    "switchbot": SwitchBotBot,
}


def _resolve_env_vars(obj):
    """Recursively replace ${VAR} references with environment variable values."""
    if isinstance(obj, str):
        return re.sub(
            r"\$\{(\w+)\}",
            lambda m: os.environ.get(m.group(1), m.group(0)),
            obj,
        )
    if isinstance(obj, dict):
        return {k: _resolve_env_vars(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve_env_vars(item) for item in obj]
    return obj


def load_config(path: Path) -> dict:
    with open(path) as f:
        return _resolve_env_vars(yaml.safe_load(f))


def get_device(config: dict, device_name: str):
    for dev_cfg in config["devices"]:
        if dev_cfg["name"] == device_name or dev_cfg["type"] == device_name:
            dtype = dev_cfg["type"]
            cls = DEVICE_TYPES[dtype]
            kwargs = {k: v for k, v in dev_cfg.items() if k != "type"}
            return cls(**kwargs)
    print(f"Device '{device_name}' not found in config.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="smart_home_hub", description="Smart Home Hub CLI")
    parser.add_argument("device", help="Device name or type (e.g. tapo, probreeze)")
    parser.add_argument("action", choices=["on", "off", "status", "set_humidity"], help="Action to perform")
    parser.add_argument("--value", type=int, help="Value for set commands (e.g. target humidity)")
    parser.add_argument("-c", "--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    device = get_device(config, args.device)

    if args.action == "set_humidity":
        if args.value is None:
            print("--value is required for set_humidity (e.g. --value 55)")
            sys.exit(1)
        device.set_humidity(args.value)
    elif args.action == "status":
        result = device.status()
        for k, v in result.items():
            print(f"  {k}: {v}")
    else:
        getattr(device, args.action)()


if __name__ == "__main__":
    main()
