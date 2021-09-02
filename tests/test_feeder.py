""" Simple example of creating a "plug-in" data feed

"""
import random

from atom.api import Float

from pytelliot.feeder import DataFeed
from pytelliot.feeder import DataSource


class ConstantDataSource(DataSource):
    """ A dumb data source that just fetches a constant value

    """
    value = Float()

    def fetch(self):
        return self.value


class RandomDataSource(DataSource):
    """ A dumb data source that fetches a random value

    """

    def fetch(self):
        return random.random()


# Specify algorithm that operates on data sources
def totalDudeLevel(bart=None, frank=None, smitty=None):
    return bart + frank + smitty


# Create a new data feed by registering the data sources
# and the algorithm
ds1 = ConstantDataSource(id='bart', value=2.0)
ds2 = ConstantDataSource(id='frank', value=3.0)
ds3 = RandomDataSource(id='smitty')

# Create a new data feed by registering the data sources
# and the algorithm
myFeed = DataFeed(
    name='My data feed',
    id='my-data-feed',
    algorithm=totalDudeLevel,
    sources=[ds1, ds2, ds3]
)


def test_feed():
    for _ in range(10):
        result = myFeed.update()
        print(result)
        assert 5 < result < 6
