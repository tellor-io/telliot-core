import pytest
import telliot.registry
from telliot.base import TimeStampedFloat


@pytest.mark.asyncio
async def test_CurrentAssetPrice():
    btc_usd_coinbase = telliot.registry.data_sources["btc-usd-coinbase"]

    # Fetch current price
    price = await btc_usd_coinbase.update_value()
    assert isinstance(price, TimeStampedFloat)

    # Make sure value property is updated
    assert btc_usd_coinbase.value is price
