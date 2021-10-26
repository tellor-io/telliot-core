""" Feeder database module

This module creates a database with a model to store off-chain data.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List

import databases
import requests
import sqlalchemy

from telliot.answer import TimeStampedAnswer
from telliot.datafeed.data_source import DataSource

DATABASE_URL = "sqlite:///./test.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

offchain = sqlalchemy.Table(
    "offchain",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("uid", sqlalchemy.String),
    sqlalchemy.Column("value", sqlalchemy.String),
    sqlalchemy.Column("timestamp", sqlalchemy.DateTime),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

metadata.create_all(engine)


class FeedDataBaseMixin(ABC):
    """A Mixin Class that provides an interface to the feed database

    """

    @abstractmethod
    async def load_value(self) -> TimeStampedAnswer[Any]:
        """Update current value with time-stamped value fetched from database"""
        raise NotImplementedError

    @abstractmethod
    async def get_history(self, n: int = 0) -> List[TimeStampedAnswer[Any]]:
        """Get data source history from database

        Args:
            n:  If n > 0, get n datapoints from database, otherwise get all
                available datapoints.

        Returns:
            History of timestamped values from database
        """
        raise NotImplementedError

    # async def store_value(self) -> None:
    #     """Store current time-stamped value to database"""
    #
    #     value = self.value.val if self.value else None
    #     timestamp = str(self.value.ts) if self.value else None
    #     data = {"uid": self.uid, "value": value, "timestamp": timestamp}
    #
    #     url = "http://127.0.0.1:8000/data/"
    #
    #     def store() -> Dict[str, Any]:
    #         """Send post request to local db."""
    #         with requests.Session() as s:
    #             try:
    #                 r = s.post(url, json=data)
    #                 json_data = r.json()
    #                 return {"response": json_data}
    #
    #             except requests.exceptions.ConnectTimeout as e:
    #                 return {"error": "Timeout Error", "exception": e}
    #
    #             except Exception as e:
    #                 return {"error": str(type(e)), "exception": e}
    #
    #     _ = store()
