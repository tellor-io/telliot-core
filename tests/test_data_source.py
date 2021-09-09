import asyncio

from telliot.datafeed.data_source import WebJsonPriceApi


def test_web_json_price_api():

    ds1 = WebJsonPriceApi(
        name="Coinbase BTCUSD Price",
        asset_id="BTCUSD",
        id="btc-usd-coinbase",
        url="https://api.pro.coinbase.com/products/BTC-USD/ticker",
        keywords=["price"],
    )

    p = asyncio.run(ds1.fetch())
    assert isinstance(p, float)
    print("{} price according to {} = {}".format(ds1.asset_id, ds1.name, p))

    ds1.url = "https://mgjvbe6hdns.com/asdfgrfde"
    p = asyncio.run(ds1.fetch())
    assert p is None
