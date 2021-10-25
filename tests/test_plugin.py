"""Test plugin module"""
from telliot.plugin.discover import telliot_plugins
from telliot.queries.query import OracleQuery
from telliot.datafeed.data_feed import DataFeed
from telliot.plugin.registry import PluginRegistry
from typing import List, Any, Optional
from telliot.answer import TimeStampedAnswer


def test_discovered_plugins():
    # Make sure that default telliot_examples plugin package is registered
    assert "telliot_examples" in telliot_plugins

    example_plugin = telliot_plugins['telliot_examples']

    example_registry = example_plugin.registry

    assert example_registry.feeds


def test_plugin_registry():
    """ Test barebones plugin registry interface

    """

    class MyQueryType(OracleQuery):
        pass

    class MyFeedType(DataFeed):

        async def update_value(self, store: bool = False) -> Optional[TimeStampedAnswer[Any]]:
            raise NotImplementedError

        def get_history(self, n: int = 0) -> List[TimeStampedAnswer[Any]]:
            raise NotImplementedError

    myfeed = MyFeedType(query=MyQueryType())

    r = PluginRegistry()

    r.register_query_type(MyQueryType)
    r.register_feed_type(MyFeedType)

    r.register_feed(myfeed)

    assert myfeed in r.feeds
    assert MyQueryType in r.query_types
    assert MyFeedType in r.feed_types
