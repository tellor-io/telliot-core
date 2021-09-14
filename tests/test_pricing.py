from datetime import datetime

import pytest
from telliot.pricing.bittrex import BittrexPriceService
from telliot.pricing.coinbase import CoinbasePriceService
from telliot.pricing.coingecko import CoinGeckoPriceService

service = {
    "coinbase": CoinbasePriceService(),
    "coingecko": CoinGeckoPriceService(),
    "bittrex": BittrexPriceService(),
}


async def get_price(asset, currency, service):
    price = await service.get_price(asset, currency)
    return price


def validate_price(price):
    assert price is not None
    assert isinstance(price.val, float)
    assert price.val > 0
    assert isinstance(price.ts, datetime)
    print(price)


@pytest.mark.asyncio
async def test_coinbase():
    price = await get_price("btc", "usd", service["coinbase"])
    validate_price(price)


@pytest.mark.asyncio
async def test_coingecko():
    price = await get_price("btc", "usd", service["coingecko"])
    validate_price(price)


@pytest.mark.asyncio
async def test_bittrex():
    price = await get_price("btc", "usd", service["bittrex"])
    validate_price(price)


# def test_web_price_service_timeout():
#     ps = CoinbasePriceService(timeout=0.0000001)
#     result = ps.get_url()
#     assert result["error"] == "Timeout Error"
