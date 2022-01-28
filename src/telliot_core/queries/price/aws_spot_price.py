import logging
from dataclasses import dataclass

from telliot_core.data.aws import INSTANCE_TYPES
from telliot_core.data.aws import ZONES
from telliot_core.dtypes.float_type import UnsignedFloatType
from telliot_core.dtypes.value_type import ValueType
from telliot_core.queries.abi_query import AbiQuery

logger = logging.getLogger(__name__)


@dataclass
class AwsSpotPrice(AbiQuery):
    """Returns the spot price in USD of the hourly rate to rent AWS compute instances.

    Attributes:
        zone:
            Asset ID (see data specifications for a full list of supported assets)
        instance:
            Currency (default = `usd`)
    """

    zone: str

    instance: str

    #: ABI used for encoding/decoding parameters
    abi = [
        {
            "abi_type": "string",
            "name": "zone",
        },
        {
            "abi_type": "string",
            "name": "instance",
        },
    ]

    @property
    def value_type(self) -> ValueType:
        """Data type returned for a AwsSpotPrice query.

        - `ufixed256x18`: 256-bit unsigned integer with 18 decimals of precision
        - `packed`: false
        """
        return UnsignedFloatType(abi_type="ufixed256x18", packed=False)

    def __post_init__(self) -> None:
        """Validate input values"""

        if self.zone not in ZONES:
            raise ValueError(f"AWS zone ({self.zone}) not found")

        if self.instance not in INSTANCE_TYPES:
            raise ValueError(f"Instance type ({self.instance}) not found")
