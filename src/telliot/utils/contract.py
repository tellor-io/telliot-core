"""
Utils for connecting to an EVM contract
"""

import json

from typing import Any, Callable, Tuple
from typing import Dict
from typing import List
from typing import Optional
import requests

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
    contract: Optional[web3.contract.Contract]

    class Config:
        arbitrary_types_allowed = True

    def connect(self) -> None:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3 is None:
            print("node is not instantiated")
        else:
            if not self.node.connect():
                print("node is not connected")
            self.contract = self.node.web3.eth.contract(
                address=self.address, abi=self.abi
            )

    def read(self,func_name:str, **kwargs:Any) -> Tuple[Tuple, bool]: 
        """
        Reads data from contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        Tuple: contains contract function outputs (tuple) and success (bool)
        """

        try:
            contract_function = self.contract.get_function_by_name(func_name)
            return (contract_function(**kwargs).call(), True)
        except ValueError:
            print(f"function '{func_name}' not found in contract abi")
            return ((), False)

    def write(self, func_name:str, **kwargs:Any) -> bool:
        """
        Writes data to contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        bool: success
        """
        try:
            acc_nonce = self.node.web3.eth.get_transaction_count(self.acc.address)
            req = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
            prices = json.loads(req.content)
            gas_price = str(prices["fast"])
            print("retrieved gas price:", gas_price)

            contract_function = self.contract.get_function_by_name(func_name)
            tx = contract_function(**kwargs).build_transaction(
                {
                "nonce": acc_nonce,
                "gas": 4000000,
                "gasPrice": self.w3.toWei(gas_price, "gwei"),
                "chainId": self.chain_id,
            }
            )

            tx_signed = self.acc.sign_transaction(tx)

            tx_hash = self.w3.eth.send_raw_transaction(tx_signed.rawTransaction)
            print(f"View reported data: https://rinkeby.etherscan.io/tx/{tx_hash.hex()}")


            _ = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=360)

            return True
        except Exception:
            print("tx was unsuccessful")
            return False