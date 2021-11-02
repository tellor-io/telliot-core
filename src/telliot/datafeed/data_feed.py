""" telliot.datafeed.data_feed

"""
from abc import ABC
from telliot.datafeed.data_source import DataSource
from telliot.queries.query import OracleQuery
from dataclasses import dataclass

@dataclass
class DataFeed(DataSource, ABC):
    """Data feed

    A data feed is a DataSource that creates a response value for an
    `OracleQuery`.
    """

    #: Query supported by this data feed
    query: OracleQuery

