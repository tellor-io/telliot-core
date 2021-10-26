""" Unit tests for data source module

"""
import pytest
from telliot.answer import TimeStampedFloat
from telliot_examples.feeds.btc_usd_feed import data_sources
from telliot.model.registry import ModelRegistry

@pytest.mark.asyncio
async def test_CurrentAssetPrice():
    """Retrieve BTC price in USD from Coinbase."""
    btc_usd_coinbase = data_sources[0]

    # Fetch current price
    price = await btc_usd_coinbase.update_value()
    assert isinstance(price, TimeStampedFloat)

    # Make sure value property is updated
    assert btc_usd_coinbase.value is price

