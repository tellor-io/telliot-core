import logging
from dataclasses import dataclass

from telliot_core.dtypes.value_type import ValueType
from telliot_core.queries.abi_query import AbiQuery

logger = logging.getLogger(__name__)


@dataclass
class Snapshot(AbiQuery):
    """Returns the result for a given option ID (a specific proposal) on Snapshot.
        An array of values representing the amount of votes (uints) for each vote option should be returned

    Attributes:
        proposal_id:
            Specifies the requested data a of a valid proposal on Snapshot.

    see https://docs.snapshot.org/graphql-api for reference
    """

    proposal_id: str

    #: ABI used for encoding/decoding parameters
    abi = [{"name": "proposal_id", "type": "string"}]

    @property
    def value_type(self) -> ValueType:
        """Data type returned for a Snapshot query.

        - `uint256[]`: variable-length array of 256-bit values with 18 decimals of precision
        - `packed`: false
        """

        return ValueType(abi_type="uint256[]", packed=False)
