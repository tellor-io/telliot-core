import pytest
from telliot.answer import TimeStampedFloat
from telliot.plugins.rinkeby_btc_usd.registry import data_sources


@pytest.mark.asyncio
async def test_CurrentAssetPrice():
    """Retrieve BTC price in USD from Coinbase."""
    btc_usd_coinbase = data_sources["btc-usd-coinbase"]

    # Fetch current price
    price = await btc_usd_coinbase.update_value()
    assert isinstance(price, TimeStampedFloat)

    # Make sure value property is updated
    assert btc_usd_coinbase.value is price
