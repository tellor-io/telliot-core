import logging
from typing import Optional

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.timestamp import TimeStamp

logger = logging.getLogger(__name__)


class TellorFlexTokenContract(Contract):
    def __init__(self, node: RPCEndpoint, private_key: str = ""):
        chain_id = node.chain_id
        assert chain_id is not None

        contract_info = contract_directory.find(chain_id=chain_id, name="tellorflex-token")[0]
        if not contract_info:
            raise Exception(f"Tellorflex token contract not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            private_key=private_key,
        )