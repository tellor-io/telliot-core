""" Simple example of creating a "plug-in" data feed

"""
import statistics

import pytest
from telliot.queries.query import OracleQuery
from telliot_examples.feeds.btc_usd_feed import btc_usd_median_feed


@pytest.mark.asyncio
async def test_AssetPriceFeed():
    """Retrieve median BTC price from example datafeed &
    make sure value is within tolerance."""

    price = await btc_usd_median_feed.update_value()

    # Get list of data sources from sources dict
    sources = [source.value for source in btc_usd_median_feed.sources.values()]

    # Make sure error is less than decimal tolerance
    assert (price.val - statistics.median([s.val for s in sources])) < 10 ** -6

    # Get query
    q = btc_usd_median_feed.query
    assert isinstance(q, OracleQuery)
