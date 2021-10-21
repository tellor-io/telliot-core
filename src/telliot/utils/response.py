from typing import Any
from typing import Optional

from telliot.model.endpoints import RPCEndpoint
from telliot.utils.base import Base


class ResponseStatus(Base):
    ok: bool = True
    error: Optional[str] = None
    e: Optional[Exception] = None


class ContractResponse(Base):

    ok: bool

    result: Optional[Any]

    error: Optional[Exception]

    error_msg: Optional[str]

    endpoint: Optional[RPCEndpoint]
