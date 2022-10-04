import logging
from typing import Optional
from typing import Tuple

from chained_accounts import ChainedAccount
from web3.exceptions import ContractLogicError

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.response import ResponseStatus


logger = logging.getLogger(__name__)


class Tellor360AutopayContract(Contract):
    """Tellor360 Autopay contract getter"""

    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None

        contract_info = contract_directory.find(chain_id=chain_id, name="tellor360-autopay")
        if not contract_info:
            raise Exception(f"Tellor360 autopay contract not found on chain_id {chain_id}")
        contract_abi = contract_info[0].get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info[0].address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_current_tip(self, query_id: bytes) -> Tuple[Optional[int], ResponseStatus]:
        tip_amount, status = await self.read(func_name="getCurrentTip", _queryId=query_id)
        if status.ok:
            return tip_amount, status
        # autopay contract reverts when tip amount is zero
        # instead of returning 0, not sure why
        elif type(status.e) == ContractLogicError:
            tip_amount = 0
            status.ok = True
            return tip_amount, status
        else:
            return None, status
