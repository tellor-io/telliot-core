from typing import Callable
from typing import List
from typing import Optional

from telliot.answer import TimeStampedFixed
from telliot.datafeed.data_feed import DataFeed

import json


class AssetPriceFeed(DataFeed):
    #: Override data type for this feed
    value: Optional[TimeStampedFixed]

    #: Asset
    asset: str

    #: Currency of returned pricd
    currency: str

    #: Callable algorithm that accepts an iterable of floats
    algorithm: Callable[..., float]

    async def update_value(self, store: bool = False) -> Optional[TimeStampedFixed]:
        """Update current value with time-stamped value fetched from source

        Args:
            store:  If true and applicable, updated value will be stored
                    to the database

        Returns:
            Current time-stamped value
        """
        sources = await self.update_sources()

        prices = []
        for key in sources:

            # Check for valid answers
            if sources[key] is not None:
                timestamped_answer = sources[key]
                price = timestamped_answer.val
                prices.append(price)
                # print(
                #     "Source Price: {} reported from {} at time {}".format(
                #         price, key, timestamped_answer.ts
                #     )
                # )

        result = self.algorithm(prices)

        self.value = TimeStampedFixed(result)

        print(
            "Feed Price: {} reported from {} at time {}".format(
                self.value.val, self.uid, self.value.ts
            )
        )

        if store:
            await self.store_value()

        return self.value

    async def get_history(self, n: int = 0) -> List[TimeStampedFixed]:  # type: ignore
        """Get data source history from database

        Args:
            n:  If n > 0, get n datapoints from database, otherwise get all
                available datapoints.

        Returns:
            History of timestamped values from database

        TODO
        """
        raise NotImplementedError
