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

from telliot.answer import TimeStampedAnswer
from telliot.model.registry import RegisteredModel

T = TypeVar("T")


class DataSource(RegisteredModel, ABC):
    """Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed`
    """

    #: Unique data source identifier
    uid: str = ""

    #: Current time-stamped value of the data source or None
    value: Optional[TimeStampedAnswer[Any]]

    @abstractmethod
    async def update_value(self) -> Optional[TimeStampedAnswer[Any]]:
        """Update current value with time-stamped value fetched from source

        Returns:
            Current time-stamped value
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
