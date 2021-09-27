import pytest

from telliot.query import LegacyPriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.query_registry import query_registry


def test_legacy_price_query():
    q = LegacyPriceQuery(1, "eth", "usd", PriceType.current)
    assert q.uid == "current-price-eth-in-usd"
    print(q.data)
    assert q.data == b"What is the current price of ETH in USD?"
    print(q.dict())


def test_registry_creation():
    qr = QueryRegistry(_queries={})

    q1 = LegacyPriceQuery(1, "eth", "usd", PriceType.current)
    q2 = LegacyPriceQuery(2, "btc", "usd", PriceType.current)

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
            LegacyPriceQuery(2, "btc", "usd", PriceType.current))

    # Avoid duplicate UIDs
    with pytest.raises(ValueError):
        qr.register(
            LegacyPriceQuery(3, "btc", "usd", PriceType.current))


def test_registry():
    q = query_registry.get_query_by_request_id(1)
    assert q.asset == 'eth'
