""" Oracle Queries
This module lists all official DAO-approved queries currently supported by
the TellorX network.
"""
from telliot.query import OracleQuery
from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.response_type import ResponseType

#: The Query Registry
query_registry = QueryRegistry(queries={})

# ------------------------------------------------------------------------
# Register contract approved queries
# ------------------------------------------------------------------------

query_registry.register(
    PriceQuery(
        asset="eth",
        currency="usd",
        uid="current-price-eth-in-usd",
        data="What is the current price of ETH in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=1,
    )
)
query_registry.register(
    PriceQuery(
        asset="btc",
        currency="usd",
        uid="current-price-btc-in-usd",
        data="What is the current price of BTC in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=2,
    )
)
query_registry.register(
    PriceQuery(
        asset="bnb",
        currency="usd",
        uid="current-price-bnb-in-usd",
        data="What is the current price of BNB in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=3,
    )
)
query_registry.register(
    PriceQuery(
        asset="btc",
        currency="usd",
        uid="twap_24hr-price-btc-in-usd",
        data="What is the twap_24hr price of BTC in USD?".encode("utf-8"),
        price_type=PriceType.twap_24hr,
        legacy_request_id=4,
    )
)
query_registry.register(
    PriceQuery(
        asset="eth",
        currency="btc",
        uid="current-price-eth-in-btc",
        data="What is the current price of ETH in BTC?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=5,
    )
)
query_registry.register(
    PriceQuery(
        asset="eth",
        currency="jpy",
        uid="current-price-eth-in-jpy",
        data="What is the current price of ETH in JPY?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=59,
    )
)

query_registry.register(
    PriceQuery(
        asset="trb",
        currency="usd",
        uid="current-price-trb-in-usd",
        data="What is the current price of TRB in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=50,
    )
)

query_registry.register(
    PriceQuery(
        asset="ampl",
        currency="usd",
        uid="custom-twap-price-ampl-in-usd",
        data="What is the 24hr TWAP/VWAP price of AMPL in USD as specified "
        "by ampleforth governance?".encode("utf-8"),
        price_type=PriceType.twap_custom,
        legacy_request_id=10,
    )
)

query_registry.register(
    OracleQuery(
        uid="uspce-ampleforth-feed",
        data="What is the 3 month rolling average value of the USPCE as "
        "specified by ampleforth governance?".encode("utf-8"),
        response_type=ResponseType(abi_type="ufixed256x6"),
        legacy_request_id=41,
    )
)
