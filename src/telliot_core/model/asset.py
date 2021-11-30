from dataclasses import dataclass

from clamfig import Serializable


@dataclass
class Asset(Serializable):
    id: str
    name: str
