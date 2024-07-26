"""
Tests covering Pytelliot data source API key utils.
"""
from telliot_core.model.api_keys import ApiKeyList


def test_api_key_list():
    lis = ApiKeyList()
    # print(json.dumps(sl.get_state(), indent=2))
    res = lis.find(name="bravenewcoin")[0]
    assert res.url == "https://bravenewcoin.p.rapidapi.com/"

    res = lis.find(url="https://api.nomics.com/")[0]
    assert res.name == "nomics"

    res = lis.find(name="coinmarketcap")[0]
    assert res.url == "https://pro-api.coinmarketcap.com/"

    res = lis.find(name="coingecko")[0]
    assert res.url == "https://pro-api.coingecko.com"

    res = lis.find(name="thegraph")[0]
    assert res.url == "https://gateway-arbitrum.network.thegraph.com/api"
