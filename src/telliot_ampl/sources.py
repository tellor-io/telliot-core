import asyncio
import statistics
from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional
from typing import Tuple
from typing import TypeVar

import requests
from telliot.datasource import DataSource
from telliot.types.datapoint import datetime_now_utc
from telliot.types.datapoint import OptionalDataPoint
from telliot.utils.response import ResponseStatus

from telliot_ampl.config import AMPLConfig


T = TypeVar("T")


@dataclass
class AMPLSource(DataSource):
    """Base AMPL datasource."""

    async def get_float_from_api(self, url: str, params, headers=None):
        """Helper function for retrieving datapoint values."""

        with requests.Session() as s:
            try:
                r = None
                if headers:
                    r = s.get(url, headers=headers)
                else:
                    r = s.get(url)
                data = r.json()

                for param in params:
                    data = data[param]

                timestamp = datetime_now_utc()
                datapoint = (data, timestamp)
                self.store_datapoint(datapoint)

                return datapoint, ResponseStatus()

            except requests.exceptions.ConnectTimeout as e:
                msg = "Timeout Error"
                return (None, None), ResponseStatus(ok=False, error=msg, e=e)

            except Exception as e:
                return (None, None), ResponseStatus(ok=False, error=str(type(e)), e=e)


@dataclass
class AnyBlockSource(AMPLSource):
    """Data source for retrieving AMPL/USD/VWAP from AnyBlock api."""

    api_key: str = ""

    async def fetch_new_datapoint(
        self,
    ) -> Tuple[OptionalDataPoint[float], ResponseStatus]:
        """Update current value with time-stamped value."""

        url = (
            "https://api.anyblock.tools/market/AMPL_USD_via_ALL/daily-volume"
            + "?roundDay=false&debug=false&access_token="
            + self.api_key
        )
        params = ["overallVWAP"]

        return await self.get_float_from_api(url, params)


@dataclass
class BraveNewCoinSource(AMPLSource):
    """Data source for retrieving AMPL/USD/VWAP from
    bravenewcoin api."""

    api_key: str = ""

    async def get_bearer_token(self) -> Tuple[Optional[str], ResponseStatus]:
        """Get authorization token for using bravenewcoin api."""

        with requests.Session() as s:
            try:
                url = "https://bravenewcoin.p.rapidapi.com/oauth/token"

                payload = """{\r
                    \"audience\": \"https://api.bravenewcoin.com\",\r
                    \"client_id\": \"oCdQoZoI96ERE9HY3sQ7JmbACfBf55RY\",\r
                    \"grant_type\": \"client_credentials\"\r
                }"""
                headers = {
                    "content-type": "application/json",
                    "x-rapidapi-host": "bravenewcoin.p.rapidapi.com",
                    "x-rapidapi-key": self.api_key,
                }

                response = s.post(url, data=payload, headers=headers)

                bearer_token = response.json()["access_token"]

                return bearer_token, ResponseStatus()

            except requests.exceptions.ConnectTimeout as e:
                msg = "Timeout Error"
                return None, ResponseStatus(ok=False, error=msg, e=e)

            except Exception as e:
                return None, ResponseStatus(ok=False, error=str(type(e)), e=e)

    async def fetch_new_datapoint(
        self,
    ) -> Tuple[OptionalDataPoint[float], ResponseStatus]:
        """Update current value with time-stamped value."""

        access_token, status = await self.get_bearer_token()

        if not status.ok:
            return (None, None), status

        url = (
            "https://bravenewcoin.p.rapidapi.com/ohlcv?"
            + "size=1&indexId=551cdbbe-2a97-4af8-b6bc-3254210ed021&indexType=GWA"
        )
        params = ["content", 0, "vwap"]

        headers = {
            "authorization": f"Bearer {access_token}",
            "x-rapidapi-host": "bravenewcoin.p.rapidapi.com",
            "x-rapidapi-key": self.api_key,
        }

        return await self.get_float_from_api(url, params, headers)


@dataclass
class AMPLUSDVWAPSource(DataSource[float], ABC):
    #: Asset
    asset: str = "ampl"

    #: Currency of returned price
    currency: str = "usd"

    #: Access tokens for apis
    cfg: AMPLConfig = field(default_factory=AMPLConfig)

    #: Data sources
    sources: List[AMPLSource] = field(default_factory=list)

    def __post_init__(self):
        self.sources = [
            AnyBlockSource(api_key=self.cfg.main.anyblock_api_key),
            BraveNewCoinSource(api_key=self.cfg.main.rapid_api_key),
        ]

    async def update_sources(self) -> List[OptionalDataPoint[float]]:
        """Update data feed sources

        Returns:
            Dictionary of updated source values, mapping data source UID
            to the time-stamped answer for that data source
        """

        async def gather_inputs() -> List[OptionalDataPoint[float]]:
            sources = self.sources
            datapoints = await asyncio.gather(
                *[source.fetch_new_datapoint() for source in sources]
            )
            return datapoints

        inputs = await gather_inputs()

        return inputs

    async def fetch_new_datapoint(self) -> OptionalDataPoint[float]:
        """Update current value with time-stamped value fetched from source

        Args:
            store:  If true and applicable, updated value will be stored
                    to the database

        Returns:
            Current time-stamped value
        """
        updates = await self.update_sources()

        # Keep datapoints with good response statuses
        datapoints = [update[0] for update in updates if update[1].ok]

        prices = []
        for datapoint in datapoints:
            v, _ = datapoint  # Ignore input timestamps
            # Check for valid answers
            if v is not None:
                prices.append(v)

        # Get median price
        result = statistics.median(prices)
        datapoint = (result, datetime_now_utc())
        self.store_datapoint(datapoint)

        print(
            "AMPL/USD/VWAP {} retrieved at time {}".format(datapoint[0], datapoint[1])
        )

        return datapoint