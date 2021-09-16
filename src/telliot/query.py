from typing import Any
from typing import Callable

from pydantic import BaseModel
from telliot.answer import Answer


class OracleQuery(BaseModel):
    """Base class for all DAO-approved tellor queries"""

    #: Unique Query ID
    uid: str

    #: Unique Contract Request ID
    request_id: int

    #: Question
    question: str

    #: Answer type
    answer_type: Callable[..., Answer[Any]]
