""" Simple example of creating a "plug-in" data feed

"""
import random
from dataclasses import dataclass
from typing import List

from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.data_feed import DataSource
from telliot.datafeed.data_source import Constant


@dataclass
class RandomDataSource(DataSource):
    """A dumb data source that fetches a random value"""

    async def fetch(self):
        return random.random()


# A simple algorithm
def total_dude_level1(
    bart: float = 0, frank: float = 0, smitty: float = 0
) -> float:
    return bart + frank + smitty


# An algorithm operating on a list input
def total_dude_level2(dudes: List[float]) -> float:
    return sum(dudes)


# Create a new data feed by registering the data sources
# and the algorithm
ds1 = Constant(2.0, id="ds1")
ds2 = Constant(3.0, id="ds2")
ds3 = RandomDataSource(id="ds3")


def test_feed1():
    # Create a new data feed by registering the data sources
    # and the algorithm
    myFeed = DataFeed(
        name="My data feed",
        id="my-data-feed",
        algorithm=total_dude_level1,
        sources={"bart": ds1, "frank": ds2, "smitty": ds3},
    )

    for _ in range(10):
        result = myFeed.update()
        print(result)
        assert 5 < result < 6
