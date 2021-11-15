import json
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional

__all__ = ["ContractInfo", "ContractDirectory", "tellor_directory"]


# Read contract ABIs from json files
_abi_folder = Path(__file__).resolve().parent / "_tellorx"
_abi_dict = {}
for name in ["master", "controller", "oracle", "governance", "treasury"]:
    with open(_abi_folder / f"{name}_abi.json", "r") as f:
        _abi_dict[name] = json.load(f)

_tellor_address_mainnet = {
    "master": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
    "controller": "",
    "oracle": "",
    "governance": "",
    "treasury": "",
}

_tellor_address_rinkeby = {
    "master": "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
    "controller": "0x0f2B0a8fa0f60459f51E452273C879eb32555e91",
    "oracle": "0x18431fd88adF138e8b979A7246eb58EA7126ea16",
    "governance": "0xA64Bb0078eB80c97484f3f09Adb47b9B73CBcA00",
    "treasury": "0x2dB91443f2b562B8b2B2e8E4fC0A3EDD6c195147",
}


@dataclass
class ContractInfo:
    org: str
    name: str
    chain_id: int
    address: str
    abi: Optional[List[Any]] = field(repr=False)


@dataclass
class ContractDirectory:
    # Private directory storage
    _contents: List[ContractInfo] = field(default_factory=list)

    def add_contract(self, info: ContractInfo) -> None:
        self._contents.append(info)

    def find(
        self,
        *,
        org: str = "tellor",
        name: Optional[str] = None,
        address: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> List[ContractInfo]:
        result = []
        for info in self._contents:
            if info.org != org:
                continue
            if chain_id is not None:
                if chain_id != info.chain_id:
                    continue
            if name is not None:
                if info.name is not name:
                    continue
            if address is not None:
                if info.address is not address:
                    continue

            result.append(info)

        return result


# Create default tellor directory
tellor_directory = ContractDirectory()

for name in ["master", "controller", "oracle", "governance", "treasury"]:
    # Add maininet contract info entry
    tellor_directory.add_contract(
        ContractInfo(
            chain_id=1,
            org="tellor",
            name=name,
            address=_tellor_address_mainnet[name],
            abi=_abi_dict[name],
        )
    )

    # Add rinkeby contract info entry
    tellor_directory.add_contract(
        ContractInfo(
            chain_id=4,
            org="tellor",
            name=name,
            address=_tellor_address_rinkeby[name],
            abi=_abi_dict[name],
        )
    )
