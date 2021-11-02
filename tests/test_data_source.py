""" Unit tests for data source module

"""
from datetime import datetime

import pytest
from telliot.datafeed.data_source import RandomSource
from telliot.datafeed.data_source import DataSource


def test_data_source_abc():
    class MyDataSource(DataSource):
        pass

    with pytest.raises(TypeError):
        obj = MyDataSource()


@pytest.mark.asyncio
async def test_RandomSource():
    s1 = RandomSource()
    # status, value, timestamp = await s1.update_value()
    tsval = await s1.update_value()

    # assert status.ok
    assert 0 <= tsval.val < 1
    assert isinstance(tsval.ts, datetime)

# @pytest.mark.asyncio
# async def test_CurrentAssetPrice():
#     """Retrieve BTC price in USD from Coinbase."""
#     btc_usd_coinbase = data_sources[0]
#
#     # Fetch current price
#     price = await btc_usd_coinbase.update_value()
#     assert isinstance(price, TimeStampedFloat)
#
#     # Make sure value property is updated
#     assert btc_usd_coinbase.value is price
