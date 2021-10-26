""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio
from typing import Any
from typing import List
from typing import Mapping
from typing import Union

from telliot.model.endpoints import RPCEndpoint
from telliot.reporter.base import Reporter
from telliot.submitter.base import Submitter
from telliot.utils.abi import tellor_playground_abi
from telliot.datafeed.data_feed import DataFeed

class IntervalReporter(Reporter):
    """Submits the price of BTC to the TellorX playground
    every 10 seconds."""

    def __init__(
        self,
        endpoint: RPCEndpoint,
        private_key: str,
        contract_address: str,
        datafeeds: List[DataFeed],
    ) -> None:

        self.endpoint = endpoint
        self.datafeeds = datafeeds

        self.submitter = Submitter(
            endpoint=self.endpoint,
            private_key=private_key,
            contract_address=contract_address,
            abi=tellor_playground_abi,
        )

    async def report_once(
        self, name: str = "", retries: int = 0
    ) -> List[Union[None, Mapping[str, Any]]]:
        transaction_receipts = []
        jobs = []
        for datafeed in self.datafeeds:
            job = asyncio.create_task(datafeed.update_value())
            jobs.append(job)

        _ = await asyncio.gather(*jobs)

        for datafeed in self.datafeeds:

            if datafeed.value:
                query = datafeed.query

                if query:
                    encoded_value = query.value_type.encode(datafeed.value.int)
                    request_id_str = "0x" + query.query_id.hex()
                    extra_gas_price = 0

                    for _ in range(retries + 1):
                        (
                            status,
                            transaction_receipt,
                            gas_price,
                        ) = self.submitter.submit_data(
                            encoded_value, request_id_str, extra_gas_price
                        )

                        if transaction_receipt and status.ok:
                            transaction_receipts.append(transaction_receipt)
                            break
                        elif (
                            not status.ok
                            and status.error
                            and "replacement transaction underpriced" in status.error
                        ):
                            extra_gas_price += gas_price
                        else:
                            extra_gas_price = 0

                else:
                    print(
                        f"Skipping submission for {repr(datafeed)}, no query for datafeed."
                    )  # TODO logging
            else:
                print(
                    f"Skipping submission for {repr(datafeed)}, datafeed value not updated."
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
