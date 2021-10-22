"""
Utils for connecting to an EVM contract
"""
import json
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import requests
import web3
from eth_typing.evm import ChecksumAddress
from telliot.apps.telliot_config import TelliotConfig
from telliot.utils.base import Base
from telliot.utils.response import ResponseStatus
from web3 import Web3
from web3.datastructures import AttributeDict


class Contract(Base):
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    # node: RPCEndpoint

    #: Contract address
    address: Union[str, ChecksumAddress]

    #: ABI specifications of contract
    abi: Union[List[Dict[str, Any]], str]

    #: web3 contract object
    contract: Optional[web3.contract.Contract]

    #: global pytelliot configurations
    config: TelliotConfig

    def connect(self) -> ResponseStatus:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.config.get_endpoint() is None:
            msg = "node not configurated"
            return ResponseStatus(ok=False, error_msg=msg)

        elif self.config.get_endpoint().web3 is None:
            msg = "node is not instantiated"
            return ResponseStatus(ok=False, error_msg=msg)

        else:
            if not self.config.get_endpoint().connect():
                msg = "node is not connected"
                return ResponseStatus(ok=False, error_msg=msg)
            self.address = Web3.toChecksumAddress(self.address)
            self.contract = self.config.get_endpoint().web3.eth.contract(
                address=self.address, abi=self.abi
            )
            return ResponseStatus(ok=True)

    def read(self, func_name: str, **kwargs: Any) -> Tuple[ResponseStatus, Optional[Tuple[Any]]]:
        """
        Reads data from contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        ResponseStatus: standard response for contract data
        """

        if self.contract:
            try:
                contract_function = self.contract.get_function_by_name(func_name)
                output = contract_function(**kwargs).call()
                return ResponseStatus(ok=True), output
            except ValueError as e:
                msg = f"function '{func_name}' not found in contract abi"
                return ResponseStatus(ok=False, error=e, error_msg=msg), None
        else:
            if self.connect():
                msg = "now connected to contract"
                return self.read(func_name=func_name, **kwargs)
            else:
                msg = "unable to connect to contract"
                return ResponseStatus(ok=False, error_msg=msg), None

    def write(
        self,
        func_name: str,
        gas_price: int,
        extra_gas_price: int,
        retries: int,
        **kwargs: Any,
    ) -> Tuple[ResponseStatus, Optional[List[AttributeDict[Any, Any]]], int]:
        """For submitting any contract transaction. Retries supported!"""
        if self.contract:
            try:
                status = ResponseStatus()

                # build transaction
                acc_nonce = (
                    self.config.get_endpoint().web3.eth.get_transaction_count(
                        self.config.acc.address
                    )
                )
                contract_function = self.contract.get_function_by_name(func_name)
                transaction = contract_function(**kwargs)
                estimated_gas = transaction.estimateGas()
                print("estimated gas:", estimated_gas)

                built_tx = transaction.buildTransaction(
                    {
                        "nonce": acc_nonce,
                        "gas": estimated_gas,
                        "gasPrice": self.config.get_endpoint().web3.toWei(gas_price, "gwei"),
                        "chainId": self.config.get_endpoint().chain_id,
                    }
                )

                # get gas price
                rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
                prices = json.loads(rsp.content)
                gas_price = int(prices["fast"] + extra_gas_price)

                # submit transaction
                tx_signed = self.config.acc.address.sign_transaction(built_tx)

                tx_hash = self.config.get_endpoint().web3.eth.send_raw_transaction(
                    tx_signed.rawTransaction
                )

                # Confirm transaction
                tx_receipt = self.config.get_endpoint().web3.eth.wait_for_transaction_receipt(
                    tx_hash, timeout=360
                )

                # Point to relevant explorer
                print(
                    f"View reported data: {self.config.get_endpoint().explorer}{tx_hash.hex()}"
                )

                return status, tx_receipt, gas_price
            except Exception as e:
                status.ok = False
                status.error = str(e.args)
                status.e = e
                return status, None, gas_price
        else:
            if self.connect():
                msg = "now connected to contract"
                return self.write(
                    func_name=func_name,
                    gas_price=gas_price,
                    extra_gas_price=extra_gas_price,
                    **kwargs,
                )
            else:
                msg = "unable to connect to contract"
                return ResponseStatus(ok=False, error_msg=msg), None, gas_price

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
