"""
Utils for connecting to an EVM contract
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from eth_typing.evm import ChecksumAddress
from eth_account.account import Account
from telliot.contract.gas import estimate_gas
from telliot.model.endpoints import RPCEndpoint
from telliot.utils.response import ResponseStatus
from web3 import Web3
from web3.datastructures import AttributeDict


class Contract:
    """Convenience wrapper for connecting to an Ethereum contract"""

    def __init__(
        self,
        address: Union[str, ChecksumAddress],
        abi: Union[List[Dict[str, Any]], str],
        node: RPCEndpoint,
        private_key: str = "",
    ):

        self.address = Web3.toChecksumAddress(address)
        self.abi = abi
        self.node = node
        self.contract = None
        self.private_key = private_key

    def connect(self) -> ResponseStatus:
        """Connect to EVM contract through an RPC Endpoint"""

        if not self.node.web3:
            msg = "node is not instantiated"
            return ResponseStatus(ok=False, error_msg=msg)

        self.node.connect()
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
        func_name:str,
        gas_price: int,
        extra_gas_price,
        **kwargs:int
    ) -> Tuple[AttributeDict[Any, Any], ResponseStatus]:

        status = ResponseStatus()

        if not self.contract:
            msg = "unable to connect to contract"
            return None, ResponseStatus(ok=False, error_msg=msg)

        if not self.node:
            msg = "no node instance"
            return  None, ResponseStatus(ok=False, error_msg=msg)

        if self.private_key:
            acc = self.node.web3.eth.account.from_key(self.private_key)
        else:
            msg = "Private key missing"
            return None, ResponseStatus(ok=False, error_msg=msg)
        try:
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
            gas_price = estimate_gas + extra_gas_price

            # submit transaction
            tx_signed = acc.sign_transaction(built_tx)

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

            return tx_receipt, status
        except Exception as e:
            status.ok = False
            status.error = str(e.args)
            status.e = e
            return None, status

    def write_with_retry(
        self,
        func_name: str,
        gas_price: int,
        extra_gas_price: int,
        retries: int,
        **kwargs: Any,
    ) -> Tuple[Optional[List[AttributeDict[Any, Any]]], ResponseStatus]:
        """For submitting any contract transaction. Retries supported!"""

        try:
            transaction_receipts = []
            # Iterate through retry attempts
            for _ in range(retries + 1):
                
                tx_receipt, status = self.write(func_name=func_name, gas_price=gas_price, kwargs=kwargs)

                # Exit loop if transaction successful
                if tx_receipt and status.ok:
                    transaction_receipts.append(tx_receipt)
                    return transaction_receipts, status
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

            return transaction_receipts, status

        except Exception as e:
            status.ok = False
            status.error = str(e.args)
            status.e = e
            return None, status

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
