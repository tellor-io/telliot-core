from typing import Callable
from typing import Any
from pydantic import BaseModel

from telliot.base import Answer


class OracleQuery(BaseModel):
    """ Base class for all DAO-approved tellor queries

    """

    #: Unique Query ID
    uid: str

    #: Unique Contract Request ID
    request_id: int

    #: Question
    question: str

    #: Answer type
    answer_type: Callable[..., Answer[Any]]
