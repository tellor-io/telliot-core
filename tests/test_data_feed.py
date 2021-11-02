""" Simple example of creating a "plug-in" data feed

"""
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional

import pytest
from telliot.answer import TimeStampedAnswer
from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.data_source import RandomSource
from telliot.queries.legacy_query import LegacyRequest

# from telliot.datafeed.data_source import SourceOutputType


@dataclass
class MyDataFeed(DataFeed):
    random_source: RandomSource = field(default_factory=RandomSource)

    async def update_value(self) -> Optional[TimeStampedAnswer[Any]]:
        # async def update_value(self) -> SourceOutputType:

        self._value = await self.random_source.update_value()

        return self.value


my_feed = MyDataFeed(query=LegacyRequest(legacy_id=4))


@pytest.mark.asyncio
async def test_my_data_source():

    # result, value, tstamp = await my_feed.update_value()
    tsval = await my_feed.update_value()
    # assert result.ok
    assert 0 <= tsval.val < 1

    print(my_feed.get_state())
    print(my_feed.value)
