from typing import List
from typing import Optional

from telliot.answer import TimeStampedFloat
from telliot.datafeed.data_source import DataSourceDb
from telliot.pricing.price_service import WebPriceService


class AssetPriceSource(DataSourceDb):
    """Current Asset Price

    The Current Asset Price data source retrieves the price of a coin
    in the specified current from a `WebPriceService`.
    """

    #: Current time-stamped value of the data source or None
    #: Override base class type
    value: Optional[TimeStampedFloat]

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Service
    service: WebPriceService

    #: Pydantic hack to allow general type-checking
    class Config:
        arbitrary_types_allowed = True

    async def update_value(self, store: bool = False) -> Optional[TimeStampedFloat]:
        """Update current value with time-stamped value fetched from source

        Args:
            store:  If true and applicable, updated value will be stored
                    to the database

        Returns:
            Current time-stamped value
        """
        price = await self.service.get_price(self.asset, self.currency)

        self.value = price

        if store:
            await self.store_value()

        return price

    async def load_value(self) -> TimeStampedFloat:
        """Update current value with time-stamped value fetched from database

        TODO
        """
        raise NotImplementedError

    async def store_value(self) -> None:
        """Store current time-stamped value to database

        TODO
        """
        raise NotImplementedError

    async def get_history(self, n: int = 0) -> List[TimeStampedFloat]:  # type: ignore
        """Get data source history from database

        Args:
            n:  If n > 0, get n datapoints from database, otherwise get all
                available datapoints.

        Returns:
            History of timestamped values from database

        TODO
        """
        raise NotImplementedError
