import asyncio

from telliot.pricing.coinbase import CoinbasePriceService
from telliot.pricing.coingecko import CoinGeckoPriceService


def test_web_price_service():
    ps = CoinbasePriceService()
    result = ps.get_url()
    assert "response" in result
    assert result["response"] is not None
    btcusd = asyncio.run(ps.get_price("btc", "usd"))
    print(btcusd)
    assert isinstance(btcusd, float)


def test_web_price_service_timeout():
    ps = CoinbasePriceService(timeout=0.00001)
    result = ps.get_url()
    assert result["error"] == "Timeout Error"


def test_coingecko_price_service():
    ps = CoinGeckoPriceService()
    btcusd = asyncio.run(ps.get_price("btc", "usd"))
    print(btcusd)
    assert isinstance(btcusd, float)
