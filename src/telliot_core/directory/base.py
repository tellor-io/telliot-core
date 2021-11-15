from typing import Any
from typing import Dict
from typing import TypedDict


# Container for contract access information
class ContractInfo(TypedDict):
    address: str
    abi: Dict[Any, Any]


# Mapping of contract name to Contract Info
ContractSet = Dict[str, ContractInfo]

# Mapping of chain_id to set of contracts deployed on that chain
Directory = Dict[int, ContractSet]
