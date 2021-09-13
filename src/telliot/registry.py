import statistics

from telliot.datafeed.data_feed import AssetPriceFeed
from telliot.datafeed.data_source import AssetPriceSource
from telliot.pricing.coinbase import CoinbasePriceService
from telliot.pricing.coingecko import CoinGeckoPriceService

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
}

data_feeds = {
    "btc-usd-median": AssetPriceFeed(
        name="BTC USD Median Price Feed",
        uid="btc-usd-median",
        asset="btc",
        currency="usd",
        sources=data_sources,
        algorithm=statistics.median,
    )
}
