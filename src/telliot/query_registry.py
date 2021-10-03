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
        uid="qid-0001",
        name="ETH/USD Current Price",
        asset="eth",
        currency="usd",
        data="What is the current price of ETH in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=1,
    )
)
query_registry.register(
    PriceQuery(
        uid="qid-0002",
        name="BTC/USD Current Price",
        asset="btc",
        currency="usd",
        data="What is the current price of BTC in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=2,
    )
)
query_registry.register(
    PriceQuery(
        uid="qid-0003",
        name="BNB/USD Current Price",
        asset="bnb",
        currency="usd",
        data="What is the current price of BNB in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=3,
    )
)
query_registry.register(
    PriceQuery(
        uid="qid-0004",
        name="BTC/USD 24hr TWAP Price",
        asset="btc",
        currency="usd",
        data="What is the twap_24hr price of BTC in USD?".encode("utf-8"),
        price_type=PriceType.twap_24hr,
        legacy_request_id=4,
    )
)
query_registry.register(
    PriceQuery(
        uid="qid-0005",
        name="ETH/BTC Current Price",
        asset="eth",
        currency="btc",
        data="What is the current price of ETH in BTC?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=5,
    )
)

query_registry.register(
    PriceQuery(
        uid="qid-0010",
        name="AMPL/USD Custom Price",
        asset="ampl",
        currency="usd",
        data="What is the 24hr TWAP/VWAP price of AMPL in USD as specified "
        "by ampleforth governance?".encode("utf-8"),
        price_type=PriceType.twap_custom,
        legacy_request_id=10,
    )
)

query_registry.register(
    OracleQuery(
        uid="qid-0041",
        name="USPCE Value (3 Month Rollng Average)",
        data="What is the 3 month rolling average value of the USPCE as "
        "specified by ampleforth governance?".encode("utf-8"),
        response_type=ResponseType(abi_type="ufixed256x6"),
        legacy_request_id=41,
    )
)

query_registry.register(
    PriceQuery(
        uid="qid-0050",
        name="TRB/USD Current Price",
        asset="trb",
        currency="usd",
        data="What is the current price of TRB in USD?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=50,
    )
)

query_registry.register(
    PriceQuery(
        uid="qid-0059",
        name="ETH/JPY Current Price",
        asset="eth",
        currency="jpy",
        data="What is the current price of ETH in JPY?".encode("utf-8"),
        price_type=PriceType.current,
        legacy_request_id=59,
    )
)

# query_registry.register(
#     OracleQuery(
#         uid="qid-0100",
#         name="Polygon Bridge (work in progress)",
#     )
# )
