from dataclasses import dataclass
from typing import Optional

from telliot.model.base import Base


@dataclass
class ResponseStatus(Base):
    ok: bool = True
    error: Optional[str] = None
    e: Optional[Exception] = None
