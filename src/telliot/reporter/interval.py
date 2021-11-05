""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio
from typing import Any, Optional, Tuple
from typing import List
from typing import Mapping
from typing import Union

from web3.datastructures import AttributeDict

from telliot.contract.contract import Contract
from telliot.contract.gas import fetch_gas_price
from telliot.datafeed import DataFeed
from telliot.model.endpoints import RPCEndpoint
from telliot.reporter.base import Reporter
from telliot.submitter.base import Submitter
from telliot.utils.abi import rinkeby_tellor_master
from telliot.utils.response import ResponseStatus


class IntervalReporter(Reporter):
    """Submits the price of BTC to the TellorX playground
    every 10 seconds."""

    def __init__(
        self,
        endpoint: RPCEndpoint,
        private_key: str,
        master: Contract,
        oracle: Contract,
        datafeeds: List[DataFeed[Any]],
    ) -> None:

        self.endpoint = endpoint
        self.datafeeds = datafeeds

        # self.submitter = Submitter(
        #     endpoint=self.endpoint,
        #     private_key=private_key,
        #     contract_address=contract_address,
        #     abi=rinkeby_tellor_master,
        # )

    async def report_once(
        self, name: str = "", retries: int = 0
    ) -> Tuple[Optional[List[AttributeDict[Any, Any]]], ResponseStatus]: #same output types as Contract.write_with_retry()
        """Submit value once"""

        status = ResponseStatus()
        gas_price_gwei = await fetch_gas_price()


        user = self.endpoint.web3.eth.account.from_key(self.private_key).address
        is_staked, read_status = await self.master.read("getStakerInfo", _staker=user)

        if not read_status.ok:
            status.error = "unable to read reporter staker status: " + read_status.error
            status.e = read_status.e
            return None, status

        if is_staked[0] == 3:
            status.error = f"you were disputed at {user}; to continue reporting, switch to new address"
            status.e = None
            return None, status

        elif is_staked[0] == 0:
            _, status = await self.master.write_with_retry(
                func_name="depositStake", gas_price=gas_price_gwei, extra_gas_price=20, retries=retries
            )
            if not read_status.ok:
                status.error = "unable to stake deposit: " + read_status.error
                status.e = read_status.e
                return None, status

        # transaction_receipts = []
        jobs = []
        for datafeed in self.datafeeds:
            job = asyncio.create_task(datafeed.source.fetch_new_datapoint())
            jobs.append(job)

        _ = await asyncio.gather(*jobs)

        for datafeed in self.datafeeds:

            datapoint = datafeed.source.latest
            v, t = datapoint

            if v is not None:
                query = datafeed.query

                if query:
                    encoded_value = query.value_type.encode(v)
                    request_id_str = "0x" + query.query_id.hex()
                    extra_gas_price = 0

                    gas_price_gwei = await fetch_gas_price()

                    balance, status = await self.master.read("balanceOf", _user=user)
                    print("your TRB balance: ", balance / 1e18)

                else:
                    print(
                        f"Skipping submission for {repr(datafeed)}, "
                        f"no query for datafeed."
                    )  # TODO logging
            else:
                print(
                    f"Skipping submission for {repr(datafeed)}, "
                    f"datafeed value not updated."
                )  # TODO logging

        return transaction_receipts

    async def report(self, name: str = "") -> None:
        """Update all off-chain values (BTC/USD) & store those values locally."""
        """Submit latest BTC/USD values to the Tellor oracle."""

        while True:
            _ = await self.report_once(name)
            await asyncio.sleep(10)

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
