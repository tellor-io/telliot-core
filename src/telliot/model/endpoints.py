"""
Utils for creating a JSON RPC connection to an EVM blockchain
"""
from typing import List
from typing import Optional

from pydantic import Field
from telliot.apps.config import ConfigFile
from telliot.apps.config import ConfigOptions
from telliot.model.base import Base
from web3 import Web3
from web3.middleware import geth_poa_middleware


class RPCEndpoint(Base):
    """JSON RPC Endpoint for EVM compatible network"""

    #: Chain ID
    chain_id: Optional[int] = None

    #: Network Name (e.g. 'mainnet', 'testnet', 'rinkeby')
    network: str

    #: Provider Name (e.g. 'Infura')
    provider: str

    #: URL (e.g. 'https://mainnet.infura.io/v3/<project_id>')
    url: str

    #: Exploerer URL ')
    explorer: Optional[str] = None

    #: Read-only Web3 Connection with private storage
    web3 = property(lambda self: self._web3)
    _web3: Optional[Web3] = None

    def connect(self) -> bool:
        """Connect to EVM blockchain

        returns:
            True if connection was successful
        """

        if self._web3:
            return True

        self._web3 = Web3(Web3.HTTPProvider(self.url))
        # Inject middlware if connecting to rinkeby
        try:
            if self.network == "rinkeby":
                self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        except Exception:
            print("unable to connect to rinkeby")

        try:
            connected = self._web3.isConnected()
        # Pokt nodes won't submit isConnected rpc call
        except Exception:
            connected = self._web3.eth.get_block_number() > 1
        if connected:
            print("Connected to {}".format(self))
        else:
            print("Could not connect to {}".format(self))

        return connected


default_endpoint_list = [
    RPCEndpoint(
        chain_id=1,
        provider="Infura",
        network="mainnet",
        url="https://mainnet.infura.io/v3/{INFURA_API_KEY}",
        explorer="https://etherscan.io",
    ),
    RPCEndpoint(
        chain_id=4,
        provider="Infura",
        network="rinkeby",
        url="https://rinkeby.infura.io/v3/{INFURA_API_KEY}",
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


class EndpointList(ConfigOptions):

    endpoints: List[RPCEndpoint] = Field(default=default_endpoint_list)

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
