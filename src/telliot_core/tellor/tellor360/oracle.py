import logging
from typing import Optional
from typing import Tuple

from chained_accounts import ChainedAccount

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp


logger = logging.getLogger(__name__)


class Tellor360OracleContract(Contract):
    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None

        contract_info = contract_directory.find(chain_id=chain_id, name="tellor360-oracle")
        if not contract_info:
            raise Exception(f"Tellor360 oracle contract not found on chain_id {chain_id}")

        contract_abi = contract_info[0].get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info[0].address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_time_of_last_new_value(self) -> Tuple[Optional[TimeStamp], ResponseStatus]:

        tlnv, status = await self.read("getTimeOfLastNewValue")

        if status.ok:
            return TimeStamp(tlnv), status
        else:
            return None, status
