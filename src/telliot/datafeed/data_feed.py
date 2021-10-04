import asyncio
from typing import Any
from typing import Dict
from typing import Optional

from telliot.answer import TimeStampedAnswer
from telliot.datafeed.data_source import DataSource
from telliot.datafeed.data_source import DataSourceDb
from telliot.query_registry import query_registry
from telliot.query import OracleQuery

class DataFeed(DataSourceDb):
    """Data feed"""

    #: Data feed sources
    sources: Dict[str, DataSource]

    #: Unique Query ID supported by this feed
    qid: str

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

    def get_query(self) -> Optional[OracleQuery]:
        """ Get target query for this Data Feed

        Returns:
            Target query for this DataFeed or None if not found
        """
        return query_registry.queries.get(self.qid, None)
