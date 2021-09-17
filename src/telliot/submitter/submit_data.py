""" Submit Data

This module's purpose is to submit off-chain data on-chain.
"""

from typing import Dict
from web3 import Web3

from telliot.datafeed.data_feed import DataFeed
from telliot.utils import TelliotUtils

w3 = Web3(Web3.HTTPProvider("https://eth-rinkeby.gateway.pokt.network/v1/lb/612e6d5cdc57c500365435bc"))
mesosphere = w3.eth.contract("0x33A9e116C4E78c5294d82Af7e0313E10E0a4B027", abi=open("abi.json").read())

def submit_data(datafeed:DataFeed):
    """Submit data collected from APIs to Tellor. Converts DataFeed's request_id and value into bytes for contract."""


    #build transaction
    tx = build_tx()

    #send raw transaction

    #await transaction receipt

    #TODO add logging

def build_tx(
        asset: DataFeed,
        acc_nonce: int,
        new_gas_price: str,
    ) -> Dict:

        #convert request_id and value to bytes from str (use Web3.toBytes?)
        request_id = TelliotUtils.to_bytes32(asset.request_id)
        value = TelliotUtils.to_bytes(asset.value.val)

        transaction = mesosphere.functions.submitValue(
            request_id, value
        ).buildTransaction(
            {
                "nonce": acc_nonce,
                "gas": 4000000,
                "gasPrice": w3.toWei(new_gas_price, "gwei"),
                "chainId": 4, #rinkeby
            }
        )

        return transaction