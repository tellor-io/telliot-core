"""
Utils for connecting to an EVM contract
"""
import asyncio
import logging
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from chained_accounts import ChainedAccount
from eth_typing.evm import ChecksumAddress
from eth_utils.address import to_checksum_address
from web3.datastructures import AttributeDict

from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.key_helpers import lazy_key_getter
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
        account: Optional[ChainedAccount] = None,
    ):

        self.address = to_checksum_address(address)
        self.abi = abi
        self.node = node
        self.contract = None
        self.account = account
        self._private_key: Optional[bytes] = None

    def connect(self) -> ResponseStatus:
        """Connect to EVM contract through an RPC Endpoint"""

        if not self.node.web3:
            msg = "node is not instantiated"
            return ResponseStatus(ok=False, error=msg)

        self.node.connect()
        self.contract = self.node.web3.eth.contract(address=self.address, abi=self.abi)
        return ResponseStatus(ok=True)

    async def read(self, func_name: str, *args: Any, **kwargs: Any) -> Tuple[Any, ResponseStatus]:
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
            except asyncio.exceptions.TimeoutError as e:
                msg = "timeout reading from contract"
                return None, ResponseStatus(ok=False, e=e, error=msg)
            except Exception as e:
                msg = "error reading from contract"
                return None, ResponseStatus(ok=False, e=e, error=msg)
        else:
            msg = "no instance of contract"
            return None, ResponseStatus(ok=False, error=msg)

    @property
    def private_key(self) -> bytes:

        if not self._private_key:
            self._private_key = lazy_key_getter(self.account)

        return self._private_key

    async def write(
        self,
        func_name: str,
        gas_limit: int,
        legacy_gas_price: Optional[int] = None,
        max_priority_fee_per_gas: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
        acc_nonce: Optional[int] = None,
        **kwargs: Any,
    ) -> Tuple[Optional[AttributeDict[Any, Any]], ResponseStatus]:
        """For submitting any contract transaction once without retries

        gas price measured in gwei

        """

        # Validate inputs
        if (legacy_gas_price is not None) and ((max_fee_per_gas is not None) or (max_priority_fee_per_gas is not None)):
            raise ValueError(
                """invalid combination of legacy gas arguments
                 and EIP-1559 gas arguments"""
            )

        if (legacy_gas_price is None) and (max_fee_per_gas is None) and (max_priority_fee_per_gas is None):
            raise ValueError("no gas strategy selected!")

        status = ResponseStatus()

        if not acc_nonce:
            acc = self.node.web3.eth.account.from_key(self.private_key)
            acc_nonce = self.node.web3.eth.get_transaction_count(acc.address)

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

            # start tx dict with static elements
            tx_dict = {
                "from": acc.address,
                "nonce": acc_nonce,
            }
            # Estimate gas_limit if not provided
            if gas_limit is None:
                try:
                    gas_limit = transaction.estimateGas(tx_dict)
                except Exception as e:
                    msg = f"Contract.write({func_name}) error: Unable to estimate gas"
                    return None, error_status(msg, e=e, log=logger.error)

            tx_dict["gas"] = gas_limit
            # use legacy gas strategy if only legacy gas price is provided
            if legacy_gas_price is not None:

                if (max_fee_per_gas is not None) or (max_priority_fee_per_gas is not None):
                    raise ValueError(
                        """"cannot use both legacy gas arguments
                        and type 2 transaction (EIP1559) args in one transaction"""
                    )

                tx_dict["gasPrice"] = self.node.web3.toWei(legacy_gas_price, "gwei")

            # use EIP-1559 gas strategy if maxFeePerGas
            # and/or MaxPriorityFeePerGas are provided
            else:
                if legacy_gas_price is not None:
                    raise ValueError(
                        """"cannot use both legacy gas arguments
                         and type 2 transaction (EIP1559) args in one transaction"""
                    )

                if max_fee_per_gas is not None:
                    tx_dict["maxFeePerGas"] = self.node.web3.toWei(max_fee_per_gas, "gwei")

                    if max_priority_fee_per_gas is not None:
                        tx_dict["maxPriorityFeePerGas"] = self.node.web3.toWei(max_priority_fee_per_gas, "gwei")

                    # else if (if legacy price and max fee are not provided)
                    # use max priority fee
                    elif max_priority_fee_per_gas is not None:
                        tx_dict["maxPriorityFeePerGas"] = self.node.web3.toWei(max_priority_fee_per_gas, "gwei")

                    # raise ValueError if no gas arguments are provided
                    else:
                        raise ValueError(
                            """no gas strategy selected!
                            must provide either legacy
                            or EIP-1559 gas arguments"""
                        )
            # pass in tx dict to build the transaction
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
            tx_receipt = self.node.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=360)

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
