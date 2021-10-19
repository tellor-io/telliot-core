""" Submit Data

This module's provides a base Submitter class to be subclassed
in the `reporter_plugins` module. Submitters submit off-chain data on-chain
to the Tellor oracle.
"""
import json
from abc import ABC
from typing import Any
from typing import Mapping
from typing import Sequence

import requests
from telliot.utils.abi import tellor_playground_abi
from telliot.model.endpoints import RPCEndpoint



class Submitter(ABC):
    """Submits BTC on testnet.

    Submits BTC price data in USD to the TellorX playground
    on the Rinkeby test network."""

    def __init__(
        self,
        endpoint: RPCEndpoint,
        private_key: str,
        contract_address: str,
        abi: Sequence[Mapping[str, Any]],
    ) -> None:
        """Reads user private key and node endpoint from `.env` file to
        set up `Web3` client for interacting with the TellorX playground
        smart contract."""

        self.endpoint = endpoint
        self.private_key = private_key
        self.contract_address = contract_address

        self.endpoint.connect()

        self.acc = self.endpoint.web3.eth.account.from_key(self.private_key)

        self.contract = self.endpoint.web3.eth.contract(
            self.contract_address, abi=tellor_playground_abi
        )

    def build_tx(self, value: bytes, request_id: str, gas_price: str) -> Any:
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

    def submit_data(self, value: bytes, request_id: str) -> Any:
        """Submits data on-chain & provides a link to view the
        successful transaction."""

        req = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
        prices = json.loads(req.content)
        gas_price = str(prices["fast"])
        print("retrieved gas price:", gas_price)
        # gas_price = "3"
        # print("gas price used:", gas_price)

        tx = self.build_tx(value, request_id, gas_price)

        tx_signed = self.acc.sign_transaction(tx)

        tx_hash = self.endpoint.web3.eth.send_raw_transaction(tx_signed.rawTransaction)

        tx_receipt = self.endpoint.web3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=360
        )
        print(f"View reported data: https://rinkeby.etherscan.io/tx/{tx_hash.hex()}")

        return tx_receipt
