from typing import Any
from typing import Dict


def dict2argstr(d: Dict[str, Any]) -> str:
    """Convert a dict to a text of kwd=arg pairs"""
    return ",".join("{!s}={!r}".format(key, val) for (key, val) in d.items())
