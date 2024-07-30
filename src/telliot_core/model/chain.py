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
        chain_id=69,
        name="Optimism Kovan",
        chain="Optimism",
        network="testnet (public)",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=1666600000,
        name="Harmony Mainnet",
        chain="Harmony",
        network="mainnet",
        currency=EVMCurrency(name="Harmony ONE", symbol="ONE", decimals=18),
    ),
    Chain(
        chain_id=1666700000,
        name="Harmony Testnet",
        chain="Harmony",
        network="testnet",
        currency=EVMCurrency(name="Harmony ONE", symbol="ONE", decimals=18),
    ),
    Chain(
        chain_id=421611,
        name="Arbitrum Rinkeby",
        chain="Arbitrum",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=42161,
        name="Arbitrum One",
        chain="Arbitrum",
        network="mainnet",
        currency=EVMCurrency(name="Arbitrum Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=421613,
        name="Arbitrum Goerli",
        chain="Arbitrum-goerli",
        network="testnet-goerli",
        currency=EVMCurrency(name="Arbitrum Goerli Ether", symbol="AGOR", decimals=18),
    ),
    Chain(
        chain_id=10200,
        name="Chiado Testnet",
        chain="Chiado",
        network="testnet",
        currency=EVMCurrency(name="Chiado xDai", symbol="XDAI", decimals=18),
    ),
    Chain(
        chain_id=100,
        name="gnosis",
        chain="gnosis",
        network="mainnet",
        currency=EVMCurrency(name="xDai", symbol="XDAI", decimals=18),
    ),
    Chain(
        chain_id=10,
        name="optimism",
        chain="optimism",
        network="mainnet",
        currency=EVMCurrency(name="Optimism Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=420,
        name="optimism-goerli",
        chain="optimism-goerli",
        network="testnet-goerli",
        currency=EVMCurrency(name="Optimism Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=3141,
        name="filecoin-hyperspace",
        chain="filecoin-hyperspace",
        network="testnet",
        currency=EVMCurrency(name="Testnet Filecoin", symbol="FIL", decimals=18),
    ),
    Chain(
        chain_id=314159,
        name="filecoin-calibration",
        chain="filecoin-calibration",
        network="testnet",
        currency=EVMCurrency(name="Testnet Filecoin", symbol="FIL", decimals=18),
    ),
    Chain(
        chain_id=314,
        name="filecoin",
        chain="filecoin",
        network="mainnet",
        currency=EVMCurrency(name="Filecoin", symbol="FIL", decimals=18),
    ),
    Chain(
        chain_id=11155111,
        name="Ethereum Testnet Sepolia",
        chain="sepolia",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=369,
        name="pulsechain",
        chain="pulsechain",
        network="mainnet",
        currency=EVMCurrency(name="PulseChain PLS", symbol="PLS", decimals=18),
    ),
    Chain(
        chain_id=943,
        name="pulsechain-testnet",
        chain="pulsechain-testnet",
        network="testnet",
        currency=EVMCurrency(name="PulseChain tPLS", symbol="tPLS", decimals=18),
    ),
    Chain(
        chain_id=3441005,
        name="manta-testnet",
        chain="manta-testnet",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=84531,
        name="base-goerli",
        chain="base-goerli",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=5001,
        name="mantle-testnet",
        chain="mantle-testnet",
        network="testnet",
        currency=EVMCurrency(name="Mantle", symbol="MNT", decimals=18),
    ),
    Chain(
        chain_id=5000,
        name="mantle",
        chain="mantle",
        network="mainnet",
        currency=EVMCurrency(name="Mantle", symbol="MNT", decimals=18),
    ),
    Chain(
        chain_id=2442,
        name="Polygon zkEVM Cardona Testnet",
        chain="cardona",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=1101,
        name="Polygon zkEVM",
        chain="zkEVM",
        network="mainnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=59140,
        name="Linea Goerli",
        chain="Linea Goerli",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=59144,
        name="Linea",
        chain="Linea",
        network="mainnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=2522,
        name="Fraxtal Testnet",
        chain="Fraxtal Testnet",
        network="testnet",
        currency=EVMCurrency(name="Frax Ether", symbol="frxETH", decimals=18),
    ),
    Chain(
        chain_id=252,
        name="Fraxtal Mainnet",
        chain="Fraxtal Mainnet",
        network="mainnet",
        currency=EVMCurrency(name="Frax Ether", symbol="frxETH", decimals=18),
    ),
    Chain(
        chain_id=1998,
        name="Kyoto Testnet",
        chain="Kyoto Testnet",
        network="testnet",
        currency=EVMCurrency(name="KYOTO", symbol="KYOTO", decimals=18),
    ),
    Chain(
        chain_id=1444673419,
        name="Skale Europa Testnet",
        chain="Skale Europa Testnet",
        network="testnet",
        currency=EVMCurrency(name="Skale Fuel", symbol="sFUEL", decimals=18),
    ),
    Chain(
        chain_id=2046399126,
        name="Skale Europa Mainnet",
        chain="Skale Europa Mainnet",
        network="mainnet",
        currency=EVMCurrency(name="Skale Fuel", symbol="sFUEL", decimals=18),
    ),
    Chain(
        chain_id=59141,
        name="Linea Sepolia",
        chain="Linea Sepolia",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=324,
        name="zkSync Era Mainnet",
        chain="zkSync Era Mainnet",
        network="network",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=300,
        name="zkSync Era Sepolia Testnet",
        chain="zkSync Era Sepolia Testnet",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=80002,
        name="Polygon Amoy Testnet",
        chain="polygon-amoy",
        network="testnet",
        currency=EVMCurrency(name="Matic", symbol="MATIC", decimals=18),
    ),
    Chain(
        chain_id=11155420,
        name="Optimism Sepolia Testnet",
        chain="optimism-sepolia",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=421614,
        name="Arbitrum Sepolia Testnet",
        chain="arbitrum-sepolia",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=5003,
        name="Mantle Sepolia Testnet",
        chain="mantle-sepolia",
        network="testnet",
        currency=EVMCurrency(name="Mantle", symbol="MNT", decimals=18),
    ),
    Chain(
        chain_id=84532,
        name="Base Sepolia Testnet",
        chain="base-sepolia",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=111,
        name="puff-bob-jznbxtoq7h",
        chain="BOB",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=60808,
        name="BOB",
        chain="BOB",
        network="mainnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=919,
        name="mode-sepolia-vtnhnpim72",
        chain="mode",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=1918988905,
        name="Rari Testnet",
        chain="rari",
        network="testnet",
        currency=EVMCurrency(name="Ether", symbol="ETH", decimals=18),
    ),
    Chain(
        chain_id=41,
        name="Telos EVM Testnet",
        chain="telos",
        network="testnet",
        currency=EVMCurrency(name="Telos", symbol="TLOS", decimals=18),
    ),
    Chain(
        chain_id=2340,
        name="Atleta Testnet",
        chain="atleta",
        network="testnet",
        currency=EVMCurrency(name="Atleta", symbol="ATLA", decimals=18),
    ),
    Chain(
        chain_id=842,
        name="Taraxa Testnet",
        chain="taraxa",
        network="testnet",
        currency=EVMCurrency(name="Taraxa", symbol="TARA", decimals=18),
    ),
]


@dataclass
class ChainList(ConfigOptions):
    """returns chain information for the
    chain set in the telliot account

    Returns:
        currency, status...
    """

    chains: List[Chain] = field(default_factory=lambda: default_chain_list)

    def get_chain(self, chain: str = "ETH", network: str = "rinkeby") -> Optional[Chain]:
        """Get chain"""

        for ch in self.chains:
            if chain.lower() in ch.chain.lower():
                if network.lower() in ch.network.lower():
                    return ch

        return None
