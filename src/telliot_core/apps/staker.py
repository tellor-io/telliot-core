from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

from telliot_core.apps.config import ConfigOptions
from telliot_core.model.base import Base


@dataclass
class Staker(Base):
    tag: str
    address: str
    private_key: str
    chain_id: int


default_stakers = [
    Staker(
        tag="my_mainnet_staker",
        address="0x00001234",
        private_key="0x00009999",
        chain_id=1,
    ),
    Staker(
        tag="my_rinkeby_staker",
        address="0x00005678",
        private_key="0x00009999",
        chain_id=4,
    ),
]


@dataclass
class StakerList(ConfigOptions):
    stakers: List[Staker] = field(default_factory=lambda: default_stakers)

    def get(
        self,
        tag: Optional[str] = None,
        address: Optional[str] = None,
        private_key: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> List[Staker]:
        """Returns a list of stakers matching the search parameters"""

        stakers = []
        for staker in self.stakers:
            if tag is not None:
                if tag != staker.tag:
                    continue
            if address is not None:
                if address.lower() != staker.address.lower():
                    continue
            if private_key is not None:
                if private_key.lower() != staker.private_key.lower():
                    continue
            if chain_id is not None:
                if chain_id != staker.chain_id:
                    continue

            stakers.append(staker)

        return stakers
