import logging
from dataclasses import dataclass
from typing import Any

from telliot_core.dtypes.float_type import UnsignedFloatType
from telliot_core.dtypes.value_type import ValueType
from telliot_core.queries.abi_query import AbiQuery

logger = logging.getLogger(__name__)


@dataclass
class AWSSpotPrice(AbiQuery):
    """Returns the spot price in USD of the hourly rate to rent AWS compute instances."""

    parameters: list[dict[str, Any]]

    @property
    def value_type(self) -> ValueType:
        """Data type returned for a SpotPrice query.

        - `ufixed256x18`: 256-bit unsigned integer with 18 decimals of precision
        - `packed`: false
        """
        return UnsignedFloatType(abi_type="ufixed256x18", packed=False)

    def __post_init__(self) -> None:
        assert self.parameters[0]["name"] == "zone"
        assert self.parameters[1]["name"] == "instance"
