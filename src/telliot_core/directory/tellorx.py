import json
from pathlib import Path

from telliot_core.directory.base import Directory

# Read contract ABIs from json files
_abi_folder = Path(__file__).resolve().parent / "_tellorx"
_abi_dict = {}
for name in ["master", "controller", "oracle", "governance", "treasury"]:
    with open(_abi_folder / f"{name}_abi.json", "r") as f:
        _abi_dict[name] = json.load(f)

# Main directory for tellorX contracts
TellorDirectory: Directory = {
    1: {
        "master": {
            "address": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "abi": _abi_dict["master"],
        },
        "controller": {"address": "", "abi": _abi_dict["controller"]},
        "oracle": {"address": "", "abi": _abi_dict["oracle"]},
        "governance": {"address": "", "abi": _abi_dict["governance"]},
        "treasury": {"address": "", "abi": _abi_dict["treasury"]},
    },
    4: {
        "master": {
            "address": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            "abi": _abi_dict["master"],
        },
        "controller": {
            "address": "0x0f2B0a8fa0f60459f51E452273C879eb32555e91",
            "abi": _abi_dict["controller"],
        },
        "oracle": {
            "address": "0x18431fd88adF138e8b979A7246eb58EA7126ea16",
            "abi": _abi_dict["oracle"],
        },
        "governance": {
            "address": "0xA64Bb0078eB80c97484f3f09Adb47b9B73CBcA00",
            "abi": _abi_dict["governance"],
        },
        "treasury": {
            "address": "0x2dB91443f2b562B8b2B2e8E4fC0A3EDD6c195147",
            "abi": _abi_dict["treasury"],
        },
    },
}
