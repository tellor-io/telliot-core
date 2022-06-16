from telliot_core.model.chain import Chain
from telliot_core.model.chain import ChainList


def test_chain():
    """Test ChainList"""

    cl = ChainList()
    ch = cl.get_chain("ETH", "mainnet")
    assert isinstance(ch, Chain)
    assert ch.chain == "ETH"
    assert ch.chain_id == 1
    assert ch.network == "mainnet"


def test_matic():
    cl = ChainList()
    ch = cl.get_chain("MATIC", "mainnet")
    assert isinstance(ch, Chain)
    assert ch.chain_id == 137

    ch = cl.get_chain("MATIC", "testnet")
    assert ch.chain_id == 80001
