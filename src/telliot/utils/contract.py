"""
Utils for connecting to an EVM contract
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import web3
from telliot.utils.base import Base
from telliot.utils.rpc_endpoint import RPCEndpoint


class Contract(Base):
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    #: Contract address
    address: str

    #: ABI specifications of contract
    abi: List[Dict[str, Any]]

    #: web3 contract object
    web3_contract: Optional[web3.contract.Contract]

    class Config:
        arbitrary_types_allowed = True

    @property
    def contract(self) -> Union[web3.contract.Contract, None]:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3:
            if self.node.connect():
                return self.node.web3.eth.contract(address=self.address, abi=self.abi)
            else:
                print("rpc endpoint not connected")
                return None
        else:
            print("rpc endpoint not instantiated")
            return None
