import os
from datetime import datetime

import pytest

from ampl_plugin.ampl_sources import AnyBlockSource
from ampl_plugin.ampl_sources import BraveNewCoinSource


@pytest.mark.asyncio
async def test_bravenewcoin_source():
    """Test retrieving AMPL/USD/VWAP data from BraveNewCoin/Rapid api.

    Retrieves bearer token and adds to headers of main data request."""

    api_key = os.environ["RAPID_KEY"]
    ampl_source = BraveNewCoinSource()

    datapoint, status = await ampl_source.fetch_new_datapoint(api_key)
    value, timestamp = datapoint

    assert status.ok
    assert isinstance(value, float)
    assert isinstance(timestamp, datetime)
    assert value > 0


@pytest.mark.asyncio
async def test_anyblock_source():
    """Test retrieving AMPL/USD/VWAP data from AnyBlock api."""

    api_key = os.environ["ANYBLOCK_KEY"]
    ampl_source = AnyBlockSource()

    datapoint, status = await ampl_source.fetch_new_datapoint(api_key)
    value, timestamp = datapoint

    assert status.ok
    assert isinstance(value, float)
    assert isinstance(timestamp, datetime)
    assert value > 0
