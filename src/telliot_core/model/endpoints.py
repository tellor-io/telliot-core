"""
Utils for creating a JSON RPC connection to an EVM blockchain
"""
import logging
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

import websockets.exceptions
from web3 import Web3
from web3.middleware import geth_poa_middleware

from telliot_core.apps.config import ConfigFile
from telliot_core.apps.config import ConfigOptions
from telliot_core.model.base import Base

logger = logging.getLogger(__name__)


@dataclass
class RPCEndpoint(Base):
    """JSON RPC Endpoint for EVM compatible network"""

    #: Chain ID
    chain_id: Optional[int] = None

    #: Network Name (e.g. 'mainnet', 'testnet', 'sepolia')
    network: str = ""

    #: Provider Name (e.g. 'Infura')
    provider: str = ""

    #: URL (e.g. 'https://mainnet.infura.io/v3/<project_id>')
    url: str = ""

    #: Explorer URL ')
    explorer: Optional[str] = None

    #: Read-only Web3 Connection with private storage
    web3 = property(lambda self: self._web3)
    _web3: Optional[Web3] = field(default=None, init=False, repr=False)

    def connect(self) -> bool:
        """Connect to EVM blockchain

        A connection failure does not raise an exception.  This is left
        to the caller.

        returns:
            True if connection was successful
        """

        if self._web3:
            return True

        if self.url.startswith("ws"):
            self._web3 = Web3(Web3.WebsocketProvider(self.url))
        elif self.url.startswith("http"):
            self._web3 = Web3(Web3.HTTPProvider(self.url))
        else:
            raise ValueError(f"Invalid endpoint url: {self.url}")

        # Inject middleware if connecting to sepolia (chain_id=11155111)
        if self.chain_id == 11155111:
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        connected = False
        try:
            connected = self._web3.eth.get_block_number() > 1
            logger.debug("Connected to {}".format(self))

        except websockets.exceptions.InvalidStatusCode as e:
            connected = False
            msg = f"Could not connect to RPC endpoint at: {self.url}"
            logger.error(e)
            logger.error(msg)

        return connected


default_endpoint_list = [
    RPCEndpoint(
        chain_id=1,
        provider="Infura",
        network="mainnet",
        url="wss://mainnet.infura.io/ws/v3/{INFURA_API_KEY}",
        explorer="https://etherscan.io",
    ),
    RPCEndpoint(
        chain_id=3,
        provider="Infura",
        network="ropsten",
        url="wss://ropsten.infura.io/ws/v3/{INFURA_API_KEY}",
        explorer="https://ropsten.etherscan.io",
    ),
    RPCEndpoint(
        chain_id=4,
        provider="Infura",
        network="rinkeby",
        url="wss://rinkeby.infura.io/ws/v3/{INFURA_API_KEY}",
        explorer="https://rinkeby.etherscan.io",
    ),
    RPCEndpoint(
        chain_id=5,
        provider="Infura",
        network="goerli",
        url="wss://goerli.infura.io/ws/v3/{INFURA_API_KEY}",
        explorer="https://goerli.etherscan.io",
    ),
    RPCEndpoint(
        chain_id=137,
        provider="Matic",
        network="mainnet",
        url="https://rpc-mainnet.matic.network",
        explorer="https://polygonscan.com/",
    ),
    RPCEndpoint(
        chain_id=122,
        provider="Fuse",
        network="mainnet",
        url="https://rpc.fuse.io",
        explorer="https://explorer.fuse.io",
    ),
    RPCEndpoint(
        chain_id=80001,
        provider="Matic",
        network="mumbai",
        url="https://rpc-mumbai.maticvigil.com",
        explorer="https://mumbai.polygonscan.com/",
    ),
    RPCEndpoint(
        chain_id=69,
        provider="optimism-kovan",
        network="infura",
        url="https://optimism-kovan.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://kovan-optimistic.etherscan.io",
    ),
    RPCEndpoint(
        chain_id=1666600000,
        provider="Harmony",
        network="Harmony",
        url="https://api.harmony.one",
        explorer="https://explorer.harmony.one/",
    ),
    RPCEndpoint(
        chain_id=1666700000,
        provider="Harmony",
        network="Harmony Testnet",
        url="https://api.s0.b.hmny.io",
        explorer="https://explorer.pops.one/",
    ),
    RPCEndpoint(
        chain_id=421611,
        provider="Infura",
        network="Arbitrum Rinkeby",
        url="https://arbitrum-rinkeby.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://rinkeby-explorer.arbitrum.io/#/",
    ),
    RPCEndpoint(
        chain_id=42161,
        provider="Infura",
        network="Arbitrum One",
        url="https://arbitrum-mainnet.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://arbiscan.io",
    ),
    RPCEndpoint(
        chain_id=421613,
        provider="Infura",
        network="Arbitrum Goerli",
        url="https://arbitrum-goerli.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://goerli.arbiscan.io/",
    ),
    RPCEndpoint(
        chain_id=10200,
        provider="blockscout",
        network="Chiado testnet",
        url="https://rpc.chiadochain.net",
        explorer="https://blockscout.chiadochain.net/",
    ),
    RPCEndpoint(
        chain_id=100,
        provider="ankr",
        network="gnosis",
        url="https://rpc.ankr.com/gnosis",
        explorer="https://gnosisscan.io",
    ),
    RPCEndpoint(
        chain_id=10,
        provider="infura",
        network="optimism",
        url="https://optimism-mainnet.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://optimistic.etherscan.io/",
    ),
    RPCEndpoint(
        chain_id=420,
        provider="infura",
        network="optimism-goerli",
        url="https://optimism-goerli.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://goerli-optimism.etherscan.io/",
    ),
    RPCEndpoint(
        chain_id=3141,
        provider="Filecoin",
        network="filecoin-hyperspace",
        url="https://api.hyperspace.node.glif.io/rpc/v1",
        explorer="https://hyperspace.filfox.info/en",
    ),
    RPCEndpoint(
        chain_id=314159,
        provider="Filecoin",
        network="filecoin-calibration",
        url="https://api.calibration.node.glif.io/rpc/v1",
        explorer="https://calibration.filfox.info/en",
    ),
    RPCEndpoint(
        chain_id=314,
        provider="Filecoin",
        network="filecoin",
        url="https://api.node.glif.io/rpc/v1",
        explorer="https://filfox.info/en",
    ),
    RPCEndpoint(
        chain_id=11155111,
        provider="infura",
        network="sepolia",
        url="https://sepolia.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://sepolia.etherscan.io/",
    ),
    RPCEndpoint(
        chain_id=369,
        provider="PulseChain",
        network="pulsechain",
        url="https://rpc.pulsechain.com",
        explorer="https://scan.pulsechain.com/",
    ),
    RPCEndpoint(
        chain_id=943,
        provider="PulseChain Testnet",
        network="pulsechain-testnet",
        url="https://rpc.v4.testnet.pulsechain.com",
        explorer="https://scan.v4.testnet.pulsechain.com/",
    ),
    RPCEndpoint(
        chain_id=3441005,
        provider="caldera",
        network="manta-testnet",
        url="https://manta-testnet.calderachain.xyz/http",
        explorer="https://manta-testnet.calderaexplorer.xyz/",
    ),
    RPCEndpoint(
        chain_id=84531,
        provider="Base",
        network="Base Goerli",
        url="https://goerli.base.org",
        explorer="https://goerli.basescan.org/",
    ),
    RPCEndpoint(
        chain_id=5001,
        provider="Mantle",
        network="Mantle Testnet",
        url="https://rpc.testnet.mantle.xyz",
        explorer="https://explorer.testnet.mantle.xyz/",
    ),
    RPCEndpoint(
        chain_id=5000,
        provider="Mantle",
        network="Mantle",
        url="https://rpc.mantle.xyz",
        explorer="https://explorer.mantle.xyz/",
    ),
    RPCEndpoint(
        chain_id=2442,
        provider="Polygon",
        network="Polygon zkEVM Cardona Testnet",
        url="https://rpc.cardona.zkevm-rpc.com",
        explorer="https://cardona-zkevm.polygonscan.com/",
    ),
    RPCEndpoint(
        chain_id=1101,
        provider="Polygon",
        network="Polygon zkEVM",
        url="https://zkevm-rpc.com",
        explorer="https://zkevm.polygonscan.com/",
    ),
    RPCEndpoint(
        chain_id=59140,
        provider="Linea",
        network="Linea Goerli",
        url="https://rpc.goerli.linea.build",
        explorer="https://goerli.lineascan.build",
    ),
    RPCEndpoint(
        chain_id=59141,
        provider="Linea",
        network="Linea Sepolia",
        url="https://rpc.sepolia.linea.build",
        explorer="https://sepolia.lineascan.build",
    ),
    RPCEndpoint(
        chain_id=59144,
        provider="Linea",
        network="Linea",
        url="https://rpc.linea.build",
        explorer="https://lineascan.build/",
    ),
    RPCEndpoint(
        chain_id=2522,
        provider="Fraxtal",
        network="Fraxtal Testnet",
        url="https://rpc.testnet.frax.com",
        explorer="https://holesky.fraxscan.com",
    ),
    RPCEndpoint(
        chain_id=252,
        provider="Fraxtal",
        network="Fraxtal Mainnet",
        url="https://rpc.frax.com",
        explorer="https://fraxscan.com",
    ),
    RPCEndpoint(
        chain_id=1998,
        provider="Kyoto",
        network="Kyoto Testnet",
        url="https://rpc.testnet.kyotoprotocol.io:8545",
        explorer="https://testnet.kyotoscan.io",
    ),
    RPCEndpoint(
        chain_id=1444673419,
        provider="Skale",
        network="Skale Europa Testnet",
        url="https://testnet.skalenodes.com/v1/juicy-low-small-testnet",
        explorer="https://juicy-low-small-testnet.explorer.testnet.skalenodes.com",
    ),
    RPCEndpoint(
        chain_id=2046399126,
        provider="Skale",
        network="Skale Europa Mainnet",
        url="https://mainnet.skalenodes.com/v1/elated-tan-skat",
        explorer="https://elated-tan-skat.explorer.mainnet.skalenodes.com",
    ),
    RPCEndpoint(
        chain_id=324,
        provider="zksync",
        network="ZkSync Era Mainnet",
        url="https://mainnet.era.zksync.io",
        explorer="https://explorer.zksync.io",
    ),
    RPCEndpoint(
        chain_id=300,
        provider="zksync",
        network="ZkSync Era Sepolia Testnet",
        url="https://zksync-era-sepolia.blockpi.network/v1/rpc/public",
        explorer="https://sepolia.explorer.zksync.io",
    ),
    RPCEndpoint(
        chain_id=80002,
        provider="infura",
        network="Polygon Amoy Testnet",
        url="https://polygon-amoy.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://amoy.polygonscan.com/",
    ),
    RPCEndpoint(
        chain_id=11155420,
        provider="infura",
        network="Optimism Sepolia Testnet",
        url="https://optimism-sepolia.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://sepolia-optimism.etherscan.io/",
    ),
    RPCEndpoint(
        chain_id=421614,
        provider="infura",
        network="Arbitrum Sepolia Testnet",
        url="https://arbitrum-sepolia.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://sepolia.arbiscan.io/",
    ),
    RPCEndpoint(
        chain_id=5003,
        provider="Mantle",
        network="Mantle Sepolia Testnet",
        url="https://rpc.sepolia.mantle.xyz",
        explorer="https://explorer.sepolia.mantle.xyz",
    ),
    RPCEndpoint(
        chain_id=84532,
        provider="Base",
        network="Base Sepolia Testnet",
        url="https://sepolia.base.org",
        explorer="https://sepolia.basescan.org",
    ),
    RPCEndpoint(
        chain_id=111,
        provider="BOB",
        network="puff-bob-jznbxtoq7h",
        url="https://l2-puff-bob-jznbxtoq7h.t.conduit.xyz",
        explorer="https://testnet-explorer.gobob.xyz:443",
    ),
    RPCEndpoint(
        chain_id=60808,
        provider="BOB",
        network="BOB",
        url="https://rpc.gobob.xyz",
        explorer="hhttps://explorer.gobob.xyz:443",
    ),
    RPCEndpoint(
        chain_id=919,
        provider="mode",
        network="mode-sepolia-vtnhnpim72",
        url="https://rpc-mode-sepolia-vtnhnpim72.t.conduit.xyz",
        explorer="https://sepolia.explorer.mode.network:443",
    ),
    RPCEndpoint(
        chain_id=1918988905,
        provider="Rari",
        network="Rari Testnet",
        url="https://testnet.rpc.rarichain.org/http",
        explorer="https://sepolia.explorer.mode.network:443",
    ),
    RPCEndpoint(
        chain_id=41,
        provider="Telos",
        network="Telos EVM Testnet",
        url="https://testnet.telos.net/evm",
        explorer="https://testnet.teloscan.io",
    ),
    RPCEndpoint(
        chain_id=2340,
        provider="Atleta",
        network="Atleta Olympia",
        url="https://testnet-rpc.atleta.network:9944",
        explorer="https://blockscout.atleta.network",
    ),
    RPCEndpoint(
        chain_id=842,
        provider="Taraxa",
        network="Taraxa Testnet",
        url="https://rpc.testnet.taraxa.io",
        explorer="https://explorer.testnet.taraxa.io",
    ),
]


@dataclass
class EndpointList(ConfigOptions):
    """gets the rpc endpoint for current chain

    Returns:
        endpoint url...
    """

    endpoints: List[RPCEndpoint] = field(default_factory=lambda: default_endpoint_list)

    def get_chain_endpoint(self, chain_id: int = 1) -> Optional[RPCEndpoint]:
        """Get an Endpoint for the specified chain_id"""

        for endpoint in self.endpoints:
            if endpoint.chain_id == chain_id:
                return endpoint

        return None

    def find(
        self,
        *,
        chain_id: Optional[int] = None,
        provider: Optional[str] = None,
    ) -> list[RPCEndpoint]:

        result = []
        for ep in self.endpoints:

            if chain_id is not None:
                if chain_id != ep.chain_id:
                    continue
            if provider is not None:
                if provider != ep.provider:
                    continue

            result.append(ep)

        return result


if __name__ == "__main__":
    cf = ConfigFile(name="endpoints", config_type=EndpointList, config_format="yaml")

    config_endpoints = cf.get_config()

    print(config_endpoints)
