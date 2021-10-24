""" Unit tests for pricing module

"""
from datetime import datetime

import pytest
from telliot_examples.coinprices.bittrex import BittrexPriceService
from telliot_examples.coinprices.coinbase import CoinbasePriceService
from telliot_examples.coinprices.coingecko import CoinGeckoPriceService
from telliot_examples.coinprices.gemini import GeminiPriceService

service = {
    "coinbase": CoinbasePriceService(),
    "coingecko": CoinGeckoPriceService(),
    "bittrex": BittrexPriceService(),
    "gemini": GeminiPriceService(),
}


async def get_price(asset, currency, service):
    """Helper function for retrieving prices."""
    price = await service.get_price(asset, currency)
    return price


def validate_price(price):
    """Check types and price anomalies."""
    assert price is not None
    assert isinstance(price.val, float)
    assert price.val > 0
    assert isinstance(price.ts, datetime)
    print(price)


@pytest.mark.asyncio
async def test_coinbase():
    """Test retrieving from Coinbase price source."""
    price = await get_price("btc", "usd", service["coinbase"])
    validate_price(price)


@pytest.mark.asyncio
async def test_coingecko():
    """Test retrieving from Coingecko price source."""
    price = await get_price("btc", "usd", service["coingecko"])
    validate_price(price)


@pytest.mark.asyncio
async def test_bittrex():
    """Test retrieving from Bittrex price source."""
    price = await get_price("btc", "usd", service["bittrex"])
    validate_price(price)


@pytest.mark.asyncio
async def test_gemini():
    """Test retrieving from Gemini price source."""
    price = await get_price("btc", "usd", service["gemini"])
    validate_price(price)


# def test_web_price_service_timeout():
#     ps = CoinbasePriceService(timeout=0.0000001)
#     result = ps.get_url()
#     assert result["error"] == "Timeout Error"
