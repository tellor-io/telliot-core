"""
Utils for connecting to an EVM contract
"""
from typing import Any, Tuple
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import web3
import requests
import json
from eth_typing.evm import ChecksumAddress
from telliot.apps.telliot_config import TelliotConfig
from telliot.utils.base import Base
from telliot.utils.response import ContractResponse, ResponseStatus
from web3 import Web3


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

    def connect(self) -> ContractResponse:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3 is None:
            msg = "node is not instantiated"
            return ContractResponse(ok=False, error_msg=msg)
        else:
            if not self.node.connect():
                msg = "node is not connected"
                return ContractResponse(ok=False, error_msg=msg, endpoint=self.node)
            self.address = Web3.toChecksumAddress(self.address)
            self.contract = self.config.default_endpoint.web3.eth.contract(
                address=self.address, abi=self.abi
            )
            return ContractResponse(ok=True, endpoint=self.node)

    def read(self, func_name: str, **kwargs: Any) -> ContractResponse:
        """
        Reads data from contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        ContractResponse: standard response for contract data
        """

        if self.contract:
            try:
                contract_function = self.contract.get_function_by_name(func_name)
                output = contract_function(**kwargs).call()
                return ContractResponse(ok=True, result=output)
            except ValueError as e:
                msg = f"function '{func_name}' not found in contract abi"
                return ContractResponse(
                    ok=False, error=e, error_msg=msg, endpoint=self.node
                )
        else:
            if self.connect():
                msg = "now connected to contract"
                return self.read(func_name=func_name, **kwargs)
            else:
                msg = "unable to connect to contract"
                return ContractResponse(ok=False, error_msg=msg, endpoint=self.node)

    # def write(self, func_name: str, **kwargs: Any) -> bool:
    def __build_tx(self, value: bytes, request_id: str, gas_price: str) -> Any:
        """Assembles needed transaction data."""

        nonce = self.contract.functions.getNewValueCountbyRequestId(request_id).call()

        print("nonce:", nonce)

        acc_nonce = self.endpoint.web3.eth.get_transaction_count(self.acc.address)

        transaction = self.contract.functions.submitValue(request_id, value, nonce)

        estimated_gas = transaction.estimateGas()
        print("estimated gas:", estimated_gas)

        built_tx = transaction.buildTransaction(
            {
                "nonce": acc_nonce,
                "gas": estimated_gas,
                "gasPrice": self.endpoint.web3.toWei(gas_price, "gwei"),
                "chainId": self.endpoint.chain_id,
            }
        )

        return built_tx

    def __submit_data(
        self, value: bytes, request_id: str, extra_gas_price: int = 0
    ) -> Tuple[ResponseStatus, Any, int]:
        """Submits data on-chain & provides a link to view the
        successful transaction."""
        try:
            status = ResponseStatus()

            rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
            prices = json.loads(rsp.content)
            gas_price = int(prices["fast"] + extra_gas_price)

            tx = self.build_tx(value, request_id, str(gas_price))

            tx_signed = self.acc.sign_transaction(tx)

            tx_hash = self.endpoint.web3.eth.send_raw_transaction(
                tx_signed.rawTransaction
            )

            tx_receipt = self.endpoint.web3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=360
            )
            print(
                f"View reported data: https://rinkeby.etherscan.io/tx/{tx_hash.hex()}"
            )

            return status, tx_receipt, gas_price

        except Exception as e:
            status.ok = False
            status.error = str(e.args)
            status.e = e
            return status, None, gas_price

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
