""" Oracle Queries
This module lists all official DAO-approved queries currently supported by
the TellorX network.
"""
from telliot.query import PriceQuery
from telliot.query import PriceType
from telliot.query import QueryRegistry

#: The Query Registry
query_registry = QueryRegistry(_queries={})

# ------------------------------------------------------------------------
# Register contract approved queries
# ------------------------------------------------------------------------

query_registry.register(PriceQuery("eth", "usd", PriceType.current, 1))
query_registry.register(PriceQuery("btc", "usd", PriceType.current, 2))
query_registry.register(PriceQuery("bnb", "usd", PriceType.current, 3))
query_registry.register(PriceQuery("btc", "usd", PriceType.twap_24hr, 4))
query_registry.register(PriceQuery("eth", "btc", PriceType.current, 5))
