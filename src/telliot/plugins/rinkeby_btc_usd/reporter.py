""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio

from multiprocessing import Process
from typing import Any
from typing import Dict

import uvicorn  # type: ignore

import requests
import os

from dotenv import find_dotenv
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

from telliot.plugins.rinkeby_btc_usd.datafeeds import btc_usd_data_feeds
from telliot.reporter_base import Reporter
from telliot.plugins.rinkeby_btc_usd.abi import tellorX_playground_abi
from telliot.submitter.submitter_base import Submitter

load_dotenv()


class RinkebySubmitter(Submitter):
    """
    """

    def __init__(self) -> None:
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("NODE_URL")))
        self.acc = self.w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

        self.playground = self.w3.eth.contract(
            "0x33A9e116C4E78c5294d82Af7e0313E10E0a4B027", 
            abi=tellorX_playground_abi
            )

    def tobytes32(self, x):
        return bytes(x, "ascii")


    def tobytes(self, x):
        return Web3.toBytes(hexstr=Web3.toHex(text=str(x)))


    def build_tx(self, value, request_id):
        request_id = self.tobytes32(request_id)
        value = self.tobytes(int(value * 1e6))
        nonce = self.playground.functions.getNewValueCountbyRequestId(request_id).call()

        print('nonce', nonce)

        acc_nonce = self.w3.eth.get_transaction_count(self.acc.address)

        transaction = self.playground.functions.submitValue(
            request_id, value, nonce
        ).buildTransaction(
            {
                "nonce": acc_nonce,
                "gas": 4000000,
                "gasPrice": self.w3.toWei("3", "gwei"),
                "chainId": 4, #rinkeby
            }
        )

        return transaction


    def submit_data(self, value, request_id):
        tx = self.build_tx(value, request_id)

        tx_signed = (
            self.acc.sign_transaction(tx)
        )

        tx_hash = self.w3.eth.send_raw_transaction(
            tx_signed.rawTransaction
        )
        
        _ = self.w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=360
        )
        print(f'View reported data: https://rinkeby.etherscan.io/tx/{tx_hash.hex()}')



class BTCUSDReporter(Reporter):
    """
    Runs datafeed server as a background task. Populates
    local database with BTC/USD price data every 10 seconds.
    Submits stored data to Tellor Oracle every 15 seconds.
    """

    def __init__(self) -> None:
        self.submitter = RinkebySubmitter()
        self.datafeeds = btc_usd_data_feeds

    async def report(self) -> None:
        """Update all off-chain values (BTC/USD) & store those values locally."""
        """Submit latest BTC/USD values to the Tellor oracle."""

        while True:
            jobs = []
            for uid, datafeed in self.datafeeds.items():
                job = asyncio.create_task(datafeed.update_value(store=True))
                jobs.append(job)

            _ = await asyncio.gather(*jobs)

            print(f'Submitting value for {uid}: {datafeed.value.val}')
            self.submitter.submit_data(
                datafeed.value.val, 
                datafeed.request_id)

            await asyncio.sleep(3)

    def run(self) -> None:  # type: ignore
        """Used by telliot CLI to update & submit BTC/USD price data to Tellor Oracle."""

        # Create coroutines to run concurrently.
        loop = asyncio.get_event_loop()
        _ = loop.create_task(self.report())

        # Blocking loop.
        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            loop.close()


btc_usd_reporter = BTCUSDReporter()
