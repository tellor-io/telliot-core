"""Example datafeeds used by BTCUSDReporter."""
import statistics

from telliot.datafeed.asset_price_feed import AssetPriceFeed
from telliot.datafeed.asset_price_source import AssetPriceSource
from telliot.pricing.bittrex import BittrexPriceService
from telliot.pricing.coinbase import CoinbasePriceService
from telliot.pricing.coingecko import CoinGeckoPriceService
from telliot.pricing.gemini import GeminiPriceService
from telliot.queries.price_query import PriceQuery

data_sources = {
    "btc-usd-coinbase": AssetPriceSource(
        name="BTC USD Price from Coinbase",
        uid="btc-usd-coinbase",
        asset="btc",
        currency="usd",
        service=CoinbasePriceService(),
    ),
    "btc-usd-coingecko": AssetPriceSource(
        name="BTC USD Price from Coinbase",
        uid="btc-usd-coinbase",
        asset="btc",
        currency="usd",
        service=CoinGeckoPriceService(),
    ),
    "btc-usd-bittrex": AssetPriceSource(
        name="BTC USD Price from Bittrex",
        uid="btc-usd-bittrex",
        asset="btc",
        currency="usd",
        service=BittrexPriceService(),
    ),
    "btc-usd-gemini": AssetPriceSource(
        name="BTC USD Price from Gemini",
        uid="btc-usd-gemini",
        asset="btc",
        currency="usd",
        service=GeminiPriceService(),
    ),
}

target_query = PriceQuery(asset='btc', currency='usd', price_type='current')

data_feeds = {
    "btc-usd-median": AssetPriceFeed(
        name="BTC USD Median Price Feed",
        uid="btc-usd-median",
        query=target_query,
        asset="btc",
        currency="usd",
        sources=data_sources,
        algorithm=statistics.median,
    )

}

pass
