from datetime import datetime
from datetime import timezone
from typing import Any
from typing import Generic
from typing import TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

T = TypeVar("T")


class Answer(GenericModel, Generic[T]):
    """Base class for all answers to Tellor queries"""

    #: Value
    val: T

    def __init__(self, val: T, **data: Any):
        super().__init__(val=val, **data)

    # def to_bytes(self) -> bytes:
    #     """Convert value to bytes as stored on the blockchain

    #     Returns:
    #         Byte representation of value
    #     """
    #     raise NotImplementedError

    # def from_bytes(self, bytesval: bytes) -> T:
    #     """Convert blockchain bytes to value

    #     Returns:
    #         Value
    #     """
    #     raise NotImplementedError


def datetime_now_utc() -> datetime:
    return datetime.now(timezone.utc)


class TimeStampedAnswer(Answer[T], Generic[T]):
    """A time-stamped answer for answer data feeds or other time series

    Note that mypy is OK if Generic[T] is removed, but pytantic
    fails if it is removed.
    """

    #: UTC Timestamp
    ts: datetime = Field(default_factory=datetime_now_utc)


class TimeStampedFixed(TimeStampedAnswer[float]):
    """A time-stamped fixed point value"""

    #: Precision (in decimals)
    decimals = 6

    int = property(lambda self: round(self.val * 10 ** self.decimals))

    def __init__(self, val: float, **data: Any):
        super().__init__(val=val, **data)
        stored_float = float(self.int) / 10 ** self.decimals
        if stored_float != val:
            print("WARNING: float value {} rounded to {}".format(val, stored_float))
        self.val = stored_float


class TimeStampedFloat(TimeStampedAnswer[float]):
    """A time-stamped floating point value"""

    pass
