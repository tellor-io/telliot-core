import logging
from dataclasses import dataclass

from telliot_core.dtypes.value_type import ValueType
from telliot_core.queries.abi_query import AbiQuery

logger = logging.getLogger(__name__)


@dataclass
class Morphware(AbiQuery):
    """Returns the result for a given Morphware query version number.

    Attributes:
        version:
            A reference to Morphware data specifications found
            here: www.TODObyMorphware.org/path/to/data/specs

            More about this query:
            https://github.com/tellor-io/dataSpecs/blob/main/types/Morphware.md

            More about Morphware:
            https://morphware.org
    """

    version: int

    #: ABI used for encoding/decoding parameters
    abi = [{"name": "version", "type": "uint256"}]

    @property
    def value_type(self) -> ValueType:
        """Data type returned for a Morphware query.

        - `string`: JSON string containing provider, zones, and instance types
        - `packed`: false
        """
        return ValueType(abi_type="string", packed=False)
