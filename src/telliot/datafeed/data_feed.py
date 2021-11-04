""" telliot.datafeed.data_feed

"""
from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from telliot.datafeed.data_source import DataSource
from telliot.model.base import Base
from telliot.queries.query import OracleQuery

T = TypeVar("T")


@dataclass
class DataFeed(Generic[T], Base):
    """Data feed providing query response

    A data feed contains a DataSource to fetch values in response to an `OracleQuery`.
    """

    source: DataSource[T]

    #: Query supported by this data feed
    query: OracleQuery


if __name__ == "__main__":
    # Example:
    from telliot.datafeed.data_source import RandomSource
    from telliot.queries.legacy_query import LegacyRequest

    feed = DataFeed(source=RandomSource(), query=LegacyRequest(legacy_id=4))

    import yaml

    print(yaml.dump(feed.get_state(), sort_keys=False))
