""" telliot.datafeed.data_source

"""
import random
from abc import ABC
from abc import abstractmethod
from datetime import datetime
from typing import Any
from typing import Optional
from typing import Tuple
from dataclasses import dataclass
from telliot.model.base import Base
from telliot.utils.response import ResponseStatus
from telliot.utils.timestamp import now
from dataclasses import dataclass, field
from telliot.answer import TimeStampedAnswer

# SourceOutputType = Tuple[ResponseStatus, Any, Optional[datetime]]


@dataclass
class DataSource(Base, ABC):
    """Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed`
    """

    value = property(lambda self: self._value)

    # Private storage for fetched value
    _value: Optional[Any] = field(default=None, init=False, repr=False)


    @abstractmethod
    async def update_value(self) -> Optional[TimeStampedAnswer[Any]]:
        # async def update_value(self) -> SourceOutputType:

        """Update current value with time-stamped value fetched from source

        Returns:
            Current time-stamped value
        """
        raise NotImplementedError


@dataclass
class RandomSource(DataSource):
    """A random data source

    Returns a random floating point number in the range [0.0, 1.0).
    """

    async def update_value(self):

        self._value = TimeStampedAnswer(val = random.random())

        return self.value
        # return ResponseStatus(True), self.value, now()

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
