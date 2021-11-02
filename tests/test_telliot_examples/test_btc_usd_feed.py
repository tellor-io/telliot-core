import pytest

from telliot.queries.query import OracleQuery
from telliot_examples.feeds.btc_usd_feed import btc_usd_median_feed
import statistics


@pytest.mark.asyncio
async def test_AssetPriceFeed():
    """Retrieve median BTC price from example datafeed &
    make sure value is within tolerance."""

    # Get query
    q = btc_usd_median_feed.query
    assert isinstance(q, OracleQuery)

    # Fetch price
    # status, price, tstamp = await btc_usd_median_feed.update_value()
    tsval = await btc_usd_median_feed.update_value()

    # Make sure error is less than decimal tolerance
    #assert status.ok
    assert 10000 < tsval.val < 100000
    print(f"BTC Price: {tsval.val}")

    # Get list of data sources from sources dict
    source_prices = [source.value.val for source in btc_usd_median_feed.sources]

    # Make sure error is less than decimal tolerance
    assert (tsval.val - statistics.median(source_prices)) < 10 ** -6

