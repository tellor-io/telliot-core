""" Oracle Queries
This module lists all official DAO-approved queries currently supported by
the TellorX network.
"""
from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry
from telliot.query import RequestId

#: The Query Registry
query_registry = QueryRegistry(_queries={})

# ------------------------------------------------------------------------
# Register contract approved queries
# ------------------------------------------------------------------------

query_registry.register(
    PriceQuery(RequestId(1), "eth", "usd", PriceType.current)
)
query_registry.register(
    PriceQuery(RequestId(2), "btc", "usd", PriceType.current)
)
query_registry.register(
    PriceQuery(RequestId(3), "bnb", "usd", PriceType.current)
)
query_registry.register(
    PriceQuery(RequestId(4), "btc", "usd", PriceType.twap_24hr)
)
query_registry.register(
    PriceQuery(RequestId(5), "eth", "btc", PriceType.current)
)
