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
from telliot.contract.gas import estimate_gas
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

    def read(
        self, func_name: str, **kwargs: Any
    ) -> Tuple[Optional[Tuple[Any]], ResponseStatus]:
        """
        Reads data from contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        Tuple: output of contract getter
        ResponseStatus: standard response for contract data
        """

        if self.contract:
            try:
                contract_function = self.contract.get_function_by_name(func_name)
                output = contract_function(**kwargs).call()
                return output, ResponseStatus(ok=True)
            except ValueError as e:
                msg = f"function '{func_name}' not found in contract abi"
                return None, ResponseStatus(ok=False, error=e, error_msg=msg)
        else:
            if self.connect():
                msg = "now connected to contract"
                return self.read(func_name=func_name, **kwargs)
            else:
                msg = "unable to connect to contract"
                return None, ResponseStatus(ok=False, error_msg=msg)

    def write(
        self,
        func_name: str,
        extra_gas_price: int = 0,
        **kwargs: Any,
    ) -> Tuple[Optional[AttributeDict[Any, Any]], ResponseStatus]:
        """For submitting any contract transaction. Retries supported!"""
        if self.contract:
            try:
                status = ResponseStatus()

                # fetch gas price
                gas_price, gas_price_status = estimate_gas()

                # exit and report status if gas price couldn't be fetched
                if gas_price_status.ok is False:
                    status.error = "Can't submit transaction: couldn't fetch gas price"
                    status.ok = False
                    status.e = gas_price_status.e
                    return None, status

                # build transaction
                acc_nonce = self.config.get_endpoint().web3.eth.get_transaction_count(
                    self.config.acc.address
                )
                contract_function = self.contract.get_function_by_name(func_name)
                transaction = contract_function(**kwargs)
                estimated_gas = transaction.estimateGas()

                print("estimated gas:", estimated_gas)

                built_tx = transaction.buildTransaction(
                    {
                        "nonce": acc_nonce,
                        "gas": estimated_gas,
                        "gasPrice": self.config.get_endpoint().web3.toWei(
                            gas_price, "gwei"
                        ),
                        "chainId": self.config.get_endpoint().chain_id,
                    }
                )

                # submit transaction
                tx_signed = self.config.acc.address.sign_transaction(built_tx)

                tx_hash = self.config.get_endpoint().web3.eth.send_raw_transaction(
                    tx_signed.rawTransaction
                )

                # Confirm transaction
                tx_receipt = (
                    self.config.get_endpoint().web3.eth.wait_for_transaction_receipt(
                        tx_hash, timeout=360
                    )
                )

                # Point to relevant explorer
                print(
                    f"View reported data: {self.config.get_endpoint().explorer}{tx_hash.hex()}"
                )

                return tx_receipt, status
            except Exception as e:
                status.ok = False
                status.error = str(e.args)
                status.e = e
                return None, status
        else:
            if self.connect():
                msg = "now connected to contract"
                return self.write(
                    func_name=func_name,
                    extra_gas_price=extra_gas_price,
                    **kwargs,
                )
            else:
                msg = "unable to connect to contract"
                return None, ResponseStatus(ok=False, error_msg=msg)

    def write_with_retries(
        self,
        func_name: str,
        extra_gas_price: int,
        num_retries: int,
        **kwargs: Any,
    ) -> Tuple[Optional[List[AttributeDict[Any, Any]]], ResponseStatus]:

        status = ResponseStatus()

        # fetch gas price
        gas_price, gas_price_status = estimate_gas()

        # exit and report status if gas price couldn't be fetched
        if gas_price_status.ok is False:
            status.error = "Can't submit transaction: couldn't fetch gas price"
            status.ok = False
            status.e = gas_price_status.e
            return None, status

        tx_receipts: List[AttributeDict[Any, Any]] = []

        for _ in range(num_retries + 1):

            tx_receipt, status = self.write(
                func_name=func_name, extra_gas_price=extra_gas_price, kwargs=kwargs
            )

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

        return tx_receipts, status

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
