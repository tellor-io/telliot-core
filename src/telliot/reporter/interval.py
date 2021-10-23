""" BTCUSD Price Reporter

Example of a subclassed Reporter.
"""
import asyncio
from typing import Any
from typing import List
from typing import Mapping
from typing import Union

from telliot.apps.telliot_config import TelliotConfig
from telliot.contract.contract import Contract
from telliot.model.endpoints import RPCEndpoint
from telliot.reporter.base import Reporter
from telliot.submitter.base import Submitter
from telliot.utils.abi import tellor_playground_abi


class IntervalReporter(Reporter):
    """Submits the price of BTC to the TellorX playground
    every 10 seconds."""

    contract: Contract

    config: TelliotConfig

    datafeeds: Mapping[str, Any]

    # def __init__(
    #     self,
    #     endpoint: RPCEndpoint,
    #     private_key: str,
    #     contract_address: str,
    #     datafeeds: Mapping[str, Any],
    # ) -> None:

    #     self.endpoint = endpoint
    #     self.datafeeds = datafeeds

    #     self.submitter = Submitter(
    #         endpoint=self.endpoint,
    #         private_key=private_key,
    #         contract_address=contract_address,
    #         abi=tellor_playground_abi,
    #     )

    async def report_once(
        self, name: str = "", num_retries: int = 0
    ) -> List[Union[None, Mapping[str, Any]]]:
        transaction_receipts: List[Union[None, Mapping[str, Any]]] = []
        jobs = []
        for datafeed in self.datafeeds.values():
            job = asyncio.create_task(datafeed.update_value(store=True))
            jobs.append(job)

        _ = await asyncio.gather(*jobs)

        for uid, datafeed in self.datafeeds.items():
            if name and name != datafeed.name:
                continue

            if datafeed.value:
                query = datafeed.query

                if query:
                    encoded_value = query.value_type.encode(datafeed.value.int)
                    query_id_str = "0x" + query.tip_id.hex()
                    extra_gas_price = 0
                    value_count = self.contract.read(
                        "getNewValueCountbyRequestId", _requestId=query_id_str
                    )

                    self.contract.write_with_retries(
                        func_name="submitValue",
                        num_retries=num_retries,
                        extra_gas_price=extra_gas_price,
                        _requestId=query_id_str,
                        _value=encoded_value,
                        _nonce=value_count,
                    )

                else:
                    print(
                        f"Skipping submission for {uid}, no query for datafeed."
                    )  # TODO logging
            else:
                print(
                    f"Skipping submission for {uid}, datafeed value not updated."
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
