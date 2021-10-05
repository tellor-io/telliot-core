"""
Utils for creating a JSON RPC connection to an EVM blockchain
"""
from typing import Optional

from telliot.utils.base import Base
from web3 import Web3


class RPCEndpoint(Base):
    """JSON RPC Endpoint for EVM compatible network"""

    #: Blockchain Name
    # chain = Enum(*supported_networks)

    #: Network Name (e.g. 'mainnet', 'testnet', 'rinkebey')
    network: str

    #: Provider Name (e.g. 'Infura')
    provider: str

    #: URL (e.g. 'https://mainnet.infura.io/v3/<project_id>')
    url: str

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
