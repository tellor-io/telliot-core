import asyncio
import time
from datetime import datetime

import pytest

from telliot.pricing.coinbase import CoinbasePriceService
from telliot.pricing.coingecko import CoinGeckoPriceService
from telliot.base import TimeStampedFloat




def test_web_price_services():
    services = [CoinbasePriceService(),
                CoinGeckoPriceService()
                ]

    async def get_price(asset, currency):
        # Get time-stamped prices from all services
        btcusd = await \
            asyncio.gather(*[ps.get_price(asset, currency) for ps in services])
        return btcusd

    btcusd = asyncio.run(get_price('btc', 'usd'))
    print(btcusd)
    time.sleep(.0001)
    values = []
    for tsp in btcusd:
        assert isinstance(tsp, TimeStampedFloat)
        assert isinstance(tsp.val, float)
        values.append(tsp.val)
        # Assert that a timestamp was previously generated
        assert datetime.now() > tsp.ts

    # Assert all prices within 5%
    assert abs(values[0] - values[1]) / values[0] < 0.05
    assert len(values) == 2


def test_web_price_service_timeout():
    ps = CoinbasePriceService(timeout=0.0000001)
    result = ps.get_url()
    assert result["error"] == "Timeout Error"
