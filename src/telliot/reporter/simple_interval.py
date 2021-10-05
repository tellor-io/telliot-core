""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio
from typing import Mapping

from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.example import data_feeds
from telliot.reporter.base import Reporter
from telliot.reporter.config import ReporterConfig
from telliot.submitter.base import Submitter
from telliot.utils.abi import tellor_playground_abi


class IntervalReporter(Reporter):
    """Submits the price of BTC to the TellorX playground
    every 10 seconds."""

    def __init__(
        self, config: ReporterConfig, datafeeds: Mapping[str, DataFeed]
    ) -> None:
        self.config = config
        self.datafeeds = datafeeds
        self.submitter = Submitter(self.config, tellor_playground_abi)

    async def report(self) -> None:
        """Update all off-chain values (BTC/USD) & store those values locally."""
        """Submit latest BTC/USD values to the Tellor oracle."""

        while True:
            jobs = []
            for datafeed in self.datafeeds.values():
                job = asyncio.create_task(datafeed.update_value(store=True))
                jobs.append(job)

            _ = await asyncio.gather(*jobs)

            for uid, datafeed in self.datafeeds.items():
                if datafeed.value:
                    print(f"Submitting value for {uid}: float {datafeed.value.val} int {datafeed.value.int}")
                    query = datafeed.get_query()
                    if query is not None:
                        encoded_value = query.response_type.encode(datafeed.value.int)
                        request_id_str = "0x" + query.request_id.hex()
                        self.submitter.submit_data(encoded_value, request_id_str)
                    else:
                        print(f"Skipping submission for {uid}, no query for datafeed.")
                else:
                    print(f"Skipping submission for {uid}, datafeed value not updated.")

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


reporter = IntervalReporter(
    config=ReporterConfig.from_file("/home/oraclown/telliot/reporter.yaml"),
    datafeeds=data_feeds,
)

reporter.run()
