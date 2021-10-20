from typing import Any
from typing import Optional

from telliot.model.endpoints import RPCEndpoint
from telliot.utils.base import Base


class ContractResponse(Base):

    ok: bool

    result: Optional[Any]

    error: Optional[Exception]

    error_msg: Optional[str]

    endpoint: Optional[RPCEndpoint]
