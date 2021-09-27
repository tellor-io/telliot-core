import pytest

from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.query_registry import query_registry


def test_legacy_price_query():
    q = PriceQuery("eth", "usd", PriceType.current, legacy_request_id=1)
    assert q.uid == "current-price-eth-in-usd"
    print(q.data)
    assert q.data == b"What is the current price of ETH in USD?"
    print(q.dict())


def test_modern_price_query():
    q = PriceQuery("eth", "usd", PriceType.current)
    assert q.uid == "current-price-eth-in-usd"
    print(q.request_id.hex())
    assert q.data == b"What is the current price of ETH in USD?"
    assert q.request_id.hex() == '615b2bcf2cffe9e48e505d81caaa0f76c72fc81a2191c6e5d5c7560bc0cc4acb'


def test_registry_creation():
    qr = QueryRegistry(_queries={})

    q1 = PriceQuery("eth", "usd", PriceType.current, legacy_request_id=1)
    q2 = PriceQuery("btc", "usd", PriceType.current, legacy_request_id=2)

    qr.register(q1)
    qr.register(q2)

    # Demonstrate getting query by Unique data spec ID
    query = qr.queries["current-price-eth-in-usd"]
    assert query is q1

    # Demonstrate getting query by Request ID
    query = qr.get_query_by_request_id(2)
    assert query is q2

    # Key error
    with pytest.raises(KeyError):
        _ = qr.queries["does-not-exist"]

    # Avoid duplicate request IDs
    with pytest.raises(ValueError):
        qr.register(
            PriceQuery("btc", "usd", PriceType.current, legacy_request_id=2))

    # Avoid duplicate UIDs
    with pytest.raises(ValueError):
        qr.register(
            PriceQuery("btc", "usd", PriceType.current, legacy_request_id=3))


def test_registry():
    q = query_registry.get_query_by_request_id(1)
    assert q.asset == 'eth'
