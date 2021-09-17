""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio

import requests

from .registry import data_feeds
from .reporter import Reporter


class BTCReporter(Reporter):
    """
    Runs datafeed server as a background task. Populates
    local database with BTC/USD price data every 10 seconds.
    Submits stored data to Tellor Oracle every 15 seconds.
    """

    # async def update_datafeeds(self) -> None:
    #     """Update all off-chain values (BTC/USD) & store those values locally."""
    #     while True:
    #         jobs = []
    #         for datafeed in self.datafeeds.values():
    #             job = asyncio.create_task(datafeed.update_value(store=True))
    #             jobs.append(job)

    #         _ = await asyncio.gather(*jobs)

    #         print("Updated & stored registry data")
    #         await asyncio.sleep(10)

    async def submit_data(self) -> None:
        """Submit latest BTC/USD values to the Tellor oracle."""
        while True:
            await asyncio.sleep(15)

            for datafeed in self.datafeeds:
                try:
                    uid = datafeed
                    # url = f"http://127.0.0.1:8000/data/latest/?uid={uid}"
                    # val = requests.get(url).json()["value"]

                    # TODO: finish basic submitter & datafeed submit
                    # method (uses submitter.submit_data module)
                    print(f"Submitted value for {datafeed}:")

                    #call submitter

                except Exception as e:
                    print("Error submitting:", e)

    def run(self) -> None:  # type: ignore
        """Used by telliot CLI to update & submit BTC/USD price data to Tellor Oracle."""
        # self.database.start()

        # Create coroutines to run concurrently.
        loop = asyncio.get_event_loop()
        # _ = loop.create_task(self.update_datafeeds())
        _ = loop.create_task(self.submit_data())

        # Blocking loop.
        try:
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            # self.database.terminate()
            loop.close()


btc_reporter = BTCReporter(data_feeds)
