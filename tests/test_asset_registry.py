from telliot_core.asset_registry import asset_registry
from telliot_core.model.tokens import BlockChainAsset


def test_asset_registry():
    btc = asset_registry.get("btc")
    assert isinstance(btc, BlockChainAsset)
