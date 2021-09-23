""" Simple example of creating a "plug-in" data feed

"""
import statistics

import pytest
from telliot.reporter_plugins.rinkeby_btc_usd.registry import btc_usd_data_feeds


@pytest.mark.asyncio
async def test_AssetPriceFeed():
    """Retrieve median BTC price from example datafeed &
    make sure value is within tolerance."""
    btc_usd_median = btc_usd_data_feeds["btc-usd-median"]

    price = await btc_usd_median.update_value()

    # Get list of data sources from sources dict
    sources = [source.value for source in btc_usd_median.sources.values()]

    # Make sure error is less than decimal tolerance
    assert (price.val - statistics.median([s.val for s in sources])) < 10 ** -6
