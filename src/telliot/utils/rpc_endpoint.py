"""
Utils for:
- creating a JSON RPC connection to an EVM blockchain
- connecting to an EVM contract
"""
from typing import Optional
from typing import Union

import web3
from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel
from web3 import Web3


class RPCEndpoint(BaseModel):
    """JSON RPC Endpoint for EVM compatible network"""

    #: Blockchain Name
    # chain = Enum(*supported_networks)

    #: Network Name (e.g. 'mainnet', 'testnet', 'rinkebey')
    network: str

    #: Provider Name (e.g. 'Infura')
    provider: str

    #: URL (e.g. 'https://mainnet.infura.io/v3/<project_id>')
    url: str

    #: Web3 Connection
    web3: Optional[Web3] = None

    class Config:
        arbitrary_types_allowed = True

    def connect(self) -> Web3:
        """Connect to EVM blockchain"""
        self.web3 = Web3(Web3.HTTPProvider(self.url))
        try:
            connected = self.web3.isConnected()
        # Pokt nodes won't submit isConnected rpc call
        except Exception:
            connected = self.web3.eth.get_block_number() > 1
        if connected:
            print("Connected to {}".format(self))
        else:
            print("Could not connect to {}".format(self))

        return self.web3


@dataclass
class Contract:
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    address: str

    #: Abi specifications of contract, likely loaded from JSON
    abi: str

    def connect(self) -> Union[web3.contract.Contract, TypeError]:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3 is None:
            return TypeError("node is not connected")
        else:
            self.Contract = self.node.web3.eth.contract(
                address=self.address, abi=self.abi
            )
            return self.Contract
