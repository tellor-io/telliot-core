""" Telliot registry module"""
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple

from clamfig import Serializable

ModelStateType = List[Tuple[str, Dict[str, Any]]]


class RegisteredModel(Serializable):
    pass
