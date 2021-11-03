import pytest

from telliot_examples.get_ampl_vals import AMPLSource, BraveNewCoinSource
import os


@pytest.mark.asyncio
async def test_bravenewcoin_source():
    """"""
    api_key = os.environ["RAPID_KEY"]
    ampl_source = BraveNewCoinSource()

    access_token, status = await ampl_source.get_bearer_token(api_key)
    assert status.ok
    assert access_token

    url = "https://bravenewcoin.p.rapidapi.com/ohlcv?size=1&indexId=551cdbbe-2a97-4af8-b6bc-3254210ed021&indexType=GWA"
    params = ["content", 0, "vwap"]

    headers = {
    'authorization': f"Bearer {access_token}",
    'x-rapidapi-host': "bravenewcoin.p.rapidapi.com",
    'x-rapidapi-key': api_key
    }

    val, status = await ampl_source.update_value(
        url=url,  
        params=params,
        headers=headers
    )

    assert status.ok
    assert val


@pytest.mark.asyncio
async def test_anyblock_source():
    """"""
    api_key = os.environ["ANYBLOCK_KEY"]
    url = "https://api.anyblock.tools/market/AMPL_USD_via_ALL/daily-volume?roundDay=false&debug=false&access_token="
    url += api_key
    params = ["overallVWAP"]
    
    ampl_source = AMPLSource()

    val, status = await ampl_source.update_value(url=url, params=params)

    assert status.ok
    assert val
