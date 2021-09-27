import abc
import enum
from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import Union

from pydantic import BaseModel
from web3 import Web3

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


class RequestId(BaseModel):
    """ Request ID in bytes32 format

    """
    byteval: bytes

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, value: CoerceToRequestId, **data: Any) -> "RequestId":

        if isinstance(value, bytearray):
            value = bytes(value)

        if isinstance(value, bytes):
            if len(value) != 32:
                raise ValueError('bytes input must be length 32')
            else:
                byteval = value

        elif isinstance(value, str):
            value = value.lower()
            if value.startswith('0x'):
                value = value[2:]

            if len(value) != 64:
                raise ValueError(
                    'Request ID must be 32 bytes: {}'.format(value))
            else:
                byteval = bytes.fromhex(value)

        elif isinstance(value, int):
            byteval = value.to_bytes(32, 'big', signed=False)

        else:
            raise ValueError('Invalid RequestID: {}'.format(value))

        super().__init__(byteval=byteval, **data)

    def hex(self) -> str:
        return '0x' + self.byteval.hex()

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

        return self.byteval == other.byteval


class _OracleQuery(BaseModel, abc.ABC):
    """Base class for all tellorX queries

    """

    #: Unique query name (Tellor Assigned)
    uid: str

    #: Data Specification
    data: bytes

    #: Answer type
    answer_type: Type[Answer]

    @property
    @abc.abstractmethod
    def request_id(self) -> bytes:
        pass


class LegacyQuery(_OracleQuery):
    """Legacy Query with fixed request_id <= 100."""

    #: Integer Request ID
    legacy_request_id: int

    @property
    def request_id(self):
        return self.legacy_request_id.to_bytes(32, 'big', signed=False)


class OracleQuery(_OracleQuery):
    """Base class for all modern tellorX queries"""

    @property
    def request_id(self):
        return Web3.keccak(self.data)


class LegacyPriceQuery(LegacyQuery):
    """A legacy query requesting the price of an asset in a specified currency"""

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Type
    price_type: PriceType

    def __init__(
            self, request_id: int, asset: str, currency: str,
            t: PriceType, **kwargs: Any
    ):
        # Use default unique ID if not provided
        uid = kwargs.get("uid")
        if not uid:
            uid = "{}-price-{}-in-{}".format(t.name, asset, currency)

        question = "What is the {} price of {} in {}?".format(
            t.name, asset.upper(), currency.upper()
        )

        super().__init__(
            data=bytes(question.encode('utf-8')),
            legacy_request_id=request_id,
            asset=asset,
            currency=currency,
            price_type=t,
            answer_type=TimeStampedFixed,
            uid=uid,
        )


@dataclass
class QueryRegistry:
    """A class for constructing the official query registry"""

    #: Read only dict of registered queries
    queries = property(lambda self: self._queries)

    #: private query storage
    _queries: Dict[str, _OracleQuery]

    def register(self, q: _OracleQuery) -> None:
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
            Optional[_OracleQuery]:
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
