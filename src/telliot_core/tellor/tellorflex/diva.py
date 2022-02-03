import logging
from typing import Any
from typing import Optional
from typing import Tuple

from chained_accounts import ChainedAccount

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp


logger = logging.getLogger(__name__)


class DivaProtocolContract(Contract):
    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None and chain_id in (137, 80001, 3) # Polygon chains & Ropsten

        contract_info = contract_directory.find(chain_id=chain_id, name="tellorflex-oracle")[0]
        if not contract_info:
            raise Exception(f"Tellorflex oracle contract not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_pool_parameters(self) -> Optional[str]:

        governance_address, status = await self.read("getGovernanceAddress")

        if status.ok:
            return str(governance_address)
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None


class DivaTellorOracleContract(Contract):
    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None and chain_id in (137, 80001, 3) # Polygon chains & Ropsten

        contract_info = contract_directory.find(chain_id=chain_id, name="tellorflex-oracle")[0]
        if not contract_info:
            raise Exception(f"Tellorflex oracle contract not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_min_period_undisputed(self) -> Optional[str]:

        governance_address, status = await self.read("getGovernanceAddress")

        if status.ok:
            return str(governance_address)
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None
    
    async def set_final_reference_value(self) -> Optional[str]:

        governance_address, status = await self.read("getGovernanceAddress")

        if status.ok:
            return str(governance_address)
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None