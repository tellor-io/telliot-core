""" :mod:`telliot.datafeed.data_source`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import TypeVar

import requests
from pydantic import BaseModel
from telliot.answer import TimeStampedAnswer

T = TypeVar("T")


class DataSource(BaseModel, ABC):
    """Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed`
    """

    #: Unique data source identifier
    uid: str = ""

    #: Descriptive name
    name: str = ""

    #: Current time-stamped value of the data source or None
    value: Optional[TimeStampedAnswer[Any]]

    @abstractmethod
    async def update_value(
        self, store: bool = False
    ) -> Optional[TimeStampedAnswer[Any]]:
        """Update current value with time-stamped value fetched from source

        Args:
            store:  If true and applicable, updated value will be stored
                    to the database

        Returns:
            Current time-stamped value
        """
        raise NotImplementedError


class DataSourceDb(DataSource, ABC):
    """A data source that can store and retrieve values from a database"""

    async def load_value(self) -> TimeStampedAnswer[Any]:
        """Update current value with time-stamped value fetched from database"""
        raise NotImplementedError

    async def store_value(self) -> None:
        """Store current time-stamped value to database"""

        value = self.value.val if self.value else None
        timestamp = str(self.value.ts) if self.value else None
        data = {"uid": self.uid, "value": value, "timestamp": timestamp}

        url = "http://127.0.0.1:8000/data/"

        def store() -> Dict[str, Any]:
            """Send post request to local db."""
            with requests.Session() as s:
                try:
                    r = s.post(url, json=data)
                    json_data = r.json()
                    return {"response": json_data}

                except requests.exceptions.ConnectTimeout as e:
                    return {"error": "Timeout Error", "exception": e}

                except Exception as e:
                    return {"error": str(type(e)), "exception": e}

        _ = store()

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


# class ConstantSource(DataSource):
#     """A simple data source that fetches a constant value"""
#
#     #: Descriptive name
#     name: str = "Constant"
#
#     #: Constant value
#     constant_value: float
#
#     def __init__(self, value: float, **kwargs: Any):
#         super().__init__(constant_value=value, **kwargs)
#
#     async def update_value(self):
#         return self.value
#
#
# class RandomSource(DataSourceDb):
#     """A random data source
#
#     Returns a random floating point number in the range [0.0, 1.0).
#     """
#
#     #: Descriptive name
#     name: str = "Random"
#
#     async def update_value(self):
#         self.value = random.random()
#         return random.random()
