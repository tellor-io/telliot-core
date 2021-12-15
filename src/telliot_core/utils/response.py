from dataclasses import dataclass
from typing import Callable
from typing import Optional

from telliot_core.model.base import Base


@dataclass
class ResponseStatus(Base):
    ok: bool = True
    error: Optional[str] = None
    e: Optional[Exception] = None


def error_status(
    note: str,
    e: Optional[Exception] = None,
    log: Optional[Callable[[str], None]] = None,
) -> ResponseStatus:
    """Helper for reporting and logging error status"""

    status = ResponseStatus()
    status.ok = False

    if e:
        msg = f"{note}: {repr(e)}"
    else:
        status.e = e
        msg = f"{note}"

    status.error = str(msg)

    if log:
        log(msg)

    return status
