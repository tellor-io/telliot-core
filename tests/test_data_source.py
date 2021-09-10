import asyncio

from telliot.datafeed.data_source import CurrentAssetPrice
from telliot.pricing.coinbase import CoinbasePriceService
from telliot.pricing.coingecko import CoinGeckoPriceService


def test_asset_price_data_source():
    ds = CurrentAssetPrice(
        id="btc-usd-price-list",
        asset="btc",
        currency="usd",
        services=[CoinbasePriceService, CoinGeckoPriceService],
    )

    prices1 = asyncio.run(ds.fetch())
    prices2 = asyncio.run(ds.fetch())
    assert abs(prices1[0] - prices1[1]) / prices1[0] < 0.05
    assert len(ds.values) == 2
