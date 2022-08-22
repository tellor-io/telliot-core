import json
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Optional

import requests
from clamfig import deserialize
from clamfig import Serializable

from telliot_core.apps.config import ConfigOptions
from telliot_core.utils.home import TELLIOT_CORE_ROOT


# Read contract ABIs from json files
_abi_folder = Path(__file__).resolve().parent / "data" / "abi"


@dataclass
class ContractInfo(Serializable):
    name: str
    org: str
    address: dict[int, str]
    abi_file: Optional[str] = None

    _abi: Optional[list[Any]] = field(default=None, init=False, repr=False)

    def get_abi(self, chain_id: int = 0, api_key: str = "") -> list[Any]:
        """Returns the contract ABI.

        The ABI is lazily loaded from a file the first time it is requested
        and stored for later access.  If an abi file is not defined, an attempt
        is made to retrieve the ABI from the chain explorer.
        """
        if not chain_id:
            chain_id = list(self.address.keys())[0]

        if not self._abi:
            if self.abi_file:
                with open(_abi_folder / self.abi_file, "r") as f:
                    self._abi = json.load(f)
            else:
                # try to get from etherscan or other explorer using example:
                address = self.address[chain_id]
                if chain_id == 1:
                    url = "https://api.etherscan.io"
                elif chain_id == 3:
                    url = "https://api-ropsten.etherscan.io"
                elif chain_id == 4:
                    url = "https://api-rinkeby.etherscan.io"
                elif chain_id == 42:
                    url = "https://api-kovan.etherscan.io"
                elif chain_id == 137:
                    url = "https://api.polygonscan.com"
                elif chain_id == 80001:
                    url = "https://api-testnet.polygonscan.com"
                elif chain_id == 42161:
                    url = "https://api.arbiscan.io/"
                else:
                    raise ValueError(f"Could not retrieve ABI using chain_id {chain_id}")

                url = url + f"/api?module=contract&action=getabi&address={address}&format=raw"

                if api_key:
                    url = url + f"&apikey={api_key}"

                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0"}
                response = requests.get(url, headers=headers)
                self._abi = response.json()

        return self._abi  # type: ignore

    def restore_state(self, state: dict[Any, Any]) -> None:
        """Workaround JSON dict key type issue.  This should be handled by clamfig in future."""
        strkeys = list(state["address"].keys())
        for chain_id in strkeys:
            state["address"][int(chain_id)] = state["address"].pop(chain_id)

        super().restore_state(state)


@dataclass
class ContractDirectory(ConfigOptions):
    """Contract directory object"""

    entries: dict[str, ContractInfo] = field(default_factory=dict)

    def add_entry(self, entry: ContractInfo) -> None:
        """Add ContractInfo object to directory."""

        if entry.name in self.entries:
            raise ValueError(f"Contrct {entry.name} already in directory")

        self.entries[entry.name] = entry

    @classmethod
    def from_file(cls, filepath: Path) -> "ContractDirectory":
        """Create a ContractDirectory from file."""

        with open(filepath) as f:
            state = json.load(f)

        entry_list = deserialize(state)

        obj = cls(entries={})

        for entry in entry_list:
            obj.add_entry(entry)

        return obj

    def find(
        self,
        *,
        org: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> list[ContractInfo]:
        """Search the Contract Directory."""

        result = []
        for info in self.entries.values():
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


contract_directory = ContractDirectory.from_file(TELLIOT_CORE_ROOT / "data/contract_directory.json")
