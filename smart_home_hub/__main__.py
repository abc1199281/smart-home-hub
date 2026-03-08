import argparse
import sys
from pathlib import Path

import yaml

from .devices.tapo import TapoP100

DEVICE_TYPES = {
    "tapo": TapoP100,
}


def load_config(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_device(config: dict, device_name: str):
    for dev_cfg in config["devices"]:
        if dev_cfg["name"] == device_name or dev_cfg["type"] == device_name:
            dtype = dev_cfg.pop("type")
            cls = DEVICE_TYPES[dtype]
            return cls(**dev_cfg)
    print(f"Device '{device_name}' not found in config.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="smart_home_hub", description="Smart Home Hub CLI")
    parser.add_argument("device", help="Device name or type (e.g. tapo, living_room_plug)")
    parser.add_argument("action", choices=["on", "off", "status"], help="Action to perform")
    parser.add_argument("-c", "--config", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    device = get_device(config, args.device)

    result = getattr(device, args.action)()
    if args.action == "status" and result:
        for k, v in result.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
