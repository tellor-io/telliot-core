""" Query Registry

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
import csv
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from telliot.queries.legacy_query import LegacyPriceQuery
from telliot.queries.legacy_query import LegacyQuery
from telliot.queries.price_query import PriceQuery
from telliot.queries.query import CoerceToRequestId
from telliot.queries.query import OracleQuery
from telliot.queries.query import to_request_id


#: The Query Registry


class QueryRegistry(BaseModel):
    """A class for constructing the official query registry"""

    #: Dict of registered queries keyed by uid
    #: Todo: make private/read-only
    queries: Dict[str, OracleQuery]

    def register(self, q: OracleQuery) -> None:
        """Add a query to the registry"""

        # Make sure uid is unique in registry
        unique_ids = self.get_uids()
        if q.uid in unique_ids:
            raise ValueError(
                "Cannot add query to registry: UID {} already used".format(q.uid)
            )

        # Assign to registry
        self.queries[q.uid] = q

    def get_query_by_request_id(
        self, request_id: CoerceToRequestId
    ) -> Optional[OracleQuery]:
        """Return Query corresponding to request_id"""

        request_id_coerced = to_request_id(request_id)

        for query in self.queries.values():
            if query.request_id == request_id_coerced:
                return query

        return None

    def get_request_ids(self) -> List[bytes]:
        """Return a list of registered Request IDs."""
        return [q.request_id for q in self.queries.values()]

    def get_uids(self) -> List[str]:
        """Return a list of registered UIDs."""
        return [q.uid for q in self.queries.values()]


# ------------------------------------------------------------------------
# Register contract approved queries
# ------------------------------------------------------------------------


def register_legacy_price_query(
    registry: QueryRegistry,
    rqid: int,
    asset: str,
    currency: str,
    price_type: str = "current",
) -> None:
    """Register a legacy price query"""
    name = f"{asset.upper()}/{currency.upper()} {price_type.lower()} price"
    qid = f"qid-{rqid}"

    q = LegacyPriceQuery(
        name=name,
        uid=qid,
        legacy_request_id=rqid,
        asset=asset.lower(),
        currency=currency.lower(),
        price_type=price_type,
    )
    registry.register(q)


def register_legacy_pairs(registry: QueryRegistry, active_only: bool = True) -> None:
    """Register legacy pairs

    This function reads the legacy CSV file and registers all price pairs.
    A legacy query is qualified as a price pair if the label has a '/'
    Other items in the legacy CSV file are ignored.

    Args:
        registry:

    """

    legacy_file = Path(__file__).parent.absolute() / "legacy_queries.csv"

    with open(legacy_file, newline="") as csvfile:
        legacy_queries = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in legacy_queries:
            rqid = int(row[0])
            label = row[1]
            price_type = row[3].lower() or "current"
            active = bool(row[4])
            if "/" in label:
                asset, currency = label.split("/")

                if active_only:
                    if active:
                        register_legacy_price_query(
                            registry, rqid, asset, currency, price_type
                        )
                else:
                    register_legacy_price_query(
                        registry, rqid, asset, currency, price_type
                    )


qid_41 = LegacyQuery(
    uid="qid-41",
    name="USPCE manual value",
    legacy_request_id=41,
    legacy_question=b"what is the manual value of the USPCE",
)

qid_53 = LegacyQuery(
    uid="qid-53",
    name="BTCDOMINANCE value",
    legacy_request_id=53,
    legacy_question=b"what is the current value of BTCDOMINANCE",
)

qid_56 = LegacyQuery(
    uid="qid-56",
    name="VIXEOD value",
    legacy_request_id=56,
    legacy_question=b"what is the current value of VIXEOD",
)

qid_57 = LegacyQuery(
    uid="qid-57",
    name="DEFITVL value",
    legacy_request_id=57,
    legacy_question=b"what is the current value of DEFITVL",
)

qid_58 = LegacyQuery(
    uid="qid-58",
    name="DEFIMCAP value",
    legacy_request_id=58,
    legacy_question=b"what is the current value of DEFIMCAP",
)


def create_default_registry() -> QueryRegistry:
    """Build the default query registry"""
    qr = QueryRegistry(queries={})

    # Legacy pairs
    register_legacy_pairs(qr)

    # Legacy values (not price pairs)
    qr.register(qid_41)
    qr.register(qid_53)
    qr.register(qid_56)
    qr.register(qid_57)
    qr.register(qid_58)

    # Modern queries
    qid_101 = PriceQuery()
    qr.register(qid_101)

    return qr


# User-facing default registry
query_registry = create_default_registry()

# query_registry.register(
#     LegacyQuery(
#         uid="qid-0001",
#         name="ETH/USD Current Price",
#         asset="eth",
#         currency="usd",
#         data="What is the current price of ETH in USD?".encode("utf-8"),
#         price_type=PriceType.current,
#         legacy_request_id=1,
#     )
# )
# query_registry.register(
#     PriceQuery(
#         uid="qid-0002",
#         name="BTC/USD Current Price",
#         asset="btc",
#         currency="usd",
#         data="What is the current price of BTC in USD?".encode("utf-8"),
#         price_type=PriceType.current,
#         legacy_request_id=2,
#     )
# )

# query_registry.register(
#     PriceQuery(
#         uid="qid-0003",
#         name="BNB/USD Current Price",
#         asset="bnb",
#         currency="usd",
#         data="What is the current price of BNB in USD?".encode("utf-8"),
#         price_type=PriceType.current,
#         legacy_request_id=3,
#     )
# )
# query_registry.register(
#     PriceQuery(
#         uid="qid-0004",
#         name="BTC/USD 24hr TWAP Price",
#         asset="btc",
#         currency="usd",
#         data="What is the twap_24hr price of BTC in USD?".encode("utf-8"),
#         price_type=PriceType.twap_24hr,
#         legacy_request_id=4,
#     )
# )
# query_registry.register(
#     PriceQuery(
#         uid="qid-0005",
#         name="ETH/BTC Current Price",
#         asset="eth",
#         currency="btc",
#         data="What is the current price of ETH in BTC?".encode("utf-8"),
#         price_type=PriceType.current,
#         legacy_request_id=5,
#     )
# )
#
# query_registry.register(
#     PriceQuery(
#         uid="qid-0010",
#         name="AMPL/USD Custom Price",
#         asset="ampl",
#         currency="usd",
#         data="What is the 24hr TWAP/VWAP price of AMPL in USD as specified "
#         "by ampleforth governance?".encode("utf-8"),
#         price_type=PriceType.twap_custom,
#         legacy_request_id=10,
#     )
# )
#
# query_registry.register(
#     OracleQuery(
#         uid="qid-0041",
#         name="USPCE Value (3 Month Rollng Average)",
#         data="What is the 3 month rolling average value of the USPCE as "
#         "specified by ampleforth governance?".encode("utf-8"),
#         response_type=ResponseType(abi_type="ufixed256x6"),
#         legacy_request_id=41,
#     )
# )
#
# query_registry.register(
#     PriceQuery(
#         uid="qid-0050",
#         name="TRB/USD Current Price",
#         asset="trb",
#         currency="usd",
#         data="What is the current price of TRB in USD?".encode("utf-8"),
#         price_type=PriceType.current,
#         legacy_request_id=50,
#     )
# )
#
# query_registry.register(
#     PriceQuery(
#         uid="qid-0059",
#         name="ETH/JPY Current Price",
#         asset="eth",
#         currency="jpy",
#         data="What is the current price of ETH in JPY?".encode("utf-8"),
#         price_type=PriceType.current,
#         legacy_request_id=59,
#     )
# )

# query_registry.register(
#     OracleQuery(
#         uid="qid-0100",
#         name="Polygon Bridge (work in progress)",
#     )
# )
