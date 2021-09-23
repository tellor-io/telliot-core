import enum
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from telliot.answer import Answer
from telliot.answer import TimeStampedFixed


@enum.unique
class PriceType(enum.Enum):
    """Enumeration of supported price types"""

    current = 1
    eod = 2
    twap_custom = 20
    twap_1hr = 21
    twap_24hr = 22


class OracleQuery(BaseModel):
    """Base class for all DAO-approved tellor queries"""

    #: Unique Query ID
    uid: str

    #: Unique Contract Request ID
    request_id: int

    #: Question
    question: str

    #: Answer type
    answer_type: Callable[..., Answer[Any]]


class PriceQuery(OracleQuery):
    """A query requesting the price of an asset in a specified currency"""

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Type
    price_type: PriceType

    def __init__(
        self, asset: str, currency: str, t: PriceType, request_id: int, **kwargs: Any
    ):

        # Use default question if not provided
        question = kwargs.get("question", None)
        if not question:
            question = "What is the {} price of {} in {}?".format(
                t.name, asset.upper(), currency.upper()
            )

        # Use default unique ID if not provided
        uid = kwargs.get("uid")
        if not uid:
            uid = "{}-price-{}-in-{}".format(t.name, asset, currency)

        super().__init__(
            asset=asset,
            currency=currency,
            price_type=t,
            answer_type=TimeStampedFixed,
            request_id=request_id,
            question=question,
            uid=uid,
        )


@dataclass
class QueryRegistry:
    """A class for constructing the official query registry"""

    #: Read only dict of registered queries
    queries = property(lambda self: self._queries)

    #: private query storage
    _queries: Dict[str, OracleQuery]

    def register(self, q: OracleQuery) -> None:
        """Add a query to the registry"""

        # Make sure request_id is unique in registry
        request_ids = self.get_request_ids()
        if q.request_id in request_ids:
            raise ValueError(
                "Cannot add query to registry: Request ID {} already used".format(
                    q.request_id
                )
            )

        # Make sure uid is unique in registry
        uids = self.get_uids()
        if q.uid in uids:
            raise ValueError(
                "Cannot add query to registry: UID {} already used".format(q.uid)
            )

        # Assign to registry
        self._queries[q.uid] = q

    def get_query_by_request_id(self, request_id: int) -> Optional[OracleQuery]:
        """Return Query corresponding to request_id"""
        for query in self._queries.values():
            if query.request_id == request_id:
                return query

        return None

    def get_request_ids(self) -> List[int]:
        """Return a list of registered Request IDs."""
        return [q.request_id for q in self._queries.values()]

    def get_uids(self) -> List[str]:
        """Return a list of registered UIDs."""
        return [q.uid for q in self._queries.values()]
