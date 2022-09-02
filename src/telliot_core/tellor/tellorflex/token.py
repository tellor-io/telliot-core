import logging
from typing import Optional

from chained_accounts import ChainedAccount

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint

logger = logging.getLogger(__name__)


class TokenContract(Contract):
    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None

        if chain_id == 122:
            contract_info = contract_directory.find(chain_id=chain_id, name="wrapped-fuse-token")[0]
        else:
            contract_info = contract_directory.find(chain_id=chain_id, name="trb-token")[0]

        if not contract_info:
            raise Exception(f"Tellorflex token contract not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )
