import enum
from dataclasses import dataclass
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel

from telliot.answer import Answer
from telliot.answer import TimeStampedFixed


@enum.unique
class PriceType(str, enum.Enum):
    """Enumeration of supported price types"""

    current = 'current'
    eod = 'end of day'
    twap_custom = 'custom time-weighted average'
    twap_1hr = '1 hour time-weighted average'
    twap_24hr = '24 hour time-weighted average'


CoerceToRequestId = Union[bytearray, bytes, int, str]


class RequestId:
    """ Request ID in bytes32 format

    """
    bytes: bytes

    def __new__(cls, value: CoerceToRequestId) -> "RequestId":

        self = object.__new__(cls)

        if isinstance(value, bytearray):
            value = bytes(value)

        if isinstance(value, bytes):
            if len(value) != 32:
                raise ValueError('bytes input must be length 32')
            else:
                self.bytes = value

        elif isinstance(value, str):
            value = value.lower()
            if value.startswith('0x'):
                value = value[2:]

            if len(value) != 64:
                raise ValueError(
                    'Request ID must be 32 bytes: {}'.format(value))
            else:
                self.bytes = bytes.fromhex(value)

        elif isinstance(value, int):
            self.bytes = value.to_bytes(32, 'big', signed=False)

        else:
            raise ValueError('Invalid RequestID: {}'.format(value))

        return self

    def hex(self) -> str:
        return '0x' + self.bytes.hex()

    def __str__(self) -> str:
        return self.hex()

    def __repr__(self) -> str:
        return "RequestId('{}')".format(self)

    def __eq__(self, other: object):
        """ Compare Request IDs for equality

        """
        # Compare always coerces `other` into a RequestID
        # in the spirit of int(5) == 5.0

        if not isinstance(other, RequestId):
            other = RequestId(other)

        return self.bytes == other.bytes


class OracleQuery(BaseModel):
    """Base class for all DAO-approved tellor queries"""

    #: Unique data Spec ID (Tellor Assigned)
    uid: str

    #: Unique Contract Request ID
    request_id: RequestId

    #: Question
    question: str

    #: Answer type
    answer_type: Callable[..., Answer[Any]]

    class Config:
        arbitrary_types_allowed = True


class PriceQuery(OracleQuery):
    """A query requesting the price of an asset in a specified currency"""

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Type
    price_type: PriceType

    def __init__(
            self, request_id: RequestId, asset: str, currency: str,
            t: PriceType, **kwargs: Any
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
            request_id=request_id,
            asset=asset,
            currency=currency,
            price_type=t,
            answer_type=TimeStampedFixed,
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
                "Cannot add query to registry: UID {} already used".format(
                    q.uid)
            )

        # Assign to registry
        self._queries[q.uid] = q

    def get_query_by_request_id(self, request_id: CoerceToRequestId) -> \
            Optional[OracleQuery]:
        """Return Query corresponding to request_id"""

        if not isinstance(request_id, RequestId):
            request_id_coerced = RequestId(request_id)
        else:
            request_id_coerced = request_id

        for query in self._queries.values():
            if query.request_id == request_id_coerced:
                return query

        return None

    def get_request_ids(self) -> List[int]:
        """Return a list of registered Request IDs."""
        return [q.request_id for q in self._queries.values()]

    def get_uids(self) -> List[str]:
        """Return a list of registered UIDs."""
        return [q.uid for q in self._queries.values()]
