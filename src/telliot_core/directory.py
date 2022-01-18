import json
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Union

from clamfig import Serializable

from telliot_core.apps.config import ConfigFile
from telliot_core.apps.config import ConfigOptions
from telliot_core.utils.home import telliot_homedir

# Read contract ABIs from json files

_abi_folder = Path(__file__).resolve().parent / "data" / "abi"


@dataclass
class ContractInfo(Serializable):
    name: str
    org: str
    address: dict[int, str]
    abi_file: Optional[str]

    _abi: Optional[list[Any]] = field(default=None, init=False, repr=False)

    @property
    def abi(self) -> list[Any]:
        """Returns the contract ABI.

        The ABI is lazily loaded from a file the first time it is requested
        and stored for later access.
        """
        if self._abi is not None:
            return self._abi
        else:
            if self.abi_file:
                with open(_abi_folder / self.abi_file, "r") as f:
                    return json.load(f)  # type: ignore
            else:
                raise ValueError("ABI File not defined")

    def restore_state(self, state: dict[Any, Any]) -> None:
        """Workaround JSON dict key type issue.  This should be handled by clamfig in future."""
        strkeys = list(state["address"].keys())
        for chain_id in strkeys:
            state["address"][int(chain_id)] = state["address"].pop(chain_id)

        super().restore_state(state)


def default_contracts() -> list[ContractInfo]:
    contracts = [
        ContractInfo(
            org="tellor",
            name="tellorx-master",
            address={
                1: "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
                4: "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            },
            abi_file="tellorx-master-abi.json",
        ),
        ContractInfo(
            org="tellor",
            name="tellorx-controller",
            address={
                1: "0xf98624E9924CAA2cbD21cC6288215Ec2ef7cFE80",
                4: "0x0f2b0a8fa0f60459f51e452273c879eb32555e91",
            },
            abi_file=None,
        ),
        ContractInfo(
            org="tellor",
            name="tellorx-oracle",
            address={
                1: "0xe8218cACb0a5421BC6409e498d9f8CC8869945ea",
                4: "0x18431fd88adF138e8b979A7246eb58EA7126ea16",
            },
            abi_file="tellorx-oracle-abi.json",
        ),
        ContractInfo(
            org="tellor",
            name="tellorx-governance",
            address={
                1: "0x51d4088d4EeE00Ae4c55f46E0673e9997121DB00",
                4: "0xA64Bb0078eB80c97484f3f09Adb47b9B73CBcA00",
            },
            abi_file="tellorx-governance-abi.json",
        ),
        ContractInfo(
            org="tellor",
            name="tellorx-treasury",
            address={
                1: "0x3b0f3eaEFaAc9f8F7FDe406919ecEb5270fE0607",
                4: "0x2dB91443f2b562B8b2B2e8E4fC0A3EDD6c195147",
            },
            abi_file="tellorx-treasury-abi.json",
        ),
        ContractInfo(
            org="tellor",
            name="tellorflex-oracle",
            address={1: "", 4: "0xFd45Ae72E81Adaaf01cC61c8bCe016b7060DD537"},
            abi_file="tellorflex-oracle-abi.json",
        ),
    ]

    return contracts


@dataclass
class ContractDirectory(ConfigOptions):
    """Contract directory object"""

    entries: list[ContractInfo] = field(default_factory=default_contracts)

    def add_contract(self, info: ContractInfo) -> None:
        self.entries.append(info)

    def find(
        self,
        *,
        org: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> list[ContractInfo]:
        result = []
        for info in self.entries:
            if org is not None:
                if org != info.org:
                    continue
            if chain_id is not None:
                if chain_id not in info.address.keys():
                    continue
            if name is not None:
                if name not in info.name:
                    continue
            if address is not None:
                if address not in info.address.values():
                    continue

            result.append(info)

        return result


def directory_config_file(config_dir: Optional[Union[str, Path]] = None) -> ConfigFile:
    if not config_dir:
        config_dir = telliot_homedir()

    cf = ConfigFile(
        name="directory",
        config_type=ContractDirectory,
        config_format="json",
        config_dir=config_dir,
    )

    return cf
