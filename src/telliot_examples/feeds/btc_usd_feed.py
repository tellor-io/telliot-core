"""Example datafeeds used by BTCUSDReporter."""
import statistics

from telliot.datafeed.pricing.price_feed import PriceFeed
from telliot.datafeed.pricing.price_source import PriceSource
from telliot.queries.coin_price import CoinPrice
from telliot_examples.coinprices.bittrex import BittrexPriceService
from telliot_examples.coinprices.coinbase import CoinbasePriceService
from telliot_examples.coinprices.coingecko import CoinGeckoPriceService
from telliot_examples.coinprices.gemini import GeminiPriceService

data_sources = {
    "btc-usd-coinbase": PriceSource(
        name="BTC USD Price from Coinbase",
        uid="btc-usd-coinbase",
        asset="btc",
        currency="usd",
        service=CoinbasePriceService(),
    ),
    "btc-usd-coingecko": PriceSource(
        name="BTC USD Price from Coinbase",
        uid="btc-usd-coinbase",
        asset="btc",
        currency="usd",
        service=CoinGeckoPriceService(),
    ),
    "btc-usd-bittrex": PriceSource(
        name="BTC USD Price from Bittrex",
        uid="btc-usd-bittrex",
        asset="btc",
        currency="usd",
        service=BittrexPriceService(),
    ),
    "btc-usd-gemini": PriceSource(
        name="BTC USD Price from Gemini",
        uid="btc-usd-gemini",
        asset="btc",
        currency="usd",
        service=GeminiPriceService(),
    ),
}

target_query = CoinPrice(coin="btc", currency="usd", price_type="current")

data_feeds = {
    "btc-usd-median": PriceFeed(
        name="BTC USD Median Price Feed",
        uid="btc-usd-median",
        query=target_query,
        asset="btc",
        currency="usd",
        sources=data_sources,
        algorithm=statistics.median,
    )
}
