""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio
from typing import Any
from typing import List
from typing import Mapping
from typing import Union

from telliot.reporter.base import Reporter
from telliot.submitter.base import Submitter
from telliot.utils.abi import tellor_playground_abi
from telliot.model.endpoints import RPCEndpoint


class IntervalReporter(Reporter):
    """Submits the price of BTC to the TellorX playground
    every 10 seconds."""

    def __init__(
            self,
            endpoint: RPCEndpoint,
            private_key: str,
            contract_address: str,
            datafeeds: Mapping[str, Any]
    ) -> None:

        self.endpoint = endpoint
        self.datafeeds = datafeeds

        self.submitter = Submitter(endpoint=self.endpoint,
                                   private_key=private_key,
                                   contract_address=contract_address,
                                   abi=tellor_playground_abi)

    async def report_once(self, name: str = "") -> List[Union[None, Mapping[str, Any]]]:
        transaction_receipts = []
        jobs = []
        for datafeed in self.datafeeds.values():
            job = asyncio.create_task(datafeed.update_value(store=True))
            jobs.append(job)

        _ = await asyncio.gather(*jobs)

        for uid, datafeed in self.datafeeds.items():
            if name and name != datafeed.name:
                continue

            if datafeed.value:
                print(
                    f"""
                    Submitting value for {uid}:
                        float {datafeed.value.val}
                        int {datafeed.value.int}"""
                )
                query = datafeed.query
                if query is not None:
                    encoded_value = query.value_type.encode(datafeed.value.int)
                    request_id_str = "0x" + query.tip_id.hex()
                    transaction_receipt = self.submitter.submit_data(
                        encoded_value, request_id_str
                    )
                    transaction_receipts.append(transaction_receipt)
                else:
                    print(f"Skipping submission for {uid}, no query for datafeed.")
            else:
                print(f"Skipping submission for {uid}, datafeed value not updated.")
        return transaction_receipts

    async def report(self) -> None:
        """Update all off-chain values (BTC/USD) & store those values locally."""
        """Submit latest BTC/USD values to the Tellor oracle."""

        while True:
            _ = await self.report_once()
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
