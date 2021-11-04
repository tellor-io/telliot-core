import os

import pytest
from ampl_plugin.ampl_sources import AMPLSource
from ampl_plugin.ampl_sources import BraveNewCoinSource
from datetime import datetime


@pytest.mark.asyncio
async def test_bravenewcoin_source():
    """Test retrieving AMPL/USD/VWAP data from BraveNewCoin/Rapid api.

    Retrieves bearer token and adds to headers of main data request."""

    api_key = os.environ["RAPID_KEY"]
    ampl_source = BraveNewCoinSource()

    access_token, status = await ampl_source.get_bearer_token(api_key)
    assert status.ok
    assert access_token

    url = (
        "https://bravenewcoin.p.rapidapi.com/ohlcv?"
        + "size=1&indexId=551cdbbe-2a97-4af8-b6bc-3254210ed021&indexType=GWA"
    )
    params = ["content", 0, "vwap"]

    headers = {
        "authorization": f"Bearer {access_token}",
        "x-rapidapi-host": "bravenewcoin.p.rapidapi.com",
        "x-rapidapi-key": api_key,
    }

    datapoint, status = await ampl_source.fetch_new_datapoint(
        url=url, params=params, headers=headers
    )
    value, timestamp = datapoint
    
    assert status.ok
    assert isinstance(value, float)
    assert isinstance(timestamp, datetime)
    assert value > 0 



@pytest.mark.asyncio
async def test_anyblock_source():
    """Test retrieving AMPL/USD/VWAP data from AnyBlock api."""

    api_key = os.environ["ANYBLOCK_KEY"]
    url = (
        "https://api.anyblock.tools/market/AMPL_USD_via_ALL/daily-volume"
        + "?roundDay=false&debug=false&access_token="
    )
    url += api_key
    params = ["overallVWAP"]

    ampl_source = AMPLSource()

    datapoint, status = await ampl_source.fetch_new_datapoint(url=url, params=params)
    value, timestamp = datapoint

    assert status.ok
    assert isinstance(value, float)
    assert isinstance(timestamp, datetime)
    assert value > 0 
