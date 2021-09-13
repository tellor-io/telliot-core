from datetime import datetime
from typing import Generic, TypeVar

from pydantic import Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class Answer(GenericModel, Generic[T]):
    """ Base class for all answers to Tellor queries

    """

    #: Value
    val: T

    def __init__(self, val, **data):
        super().__init__(val=val, **data)

    def to_bytes(self) -> bytes:
        """ Convert value to bytes as stored on the blockchain

        Returns:
            Byte representation of value
        """
        raise NotImplemented

    def from_bytes(self, bytesval: bytes) -> T:
        """ Convert blockchain bytes to value

        Returns:
            Value
        """
        raise NotImplemented


class TimeStampedAnswer(Answer[T], Generic[T]):
    """ A time-stamped answer for answer data feeds or other time series

    """

    #: Timestamp
    ts: datetime = Field(default_factory=datetime.now)


class TimeStampedFixed(TimeStampedAnswer[float]):
    """ A time-stamped fixed point value

    """

    #: Precision (in decimals)
    decimals = 6

    int = property(lambda self: round(self.val * 10 ** self.decimals))

    def __init__(self, val, **data):
        super().__init__(val=val, **data)
        stored_float = float(self.int) / 10 ** self.decimals
        if stored_float != val:
            print('WARNING: float value {} rounded to {}'.format(val,
                                                                 stored_float))
        self.val = stored_float


class TimeStampedFloat(TimeStampedAnswer[float]):
    """ A time-stamped floating point value

    """
    pass
