import argparse
import sys
from pathlib import Path

import yaml

from .devices.probreeze import ProBreeze
from .devices.tapo import TapoP100

DEVICE_TYPES = {
    "tapo": TapoP100,
    "probreeze": ProBreeze,
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
