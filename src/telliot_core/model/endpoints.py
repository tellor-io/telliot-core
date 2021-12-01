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
            print(e)
            print(msg)

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
        chain_id=4,
        provider="Infura",
        network="rinkeby",
        url="wss://rinkeby.infura.io/ws/v3{INFURA_API_KEY}",
        explorer="https://rinkeby.etherscan.io",
    ),
    RPCEndpoint(
        chain_id=137,
        provider="Matic",
        network="mainnet",
        url="https://rpc-mainnet.matic.network",
        explorer="https://matic.network",
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


if __name__ == "__main__":
    cf = ConfigFile(name="endpoints", config_type=EndpointList, config_format="yaml")

    config_endpoints = cf.get_config()

    print(config_endpoints)
