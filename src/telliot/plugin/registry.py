from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Type

from telliot.datafeed.data_feed import DataFeed
from telliot.queries import OracleQuery


@dataclass
class PluginRegistry:
    """Plugin Registry

    This is the main interface for plugins to register capabilities with Telliot
    """

    #: List of data feed instances to register with telliot
    feeds: List[DataFeed] = field(default_factory=list)

    #: List of custom query types to register with telliot
    query_types: List[Type[OracleQuery]] = field(default_factory=list)

    #: List of custom data feed types to register with telliot
    feed_types: List[Type[DataFeed]] = field(default_factory=list)

    def register_feed(self, feed: DataFeed) -> None:
        """Register a feed"""
        self.feeds.append(feed)

    def register_query_type(self, query_type: Type[OracleQuery]) -> None:
        """Register a query_type"""
        self.query_types.append(query_type)

    def register_feed_type(self, feed_type: Type[DataFeed]) -> None:
        """Register a query_type"""
        self.feed_types.append(feed_type)
