""" :mod:`telliot.datafeed.data_feed`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
import asyncio
from typing import Any
from typing import Dict

from telliot.answer import TimeStampedAnswer
from telliot.datafeed.data_source import DataSource
from telliot.datafeed.data_source import DataSourceDb
from telliot.queries.query import OracleQuery


class DataFeed(DataSourceDb):
    """Data feed

    A data feed creates a response value for an
    :class:`~telliot.queries.query.OracleQuery`.
    """

    #: Data feed sources
    sources: Dict[str, DataSource]

    #: Query supported by this data feed
    query: OracleQuery

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
