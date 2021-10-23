"""
Utils for connecting to an EVM contract
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import web3
from eth_typing.evm import ChecksumAddress
from telliot.apps.telliot_config import TelliotConfig
from telliot.utils.base import Base
from telliot.utils.response import ResponseStatus
from telliot.contract.gas import fetch_gas_price
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
        extra_gas_price: int = 0,
        **kwargs: Any,
    ) -> Tuple[ResponseStatus, Optional[AttributeDict[Any, Any]]]:
        """For submitting any contract transaction. Retries supported!"""
        if self.contract:
            try:
                status = ResponseStatus()

                #fetch gas price
                gas_price_status, gas_price = fetch_gas_price()

                #exit and report status if gas price couldn't be fetched
                if gas_price_status.ok is False:
                    status.error = "Can't submit transaction: couldn't fetch gas price"
                    status.ok = False
                    status.e = gas_price_status.e
                    return status, None

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

                return status, tx_receipt
            except Exception as e:
                status.ok = False
                status.error = str(e.args)
                status.e = e
                return status, None
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
                return ResponseStatus(ok=False, error_msg=msg), None

    def write_with_retries(
        self,
        func_name: str,
        extra_gas_price: int,
        num_retries: int,
        **kwargs: Any,
    ) -> Tuple[ResponseStatus, Optional[List[AttributeDict[Any, Any]]]]:

        tx_receipts = []

        for _ in range(num_retries + 1):

            status, tx_receipt, gas_price = self.write(func_name=func_name, gas_price=gas_price, extra_gas_price=extra_gas_price, kwargs=kwargs)

            if tx_receipt and status.ok:
                tx_receipts.append(tx_receipt)
                break
            elif (
                not status.ok
                and status.error
                and "replacement transaction underpriced" in status.error
            ):
                extra_gas_price += gas_price
            else:
                extra_gas_price = 0

        return status, tx_receipts

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
