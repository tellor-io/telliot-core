from dataclasses import dataclass
from typing import Optional

from telliot.answer import TimeStampedFloat
from telliot.datafeed.data_source import DataSource
from telliot.datafeed.pricing.price_service import WebPriceService


@dataclass
class PriceSource(DataSource):
    """Current Asset Price

    The Current Asset Price data source retrieves the price of a coin
    in the specified current from a `WebPriceService`.
    """

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Service
    service: Optional[WebPriceService] = None

    async def update_value(self) -> Optional[TimeStampedFloat]:
        """Update current value with time-stamped value fetched from source

        Returns:
            Current time-stamped value
        """
        tsfloat = await self.service.get_price(self.asset, self.currency)

        self._value = tsfloat

        return self.value

