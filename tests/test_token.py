from telliot_core.model.tokens import ERC20TokenList


def test_token_list():
    """Test importing a file from uniswap format"""
    _ = ERC20TokenList.from_uniswap(EXAMPLE_TOKEN_LIST)


EXAMPLE_TOKEN_LIST = {
    "name": "My Token List",
    "version": {"major": 2, "minor": 0, "patch": 0},
    "tokens": [
        {
            "chainId": 1,
            "address": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9",
            "name": "Aave",
            "symbol": "AAVE",
            "decimals": 18,
            "logoURI": "https://assets.coingecko.com/coins/images/12645/thumb/AAVE.png?1601374110",
        },
        {
            "chainId": 1,
            "address": "0xfF20817765cB7f73d4bde2e66e067E58D11095C2",
            "name": "Amp",
            "symbol": "AMP",
            "decimals": 18,
            "logoURI": "https://assets.coingecko.com/coins/images/12409/thumb/amp-200x200.png?1599625397",
        },
        {
            "name": "Aragon Network Token",
            "address": "0x960b236A07cf122663c4303350609A66A7B288C0",
            "symbol": "ANT",
            "decimals": 18,
            "chainId": 1,
            "logoURI": "https://raw.githubusercontent.com/trustwallet/"
            "assets/master/blockchains/ethereum/assets/"
            "0x960b236A07cf122663c4303350609A66A7B288C0/logo.png",
        },
    ],
}
