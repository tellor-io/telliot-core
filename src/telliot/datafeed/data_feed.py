import asyncio
from typing import Any
from typing import Dict

from telliot.answer import TimeStampedAnswer
from telliot.datafeed.data_source import DataSource
from telliot.datafeed.data_source import DataSourceDb


class DataFeed(DataSourceDb):
    """Data feed"""

    #: Data feed sources
    sources: Dict[str, DataSource]

    #: Unique ID of tellor query supported by this feed
    request_id: str

    async def update_sources(self) -> Dict[str, TimeStampedAnswer[Any]]:
        """Update data feed sources

        Returns:
            Dictionary of updated source values, mapping data source UID
            to the time-stamped answer for that data source
        """

        async def gather_inputs() -> Dict[str, TimeStampedAnswer[Any]]:
            keys = self.sources.keys()
            values = await asyncio.gather(
                *[self.sources[key].update_value() for key in keys]
            )
            return dict(zip(keys, values))

        return await gather_inputs()
