import pytest

from telliot.base import TimeStampedFloat
from telliot.datafeed.data_source import AssetPriceSource
from telliot.pricing.coinbase import CoinbasePriceService


@pytest.mark.asyncio
async def test_CurrentAssetPrice():
    btc_usd_coinbase = AssetPriceSource(name='BTC USD Price from Coinbase',
                                        uid='btc-usd-coinbase',
                                        asset='btc',
                                        currency='usd',
                                        service=CoinbasePriceService())

    # Fetch current price
    price = await btc_usd_coinbase.fetch_value()
    assert isinstance(price, TimeStampedFloat)

    # Make sure value property is updated
    assert btc_usd_coinbase.value is price
