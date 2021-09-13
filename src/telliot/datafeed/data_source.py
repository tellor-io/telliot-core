from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional
from typing import TypeVar

from pydantic import BaseModel

from telliot.base import TimeStampedAnswer
from telliot.base import TimeStampedFloat
from telliot.pricing.price_service import WebPriceService

T = TypeVar('T')


class DataSource(BaseModel, ABC):
    """ Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed`
    """

    #: Unique data source identifier
    uid: str = ''

    #: Descriptive name
    name: str = ''

    #: Current time-stamped value of the data source or None
    value: Optional[TimeStampedAnswer]

    @abstractmethod
    async def fetch_value(self) -> None:
        """Update current value with time-stamped value fetched from source

        Returns:
            Current time-stamped value
        """
        raise NotImplementedError


class DataSourceDb(BaseModel, ABC):
    """ A data source with the ability to recorded and restore history

    """

    async def load_value(self) -> None:
        """Update current value with time-stamped value fetched from database

        """
        raise NotImplementedError

    async def store_value(self) -> None:
        """ Store current time-stamped value to database

        """
        raise NotImplementedError

    async def get_history(self, n: int = 0) -> List[T]:
        """ Get data source history from database

        Args:
            n:  If n > 0, get n datapoints from database, otherwise get all
                available datapoints.

        Returns:
            History of timestamped values from database
        """
        raise NotImplementedError


class AssetPriceSource(DataSourceDb):
    """Current Asset Price

    The Current Asset Price data source retrieves the price of an asset
    in the specified current from a `WebPriceService`.
    """

    #: Current time-stamped value of the data source or None
    #: Override base class type
    value: Optional[TimeStampedFloat]

    #: Asset symbol
    asset: str = ''

    #: Price currency symbol
    currency: str = ''

    #: Price Service
    service: WebPriceService

    #: Pydantic hack to allow general type-checking
    class Config:
        arbitrary_types_allowed = True

    async def fetch_value(self) -> TimeStampedFloat:
        """Update current value with time-stamped value fetched from source

        Returns:
            Current time-stamped value
        """
        price = await self.service.get_price(self.asset, self.currency)

        self.value = price

        return price

    async def load_value(self) -> None:
        """Update current value with time-stamped value fetched from database

        TODO
        """
        raise NotImplementedError

    async def store_value(self) -> None:
        """ Store current time-stamped value to database

        TODO
        """
        raise NotImplementedError

    async def get_history(self, n: int = 0) -> List[T]:
        """ Get data source history from database

        Args:
            n:  If n > 0, get n datapoints from database, otherwise get all
                available datapoints.

        Returns:
            History of timestamped values from database

        TODO
        """
        raise NotImplementedError


class Constant(DataSource):
    """A simple data source that fetches a constant value"""

    #: Descriptive name
    name: str = "Constant"

    def __init__(self, value, **kwargs):
        super().__init__(value=value, **kwargs)

    async def fetch_value(self):
        return self.value
