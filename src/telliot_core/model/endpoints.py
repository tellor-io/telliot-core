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

    #: Network Name (e.g. 'mainnet', 'testnet', 'rinkeby')
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

        # Inject middleware if connecting to rinkeby (chain_id=4)
        if self.chain_id == 4:
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
        chain_id=137,
        provider="Matic",
        network="mainnet",
        url="https://rpc-mainnet.matic.network",
        explorer="https://matic.network",
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
        chain_id=941,
        provider="Pulsechain",
        network="Pulsechain Testnet",
        url="https://rpc.v2b.testnet.pulsechain.com",
        explorer="https://scan.v2b.testnet.pulsechain.com",
    ),
    RPCEndpoint(
        chain_id=42161,
        provider="Infura",
        network="Arbitrum One",
        url="https://arbitrum-mainnet.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://arbiscan.io",
    ),
]


@dataclass
class EndpointList(ConfigOptions):
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
