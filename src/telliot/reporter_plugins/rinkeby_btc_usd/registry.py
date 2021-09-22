"""Example datafeeds used by BTCUSDReporter."""
import statistics

from telliot.datafeed.asset_price_feed import AssetPriceFeed
from telliot.datafeed.asset_price_source import AssetPriceSource
from telliot.reporter_plugins.rinkeby_btc_usd.datafeed_utils.bittrex import (
    BittrexPriceService,
)
from telliot.reporter_plugins.rinkeby_btc_usd.datafeed_utils.coinbase import (
    CoinbasePriceService,
)
from telliot.reporter_plugins.rinkeby_btc_usd.datafeed_utils.coingecko import (
    CoinGeckoPriceService,
)
from telliot.reporter_plugins.rinkeby_btc_usd.datafeed_utils.gemini import (
    GeminiPriceService,
)

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

btc_usd_data_feeds = {
    "btc-usd-median": AssetPriceFeed(
        name="BTC USD Median Price Feed",
        uid="btc-usd-median",
        request_id="btc-usd-median",
        asset="btc",
        currency="usd",
        sources=data_sources,
        algorithm=statistics.median,
    )
}
