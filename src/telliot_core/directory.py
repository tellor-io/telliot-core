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
                elif chain_id == 5:
                    url = "https://api-goerli.etherscan.io"
                elif chain_id == 42:
                    url = "https://api-kovan.etherscan.io"
                elif chain_id == 137:
                    url = "https://api.polygonscan.com"
                elif chain_id == 420:
                    url = "https://goerli-optimism.etherscan.io/"
                elif chain_id == 80001:
                    url = "https://api-testnet.polygonscan.com"
                elif chain_id == 42161:
                    url = "https://api.arbiscan.io/"
                elif chain_id == 421613:
                    url = "https://goerli.arbiscan.io/"
                elif chain_id == 10200:
                    url = "https://blockscout.chiadochain.net/"
                elif chain_id == 100:
                    url = "https://api.gnosisscan.io"
                elif chain_id == 10:
                    url = "https://optimistic.etherscan.io/"
                elif chain_id == 3141:
                    url = "https://hyperspace.filfox.info/en"
                elif chain_id == 314159:
                    url = "https://calibration.filfox.info/en"
                elif chain_id == 314:
                    url = "https://filfox.info/en"
                elif chain_id == 11155111:
                    url = "https://api-sepolia.etherscan.io"
                elif chain_id == 3441005:
                    url = "https://manta-testnet.calderaexplorer.xyz"
                elif chain_id == 84531:
                    url = "https://api-goerli.basescan.org/"
                elif chain_id == 5001:
                    url = "https://explorer.testnet.mantle.xyz/"
                elif chain_id == 5000:
                    url = "https://explorer.mantle.xyz/"
                elif chain_id == 2442:
                    url = "https://cardona-zkevm.polygonscan.com/"
                elif chain_id == 1101:
                    url = "https://zkevm.polygonscan.com/"
                elif chain_id == 59140:
                    url = "https://goerli.lineascan.build"
                elif chain_id == 59144:
                    url = "https://lineascan.build"
                elif chain_id == 2522:
                    url = "https://api-holesky.fraxscan.com"
                elif chain_id == 252:
                    url = "https://api.fraxscan.com"
                elif chain_id == 1998:
                    url = "https://testnet.kyotoscan.io"
                elif chain_id == 1444673419:
                    url = "https://juicy-low-small-testnet.explorer.testnet.skalenodes.com"
                elif chain_id == 2046399126:
                    url = "https://elated-tan-skat.explorer.mainnet.skalenodes.com"
                elif chain_id == 59141:
                    url = "https://api-sepolia.lineascan.build"
                elif chain_id == 324:
                    url = "https://block-explorer-api.mainnet.zksync.io"
                elif chain_id == 300:
                    url = "https://block-explorer-api.sepolia.zksync.io"
                elif chain_id == 80002:
                    url = "https://api-amoy.polygonscan.com/"
                elif chain_id == 11155420:
                    url = "https://api-sepolia-optimism.etherscan.io/"
                elif chain_id == 421614:
                    url = "https://api-sepolia.arbiscan.io/"
                elif chain_id == 5003:
                    url = "https://explorer.sepolia.mantle.xyz/"
                elif chain_id == 84532:
                    url = "https://api-sepolia.basescan.org/"
                elif chain_id == 111:
                    url = "https://testnet-explorer.gobob.xyz:443"
                elif chain_id == 60808:
                    url = "https://explorer.gobob.xyz:443"
                elif chain_id == 919:
                    url = "https://sepolia.explorer.mode.network:443"
                elif chain_id == 1918988905:
                    url = "https://testnet.rpc.rarichain.org/http"
                elif chain_id == 41:
                    url = "https://testnet.telos.net/evm"
                elif chain_id == 2340:
                    url = "https://testnet-rpc.atleta.network:9944"
                elif chain_id == 842:
                    url = "https://rpc.testnet.taraxa.io"
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
