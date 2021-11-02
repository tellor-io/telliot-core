""" Unit tests for data source module

"""
from datetime import datetime

import pytest
from telliot.datafeed.data_source import DataSource
from telliot.datafeed.data_source import RandomSource


def test_data_source_abc():
    class MyDataSource(DataSource):
        pass

    with pytest.raises(TypeError):
        _ = MyDataSource()


@pytest.mark.asyncio
async def test_RandomSource():
    s1 = RandomSource()
    # status, value, timestamp = await s1.update_value()
    tsval = await s1.update_value()

    # assert status.ok
    assert 0 <= tsval.val < 1
    assert isinstance(tsval.ts, datetime)
