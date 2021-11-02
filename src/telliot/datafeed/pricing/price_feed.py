import asyncio
from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import List
from typing import Optional

from telliot.answer import TimeStampedAnswer
from telliot.answer import TimeStampedFixed
from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.data_source import DataSource


@dataclass
class PriceFeed(DataFeed, ABC):
    #: Asset
    asset: str

    #: Currency of returned price
    currency: str

    #: Callable algorithm that accepts an iterable of floats
    algorithm: Callable[..., float]

    #: Data feed sources
    sources: List[DataSource] = field(default_factory=list)

    async def update_sources(self) -> List[TimeStampedAnswer[Any]]:
        """Update data feed sources

        Returns:
            Dictionary of updated source values, mapping data source UID
            to the time-stamped answer for that data source
        """

        async def gather_inputs() -> List[TimeStampedAnswer[Any]]:
            sources = self.sources
            values = await asyncio.gather(
                *[source.update_value() for source in sources]
            )
            return values  # type: ignore

        inputs = await gather_inputs()

        return inputs

    async def update_value(self) -> Optional[TimeStampedAnswer[Any]]:
        # async def update_value(self) -> Tuple[ResponseStatus, Any, Optional[datetime]]:

        """Update current value with time-stamped value fetched from source

        Args:
            store:  If true and applicable, updated value will be stored
                    to the database

        Returns:
            Current time-stamped value
        """
        values = await self.update_sources()

        prices = []
        for value in values:
            # Check for valid answers
            timestamped_answer = value
            price = timestamped_answer.val
            prices.append(price)

        result = self.algorithm(prices)
        tsval = TimeStampedFixed(val=result)
        self._value = tsval

        # tstamp = now()

        print(
            "Feed Price: {} reported at time {}".format(self.value.val, self.value.ts)
        )

        # return ResponseStatus(True), self.value, tstamp
        return self._value

    async def get_history(self, n: int = 0) -> List[TimeStampedFixed]:
        """Get data source history from database

        Args:
            n:  If n > 0, get n datapoints from database, otherwise get all
                available datapoints.

        Returns:
            History of timestamped values from database

        TODO
        """
        raise NotImplementedError
