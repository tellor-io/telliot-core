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
from telliot.model.endpoints import RPCEndpoint
from telliot.utils.base import Base
from telliot.utils.response import ResponseStatus
from web3 import Web3
from web3.datastructures import AttributeDict


class Contract(Base):
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: Contract address
    address: Union[str, ChecksumAddress]

    #: ABI specifications of contract
    abi: Union[List[Dict[str, Any]], str]

    #: web3 contract object
    contract: Optional[web3.contract.Contract]

    #: global pytelliot configurations
    config: TelliotConfig

    #: RPCNode connection to Ethereum network
    node: Optional[RPCEndpoint]

    def connect(self) -> ResponseStatus:
        """Connect to EVM contract through an RPC Endpoint"""
        self.node = self.config.get_endpoint()

        if not self.node:
            msg = "node not configured"
            return ResponseStatus(ok=False, error_msg=msg)
        else:
            if not self.node.web3:
                msg = "node is not instantiated"
                return ResponseStatus(ok=False, error_msg=msg)

        self.node.connect()
        self.address = Web3.toChecksumAddress(self.address)
        self.contract = self.node.web3.eth.contract(address=self.address, abi=self.abi)
        return ResponseStatus(ok=True)

    def read(
        self, func_name: str, **kwargs: Any
    ) -> Tuple[ResponseStatus, Optional[Tuple[Any]]]:
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
            msg = "no instance of contract"
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
        if not self.contract:
            msg = "unable to connect to contract"
            return ResponseStatus(ok=False, error_msg=msg), None, gas_price

        if not self.node:
            msg = "no node instance"
            return ResponseStatus(ok=False, error_msg=msg), None, gas_price

        acc = self.node.web3.eth.account.from_key(self.config.main.private_key)

        try:
            transaction_receipts = []
            # Iterate through retry attempts
            for _ in range(retries + 1):
                status = ResponseStatus()

                # build transaction
                acc_nonce = self.node.web3.eth.get_transaction_count(acc.address)
                contract_function = self.contract.get_function_by_name(func_name)
                transaction = contract_function(**kwargs)
                estimated_gas = transaction.estimateGas()
                print("estimated gas:", estimated_gas)

                built_tx = transaction.buildTransaction(
                    {
                        "nonce": acc_nonce,
                        "gas": estimated_gas,
                        "gasPrice": self.node.web3.toWei(gas_price, "gwei"),
                        "chainId": self.node.chain_id,
                    }
                )

                # get gas price
                rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
                prices = json.loads(rsp.content)
                gas_price = int(prices["fast"] + extra_gas_price)

                # submit transaction
                tx_signed = acc.address.sign_transaction(built_tx)

                tx_hash = self.node.web3.eth.send_raw_transaction(
                    tx_signed.rawTransaction
                )

                # Confirm transaction
                tx_receipt = self.node.web3.eth.wait_for_transaction_receipt(
                    tx_hash, timeout=360
                )

                # Point to relevant explorer
                print(
                    f"""View reported data: \n
                    {self.node.explorer}{tx_hash.hex()}
                    """
                )

                # Exit loop if transaction successful
                if tx_receipt and status.ok:
                    transaction_receipts.append(tx_receipt)
                    return status, transaction_receipts, gas_price
                elif (
                    not status.ok
                    and status.error
                    and "replacement transaction underpriced" in status.error
                ):
                    extra_gas_price += gas_price
                else:
                    extra_gas_price = 0

            status.ok = False
            status.error = "ran out of retries, tx unsuccessful"

            return status, transaction_receipts, gas_price

        except Exception as e:
            status.ok = False
            status.error = str(e.args)
            status.e = e
            return status, None, gas_price

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
