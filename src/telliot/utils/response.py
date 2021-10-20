from typing import Any, Optional
from telliot.utils.base import Base
from telliot.model.endpoints import RPCEndpoint

class ContractResponse(Base):

    ok: bool

    result: Optional[Any]

    error: Optional[Exception]

    error_msg: Optional[str]

    endpoint: Optional[RPCEndpoint]