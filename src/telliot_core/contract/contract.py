"""
Utils for connecting to an EVM contract
"""
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from eth_typing.evm import ChecksumAddress
from web3 import Web3
from web3.datastructures import AttributeDict

from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.response import ResponseStatus

logger = logging.getLogger(__name__)


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
                return None, ResponseStatus(ok=False, e=e, error=msg)
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
            logger.info("gas limit:", gas_limit)

            logger.info("address: ----- ", acc.address)
            logger.info("gas price:", gas_price)

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
            logger.info(" tx signed")
            tx_hash = self.node.web3.eth.send_raw_transaction(tx_signed.rawTransaction)
            logger.info("tx sent")
            # Confirm transaction
            tx_receipt = self.node.web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=360
            )

            # Point to relevant explorer
            logger.info(
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
    ) -> Tuple[Optional[AttributeDict[Any, Any]], ResponseStatus]:
        """For submitting any contract transaction. Retries supported!

        gas_price measured in gwei

        """

        try:
            status = ResponseStatus()
            acc = self.node.web3.eth.account.from_key(self.private_key)
            acc_nonce = self.node.web3.eth.get_transaction_count(acc.address)

            # Iterate through retry attempts
            for _ in range(retries + 1):

                tx_receipt, status = await self.write(
                    func_name=func_name,
                    gas_price=gas_price,
                    acc_nonce=acc_nonce,
                    **kwargs,
                )

                logger.info("write status: ", status)

                # Exit loop if transaction successful
                if tx_receipt and status.ok and tx_receipt["status"] == 1:
                    logger.info(
                        f"tx was successful! check it out at {self.node.explorer}/tx/{tx_receipt['transactionHash']}"  # noqa: E501
                    )  # noqa: E501
                    return tx_receipt, status
                elif (
                    not status.ok
                    and status.error
                    and "replacement transaction underpriced" in status.error
                ):
                    gas_price += extra_gas_price
                elif not status.ok and status.error and "already known" in status.error:
                    acc_nonce += 1
                elif not status.ok and status.error and "nonce too low" in status.error:
                    acc_nonce += 1
                # a different rpc error
                elif (
                    not status.ok
                    and status.error
                    and "nonce is too low" in status.error
                ):
                    acc_nonce += 1
                elif (
                    not status.ok
                    and status.error
                    and "not in the chain" in status.error
                ):
                    gas_price += extra_gas_price
                elif (
                    status.ok
                    and tx_receipt["status"] == 0  # type: ignore # error won't be none
                ):
                    status.error = "tx reverted by contract/evm logic"
                    logger.info(f"tx was reverted by evm! check it out at {self.node.explorer}/tx/{tx_receipt['transactionHash']}")  # type: ignore # tx receipt won't be none # noqa: E501
                    return tx_receipt, status
                else:
                    extra_gas_price = 0

            status.ok = False
            status.error = "ran out of retries, tx unsuccessful"

            return tx_receipt, status

        except Exception as e:
            status.ok = False
            status.error = str(e.args)
            status.e = e
            return None, status

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
