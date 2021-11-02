from dataclasses import dataclass
from typing import Any
from typing import Optional

from telliot.model.base import Base
from telliot.model.endpoints import RPCEndpoint


@dataclass
class ResponseStatus(Base):
    ok: bool = True
    error: Optional[str] = None
    e: Optional[Exception] = None


@dataclass
class ContractResponse(Base):

    ok: bool

    result: Optional[Any]

    error: Optional[Exception]

    error_msg: Optional[str]

    endpoint: Optional[RPCEndpoint]
