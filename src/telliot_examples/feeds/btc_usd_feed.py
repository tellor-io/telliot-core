"""Example datafeeds used by BTCUSDReporter."""

from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.pricing.price_aggregator import PriceAggregator
from telliot.queries.coin_price import CoinPrice
from telliot_examples.coinprices.bittrex import BittrexPriceSource
from telliot_examples.coinprices.coinbase import CoinbasePriceSource
from telliot_examples.coinprices.coingecko import CoinGeckoPriceSource
from telliot_examples.coinprices.gemini import GeminiPriceSource

data_sources = [
    CoinbasePriceSource(
        asset="btc",
        currency="usd",
    ),
    CoinGeckoPriceSource(
        asset="btc",
        currency="usd"),
    BittrexPriceSource(
        asset="btc",
        currency="usd",
    ),
    GeminiPriceSource(
        asset="btc",
        currency="usd",
    ),
]

target_query = CoinPrice(coin="btc", currency="usd", price_type="current")

btc_usd_median_feed = DataFeed(
    query=CoinPrice(coin="btc", currency="usd", price_type="current"),
    source=PriceAggregator(
        sources=data_sources, asset="btc", currency="usd", algorithm='median'
    ),
)

import json
state = btc_usd_median_feed.get_state()
print(state)
print(json.dumps(state, indent=2))
