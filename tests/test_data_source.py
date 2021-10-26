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


def test_data_source_registry():
    """Test data source configs"""
    from telliot.datafeed.data_source import DataSource

    class DataSourceA(DataSource):
        pass

    class DataSourceB(DataSource):
        pass

    typeA = ModelRegistry.get('DataSourceA')

    print(ModelRegistry.models())
    print(typeA)


    from telliot.model.registry import find_subclasses

    print(find_subclasses(DataSource))


    # Cleanup
    # os.remove(config_file)
    # os.remove(config_file_bak)


