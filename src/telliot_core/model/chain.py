from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

from telliot_core.apps.config import ConfigOptions
from telliot_core.model.base import Base


@dataclass
class EVMCurrency(Base):
    name: str
    symbol: str
    decimals: int


@dataclass
class Chain(Base):
    name: str
    chain: str
    network: str
    chain_id: int
    currency: EVMCurrency


default_chain_list = [
    Chain(
        chain_id=1,
        name="Ethereum Mainnet",
        chain="ETH",
        network="mainnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=3,
        name="Ethereum Testnet Ropsten",
        chain="ETH",
        network="ropsten",
        currency=EVMCurrency(name="Ropsten Ether", symbol="ROP", decimals=18),
    ),
    Chain(
        chain_id=4,
        name="Ethereum Testnet Rinkeby",
        chain="ETH",
        network="rinkeby",
        currency=EVMCurrency(name="Rinkeby Ether", symbol="RIN", decimals=18),
    ),
    Chain(
        chain_id=137,
        name="Matic(Polygon) Mainnet",
        chain="Matic(Polygon)",
        network="mainnet",
        currency=EVMCurrency(name="Matic", symbol="MATIC", decimals=18),
    ),
    Chain(
        chain_id=80001,
        name="Matic(Polygon) Testnet Mumbai",
        chain="Matic(Polygon)",
        network="testnet",
        currency=EVMCurrency(name="Matic", symbol="tMATIC", decimals=18),
    ),
]


@dataclass
class ChainList(ConfigOptions):
    chains: List[Chain] = field(default_factory=lambda: default_chain_list)

    def get_chain(
        self, chain: str = "ETH", network: str = "rinkeby"
    ) -> Optional[Chain]:
        """Get chain"""

        for ch in self.chains:
            if chain.lower() in ch.chain.lower():
                if network.lower() in ch.network.lower():
                    return ch

        return None
