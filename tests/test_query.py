import pytest
from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.query_registry import query_registry
from telliot.response_type import ResponseType

# Modern query example
qm = PriceQuery(
    asset="eth",
    currency="usd",
    uid="current-price-eth-in-usd",
    data="What is the current price of ETH in USD?".encode("utf-8"),
    price_type=PriceType.current
)

# Legacy query example
ql = PriceQuery(
    asset="eth",
    currency="usd",
    uid="current-price-eth-in-usd",
    data="What is the current price of ETH in USD?".encode("utf-8"),
    price_type=PriceType.current,
    legacy_request_id=1
)


def test_modern_price_query():
    """Test modern price query"""
    assert qm.uid == "current-price-eth-in-usd"
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
    assert ql.uid == "current-price-eth-in-usd"
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


# @pytest.mark.skip("TODO: Finish making serializable")
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
        asset="eth",
        currency="usd",
        uid="current-price-eth-in-usd",
        data="What is the current price of ETH in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=1,
    )

    q2 = PriceQuery(
        asset="btc",
        currency="usd",
        uid="current-price-btc-in-usd",
        data="What is the current price of BTC in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=2,
    )

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
            PriceQuery(
                asset="btc",
                currency="usd",
                uid="current-price-btc-in-usd",
                data="What is the current price of BTC in USD?".encode("utf-8"),
                price_type=PriceType.current,
                legacy_request_id=2,
            )
        )

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
    exported = query_registry.dict()
    print(exported)
    qr2 = QueryRegistry.parse_obj(exported)
    assert len(qr2.queries) == len(query_registry.queries)
