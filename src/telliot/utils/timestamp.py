from datetime import datetime
from datetime import timezone


def now() -> datetime:
    """Return now as a UTC timestamp"""
    return datetime.now(timezone.utc)
