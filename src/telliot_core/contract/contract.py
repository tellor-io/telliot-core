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
from telliot_core.utils.response import error_status
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
        self, func_name: str, *args: Any, **kwargs: Any
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
                output = contract_function(*args, **kwargs).call()
                return output, ResponseStatus(ok=True)
            except ValueError as e:
                msg = f"function '{func_name}' not found in contract abi"
                return None, ResponseStatus(ok=False, e=e, error=msg)
        else:
            msg = "no instance of contract"
            return None, ResponseStatus(ok=False, error=msg)

    async def write(
        self,
        func_name: str,
        gas_price: int,
        max_priority_fee_per_gas: int,
        max_fee_per_gas: int,
        acc_nonce: int,
        gas_limit: int,
        **kwargs: Any,
    ) -> Tuple[Optional[AttributeDict[Any, Any]], ResponseStatus]:
        """For submitting any contract transaction once without retries

        gas price measured in gwei

        """

        status = ResponseStatus()

        if not self.contract:
            msg = f"Contract.write({func_name}) error: Unable to connect to contract"
            return None, error_status(msg, log=logger.error)

        if not self.node:
            msg = f"Contract.write({func_name}) error: No node instance"
            return None, error_status(msg, log=logger.error)

        if self.private_key:
            acc = self.node.web3.eth.account.from_key(self.private_key)
        else:
            msg = f"Contract.write({func_name}) error: Private key missing"
            return None, error_status(msg, log=logger.error)

        try:
            # build transaction
            contract_function = self.contract.get_function_by_name(func_name)
            transaction = contract_function(**kwargs)

            #start tx dict with static elements
            tx_dict = {
                "from": acc.address,
                "nonce": acc_nonce,
                "gas": gas_limit,
                "chainId": self.node.chain_id
            }

            #if legacy gas price is not None, use it
            if gas_price is not None:
                tx_dict["gasPrice"] = self.node.web3.toWei(gas_price, "gwei")

            #else if (if legacy gas price is None) and max fee is not None, use max fee
            elif max_fee_per_gas is not None:
                tx_dict["maxFeePerGas"] = self.node.web3.toWei(max_fee_per_gas, "gwei")

            #else if (if legacy price and max fee are not provided), use max priority fee
            elif max_priority_fee_per_gas is not None:
                tx_dict["maxPriorityFeePerGas"] = self.node.web3.toWei(max_priority_fee_per_gas, "gwei")

            #else (if none are provided) estimate max priority fee with rpc node
            else:
                tx_dict["maxPriorityFeePerGas"] = self.node.web3.eth.max_priority_fee
            #pass in tx dict to build the transaction
            built_tx = transaction.buildTransaction(tx_dict)
            # submit transaction
            tx_signed = acc.sign_transaction(built_tx)

        except Exception as e:
            note = "Failed to build transaction"
            return None, error_status(note, log=logger.error, e=e)

        try:
            logger.debug(f"Sending transaction: {func_name}")
            tx_hash = self.node.web3.eth.send_raw_transaction(tx_signed.rawTransaction)

        except Exception as e:
            note = "Send transaction failed"
            return None, error_status(note, log=logger.error, e=e)

        try:
            # Confirm transaction
            tx_receipt = self.node.web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=360
            )

            tx_url = f"{self.node.explorer}/tx/{tx_hash.hex()}"

            if tx_receipt["status"] == 1:
                logger.info(f"{func_name} transaction succeeded. ({tx_url})")
                return tx_receipt, status

            elif tx_receipt["status"] == 0:
                msg = f"{func_name} transaction reverted. ({tx_url})"
                return tx_receipt, error_status(msg, log=logger.error)

            return tx_receipt, status

        except Exception as e:
            note = "Failed to confirm transaction"
            return None, error_status(note, log=logger.error, e=e)

    async def write_with_retry(
        self,
        func_name: str,
        gas_price: int,
        max_priority_fee_per_gas: int,
        max_fee_per_gas: int,
        extra_gas_price: int,
        retries: int,
        gas_limit: int,
        **kwargs: Any,
    ) -> Tuple[Optional[AttributeDict[Any, Any]], ResponseStatus]:
        """For submitting any contract transaction. Retries supported!

        gas_price measured in gwei

        """

        try:
            status = ResponseStatus()
            acc = self.node.web3.eth.account.from_key(self.private_key)
            acc_nonce = self.node.web3.eth.get_transaction_count(acc.address)

            using_legacy_gas = False
            if gas_price is not None:
                using_legacy_gas = True

            # Iterate through retry attempts
            for k in range(retries + 1):

                attempt = k + 1

                if k >= 1:
                    logger.info(f"Retrying {func_name} (attempt #{attempt})")

                # Attempt write
                tx_receipt, status = await self.write(
                    func_name=func_name,
                    gas_price=gas_price,
                    max_priority_fee_per_gas=max_priority_fee_per_gas,
                    max_fee_per_gas=max_fee_per_gas,
                    acc_nonce=acc_nonce,
                    gas_limit=gas_limit,
                    **kwargs,
                )

                logger.debug(f"Attempt {attempt} status: ", status)

                # Exit loop if transaction successful
                if status.ok:
                    assert tx_receipt  # for typing
                    tx_url = (
                        f"{self.node.explorer}/tx/{tx_receipt['transactionHash'].hex()}"
                    )

                    if tx_receipt["status"] == 1:
                        return tx_receipt, status

                    elif tx_receipt["status"] == 0:
                        msg = f"Write attempt {attempt} failed, tx reverted ({tx_url}):"
                        return tx_receipt, error_status(msg, log=logger.info)

                    else:
                        msg = f"Write attempt {attempt}: Invalid TX Receipt status: {tx_receipt['status']}"  # noqa: E501
                        error_status(msg, log=logger.info)

                else:
                    logger.info(f"Write attempt {attempt} failed:")
                    msg = str(status.error)
                    error_status(msg, log=logger.info)
                    if status.error:
                        if "replacement transaction underpriced" in status.error:
                            if using_legacy_gas:
                                gas_price += extra_gas_price
                            else:
                                max_priority_fee_per_gas += extra_gas_price
                            logger.info(f"Next gas price: {gas_price}")
                        elif "already known" in status.error:
                            acc_nonce += 1
                            logger.info(f"Incrementing nonce: {acc_nonce}")
                        elif "nonce too low" in status.error:
                            acc_nonce += 1
                            logger.info(f"Incrementing nonce: {acc_nonce}")
                        # a different rpc error
                        elif "nonce is too low" in status.error:
                            acc_nonce += 1
                            logger.info(f"Incrementing nonce: {acc_nonce}")
                        elif "not in the chain" in status.error:
                            if using_legacy_gas:
                                gas_price += extra_gas_price
                            else:
                                max_priority_fee_per_gas += extra_gas_price                            logger.info(f"Next gas price: {gas_price}")
                        else:
                            extra_gas_price = 0

            status.ok = False
            status.error = "ran out of retries, tx unsuccessful"

            return tx_receipt, status

        except Exception as e:
            return None, error_status("Other error", log=logger.error, e=e)

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
