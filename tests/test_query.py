""" Unit tests for query module

"""
import pytest
from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.query_registry import query_registry


# Modern query example
qm = PriceQuery(
    uid="qid-9999",
    name="ETH/USD Current Price",
    asset="eth",
    currency="usd",
    data="What is the current price of ETH in USD?".encode("utf-8"),
    price_type=PriceType.current,
)

# Legacy query example
ql = PriceQuery(
    uid="qid-9998",
    name="ETH/USD Current Price",
    asset="eth",
    currency="usd",
    data="What is the current price of ETH in USD?".encode("utf-8"),
    price_type=PriceType.current,
    legacy_request_id=1,
)


def test_modern_price_query():
    """Test modern price query"""
    assert qm.uid == "qid-9999"
    print(qm.request_id.hex())
    assert qm.data == b"What is the current price of ETH in USD?"
    assert (
        qm.request_id.hex()
        == "615b2bcf2cffe9e48e505d81caaa0f76c72fc81a2191c6e5d5c7560bc0cc4acb"
    )
    assert not qm.is_legacy


def test_legacy_price_query():
    """Test legacy price query"""
    assert ql.is_legacy
    assert ql.uid == "qid-9998"
    print(ql.data)
    assert ql.data == b"What is the current price of ETH in USD?"


def test_export_import():
    # Test export and import object
    exported = ql.dict()
    q2 = PriceQuery.parse_obj(exported)

    assert ql.uid == q2.uid
    assert ql.data == q2.data
    assert ql.legacy_request_id == q2.legacy_request_id
    assert ql.asset == q2.asset
    assert ql.currency == q2.currency
    assert ql.price_type == q2.price_type


def test_export_json():
    # Test export and import object
    exported = ql.json()
    print(exported)
    q2 = PriceQuery.parse_raw(exported)

    assert ql.uid == q2.uid
    assert ql.data == q2.data
    assert ql.legacy_request_id == q2.legacy_request_id
    assert ql.asset == q2.asset
    assert ql.currency == q2.currency
    assert ql.price_type == q2.price_type


def test_registry_creation():
    """Example registry creation"""
    qr = QueryRegistry(queries={})

    q1 = PriceQuery(
        uid="qid-9999",
        name="ETH/USD current price",
        asset="eth",
        currency="usd",
        data="What is the current price of ETH in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=1,
    )

    q2 = PriceQuery(
        uid="current-price-btc-in-usd",
        name="BTC/USD current price",
        asset="btc",
        currency="usd",
        data="What is the current price of BTC in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=2,
    )

    qr.register(q1)
    qr.register(q2)

    # Demonstrate getting query by Unique data spec ID
    query = qr.queries["qid-9999"]
    assert query is q1

    # Demonstrate getting query by Request ID
    query = qr.get_query_by_request_id(2)
    assert query is q2

    # Key error
    with pytest.raises(KeyError):
        _ = qr.queries["does-not-exist"]

    # Avoid duplicate UIDs
    with pytest.raises(ValueError):
        qr.register(
            PriceQuery(
                asset="btc",
                currency="usd",
                uid="current-price-btc-in-usd",
                data="What is the current price of BTC in USD?".encode("utf-8"),
                price_type=PriceType.current,
                legacy_request_id=2,
            )
        )


def test_get_query():
    """Test get_query"""
    q = query_registry.get_query_by_request_id(1)
    assert q.asset == "eth"


def test_export_registry():
    """Make sure we can export and re-import query registry"""
    exported = query_registry.json()
    print(exported)
    # with open("query_registry_export.json", "w") as f:
    #    f.write(exported)
    qr2 = QueryRegistry.parse_raw(exported)
    assert len(qr2.queries) == len(query_registry.queries)
