import pytest
from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry


def test_oracle_price_query():
    q = PriceQuery("eth", "usd", PriceType.current, 1)
    assert q.uid == "current-price-eth-in-usd"
    assert q.question == "What is the current price of ETH in USD?"


def test_registry():
    qr = QueryRegistry(_queries={})

    q1 = PriceQuery("eth", "usd", PriceType.current, 1)
    q2 = PriceQuery("btc", "usd", PriceType.current, 2)

    qr.register(q1)
    qr.register(q2)

    # Demonstrate getting query by UID
    query = qr.queries["current-price-eth-in-usd"]
    assert query is q1

    # Demonstrate getting query by Request ID
    query = qr.get_query_by_request_id(2)
    assert query is q2

    # Key error
    with pytest.raises(KeyError):
        query = qr.queries["does-not-exist"]

    # Avoid duplicate request IDs
    with pytest.raises(ValueError):
        qr.register(PriceQuery("btc", "usd", PriceType.current, 2))

    # Avoid duplicate UIDs
    with pytest.raises(ValueError):
        qr.register(PriceQuery("btc", "usd", PriceType.current, 3))
