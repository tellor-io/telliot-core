""" Oracle Queries
This module lists all official DAO-approved queries currently supported by
the TellorX network.
"""
from telliot.query import LegacyPriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry

#: The Query Registry
query_registry = QueryRegistry(_queries={})

# ------------------------------------------------------------------------
# Register contract approved queries
# ------------------------------------------------------------------------

query_registry.register(
    LegacyPriceQuery(1, "eth", "usd", PriceType.current)
)
query_registry.register(
    LegacyPriceQuery(2, "btc", "usd", PriceType.current)
)
query_registry.register(
    LegacyPriceQuery(3, "bnb", "usd", PriceType.current)
)
query_registry.register(
    LegacyPriceQuery(4, "btc", "usd", PriceType.twap_24hr)
)
query_registry.register(
    LegacyPriceQuery(5, "eth", "btc", PriceType.current)
)
