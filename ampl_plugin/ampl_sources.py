# import os
# import statistics
from typing import List
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import Union

import requests
from telliot.datafeed.data_source import DataSource
from telliot.types.datapoint import datetime_now_utc
from telliot.types.datapoint import OptionalDataPoint
from telliot.utils.response import ResponseStatus

# from telliot.datafeed.pricing.price_feed import PriceFeed
# from telliot.queries.coin_price import CoinPrice


class AMPLSource(DataSource):
    """Data source for retrieving AMPL/USD/VWAP."""

    async def fetch_new_datapoint(
        self,
        url: str,
        params: List[Union[str, int]],
        headers: Optional[Mapping[str, str]] = None,
    ) -> Tuple[OptionalDataPoint[float], ResponseStatus]:
        """Update current value with time-stamped value."""

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


class BraveNewCoinSource(AMPLSource):
    """Data source for retrieving AMPL/USD/VWAP from
    bravenewcoin api."""

    async def get_bearer_token(
        self, api_key: str
    ) -> Tuple[Optional[str], ResponseStatus]:
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
                    "x-rapidapi-key": api_key,
                }

                response = s.post(url, data=payload, headers=headers)

                bearer_token = response.json()["access_token"]

                return bearer_token, ResponseStatus()

            except requests.exceptions.ConnectTimeout as e:
                msg = "Timeout Error"
                return None, ResponseStatus(ok=False, error=msg, e=e)

            except Exception as e:
                return None, ResponseStatus(ok=False, error=str(type(e)), e=e)


# ampl_query = CoinPrice(coin="ampl", currency="usd", price_type="24hr_vwap")

# ampl_feed = PriceFeed(
#     query = ampl_query,
#     sources = {
#     "ampl-bravenewcoin": BraveNewCoinSource(),
#     "ampl-anyblock": AnyBlockSource()
#     },
#     asset = "ampl",
#     currency = "usd",
#     algorithm = statistics.median
# )

# run update value for ampl_feed at the needed interval
# subclass reporter for the ampl feed
