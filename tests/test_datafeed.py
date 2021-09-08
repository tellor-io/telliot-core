""" Simple example of creating a "plug-in" data feed

"""
import random
from dataclasses import dataclass
from typing import List

from telliot.datafeed.feeder import DataFeed
from telliot.datafeed.feeder import DataSource


@dataclass
class ConstantDataSource(DataSource):
    """A dumb data source that just fetches a constant value"""

    value: float = 0

    def fetch(self):
        return self.value


@dataclass
class RandomDataSource(DataSource):
    """A dumb data source that fetches a random value"""

    def fetch(self):
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
ds1 = ConstantDataSource(id="ds1", value=2.0)
ds2 = ConstantDataSource(id="ds2", value=3.0)
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
