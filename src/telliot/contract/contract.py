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
            return ResponseStatus(ok=False, error=msg)

        self.node.connect()
        self.contract = self.node.web3.eth.contract(address=self.address, abi=self.abi)
        return ResponseStatus(ok=True)

    async def read(
        self, func_name: str, **kwargs: Any
    ) -> Tuple[Optional[Tuple[Any]], ResponseStatus]:
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
                return output, ResponseStatus(ok=True)
            except ValueError as e:
                msg = f"function '{func_name}' not found in contract abi"
                return None, ResponseStatus(ok=False, e=e, error_msg=msg)
        else:
            msg = "no instance of contract"
            return None, ResponseStatus(ok=False, error=msg)

    async def write(
        self, func_name: str, gas_price: int, acc_nonce: int, **kwargs: Any
    ) -> Tuple[Optional[AttributeDict[Any, Any]], ResponseStatus]:
        """For submitting any contract transaction once without retries

        gas price measured in gwei

        """

        status = ResponseStatus()

        if not self.contract:
            msg = "unable to connect to contract"
            return None, ResponseStatus(ok=False, error=msg)

        if not self.node:
            msg = "no node instance"
            return None, ResponseStatus(ok=False, error=msg)

        if self.private_key:
            acc = self.node.web3.eth.account.from_key(self.private_key)
        else:
            msg = "Private key missing"
            return None, ResponseStatus(ok=False, error=msg)
        try:
            # build transaction
            contract_function = self.contract.get_function_by_name(func_name)
            transaction = contract_function(**kwargs)
            # estimated_gas = transaction.estimateGas()
            gas_limit = 500000  # TODO optimize for gas/profitability
            print("estimated gas:", gas_limit)

            print("address: ----- ", acc.address)
            print("gas price:", gas_price)

            built_tx = transaction.buildTransaction(
                {
                    "from": acc.address,
                    "nonce": acc_nonce,
                    "gas": gas_limit,
                    "gasPrice": self.node.web3.toWei(gas_price, "gwei"),
                    "chainId": self.node.chain_id,
                }
            )

            # submit transaction
            tx_signed = acc.sign_transaction(built_tx)
            # pk = "af742bc879586358c353b5d64ec55efca9f789bb343568361431578df2f7aca3"
            # tx_signed = self.node.web3.eth.account.sign_transaction(built_tx, pk)
            print(" tx signed")
            tx_hash = self.node.web3.eth.send_raw_transaction(tx_signed.rawTransaction)
            print("tx sent")
            # Confirm transaction
            tx_receipt = self.node.web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=360
            )

            # Point to relevant explorer
            print(
                f"""View reported data: \n
                {self.node.explorer}/tx/{tx_hash.hex()}
                """
            )

            return tx_receipt, status
        except Exception as e:
            status.ok = False
            status.error = str(e.args)
            status.e = e
            return None, status

    async def write_with_retry(
        self,
        func_name: str,
        gas_price: int,
        extra_gas_price: int,
        retries: int,
        **kwargs: Any,
    ) -> Tuple[Optional[List[AttributeDict[Any, Any]]], ResponseStatus]:
        """For submitting any contract transaction. Retries supported!

        gas_price measured in gwei

        """

        try:
            status = ResponseStatus()
            acc = self.node.web3.eth.account.from_key(self.private_key)
            acc_nonce = self.node.web3.eth.get_transaction_count(acc.address)

            transaction_receipts = []
            # Iterate through retry attempts
            for _ in range(retries + 1):

                tx_receipt, status = await self.write(
                    func_name=func_name,
                    gas_price=gas_price,
                    acc_nonce=acc_nonce,
                    **kwargs,
                )

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
                elif not status.ok and status.error and "already known" in status.error:
                    continue
                elif not status.ok and status.error and "nonce too low":
                    acc_nonce += 1
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
