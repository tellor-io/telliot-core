from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List
from typing import Optional


@dataclass
class ContractInfo:
    org: str
    name: str
    chain_id: int
    address: str
    abi: Optional[List[Any]] = field(repr=False)


@dataclass
class ContractDirectory:
    # Private directory storage
    _contents: List[ContractInfo] = field(default_factory=list)

    def add_contract(self, info: ContractInfo) -> None:
        self._contents.append(info)

    def find(
        self,
        *,
        org: str = "tellor",
        name: Optional[str] = None,
        address: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> List[ContractInfo]:
        result = []
        for info in self._contents:
            if info.org != org:
                continue
            if chain_id is not None:
                if chain_id != info.chain_id:
                    continue
            if name is not None:
                if info.name is not name:
                    continue
            if address is not None:
                if info.address is not address:
                    continue

            result.append(info)

        return result
