from typing import Any, Dict


def dict2argstr(d: Dict[str, Any]) -> str:
    """Convert a dict to a string of kwd=arg pairs
    """
    return ",".join("{!s}={!r}".format(key, val) for (key, val) in d.items())
