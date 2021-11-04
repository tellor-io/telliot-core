"""Example datafeeds used by BTCUSDReporter."""
from telliot.data_feed import DataFeed
from telliot.queries.coin_price import CoinPrice

from telliot_feed_examples.sources.bittrex import BittrexPriceSource
from telliot_feed_examples.sources.coinbase import CoinbasePriceSource
from telliot_feed_examples.sources.coingecko import CoinGeckoPriceSource
from telliot_feed_examples.sources.gemini import GeminiPriceSource
from telliot_feed_examples.sources.price_aggregator import PriceAggregator

data_sources = [
    CoinbasePriceSource(
        asset="btc",
        currency="usd",
    ),
    CoinGeckoPriceSource(asset="btc", currency="usd"),
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
        sources=data_sources, asset="btc", currency="usd", algorithm="median"
    ),
)
