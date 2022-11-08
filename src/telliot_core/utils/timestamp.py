from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Union


def now() -> datetime:
    """Return now as a UTC timestamp"""
    return datetime.now(timezone.utc)


class TimeStamp:
    """Representation of a timestamp with an integer number of seconds"""

    # Access the underlying unix timestamp
    ts = property(lambda self: self._ts)
    _ts: int

    def __init__(self, ts: Union[int, float]):
        """Create from unix timestamp"""
        self._ts = round(ts)

    @classmethod
    def now(cls) -> "TimeStamp":
        return cls(datetime.now().timestamp())

    def __repr__(self) -> str:
        return f"TimeStamp({self._ts})"

    def __str__(self) -> str:
        return str(self.dt)

    @property
    def dt(self) -> datetime:
        """Timestamp as a datetime object"""
        return datetime.fromtimestamp(self._ts)

    @property
    def age(self) -> Union[timedelta, datetime]:
        age = datetime.now() - self.dt
        rounded_age = age - timedelta(microseconds=age.microseconds)
        return rounded_age
