import asyncio
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

from telliot.pricing.price_service import WebPriceService


@dataclass
class DataSource(ABC):
    """Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed` algorithm
    """

    #: Unique data source identifier
    id: str = ""

    #: Descriptive name
    name: str = "Data Source"

    @abstractmethod
    async def fetch(self) -> Any:
        """Fetch Data

        Returns:
            Data returned from source
        """
        raise NotImplementedError


@dataclass
class CurrentAssetPrice(DataSource):
    """Current Asset Price

    The Current Asset Price data source retrieves the price of an `asset`
    in the specified `currency` from a list of one or more `WebPriceService`s.
    """

    #: Descriptive name
    name: str = "Current Asset Price"

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: List of Price Services
    services: List[WebPriceService] = field(default_factory=list)

    #: List of previously fetched values, each tagged with a timestamp
    values: List[Tuple[datetime, Optional[float]]] = field(
        default_factory=list)

    async def fetch(self) -> List[Optional[float]]:
        price_list = await asyncio.gather(
            *[
                service().get_price(self.asset, self.currency)
                for service in self.services
            ]
        )
        timestamp = datetime.now()
        self.values.append((timestamp, price_list))
        return price_list


@dataclass
class Constant(DataSource):
    """A dumb data source that just fetches a constant value"""

    #: Descriptive name
    name: str = "Data Source"

    #: Constant value
    value: Any = None

    def __init__(self, value, **kwargs):
        self.value = value
        super().__init__(**kwargs)

    async def fetch(self):
        return self.value
