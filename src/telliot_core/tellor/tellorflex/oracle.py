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


class TellorFlexOracleContract(Contract):
    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None

        entries = contract_directory.find(chain_id=chain_id, name="tellorflex-oracle")
        if not entries:
            raise Exception(f"Tellorflex oracle contract not found on chain_id {chain_id}")
        contract_info = entries[0]

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_governance_address(self) -> Optional[str]:

        governance_address, status = await self.read("getGovernanceAddress")

        if status.ok:
            return str(governance_address)
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None

    async def get_reporting_lock(self) -> Optional[int]:

        lock, status = await self.read("getReportingLock")

        if status.ok:
            return int(lock)
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None

    async def get_stake_amount(self) -> Optional[float]:

        stake, status = await self.read("getStakeAmount")

        if status.ok:
            stake_in_trb = int(stake) / 1.0e18
            return stake_in_trb
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None

    async def get_time_of_last_new_value(self) -> Tuple[Optional[TimeStamp], ResponseStatus]:

        tlnv, status = await self.read("getTimeOfLastNewValue")

        if status.ok:
            return TimeStamp(tlnv), status
        else:
            return None, status

    async def get_token_address(self) -> Optional[str]:

        token_address, status = await self.read("getTokenAddress")

        if status.ok:
            return str(token_address)
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None

    async def get_total_stake_amount(self) -> Optional[float]:

        total_stake, status = await self.read("getTotalStakeAmount")

        if status.ok:
            total_stake_trb = int(total_stake) / 1.0e18
            return total_stake_trb
        else:
            logger.error("Error reading TellorFlexOracleContract")
            logger.error(status)
            return None

    async def get_staker_info(self, staker_address: str) -> Tuple[Optional[Any], ResponseStatus]:

        staker_info, status = await self.read(func_name="getStakerInfo", _staker=staker_address)

        return staker_info, status

    async def get_new_value_count_by_qeury_id(self, query_id: bytes) -> Tuple[int, ResponseStatus]:
        count, status = await self.read(func_name="getNewValueCountbyQueryId", _queryId=query_id)
        return count, status


if __name__ == "__main__":
    import asyncio
    from telliot_core.apps.core import TelliotCore

    async def hello_world() -> None:
        async with TelliotCore(chain_id=137) as core:

            flex = core.get_tellorflex_contracts()

            t = await flex.oracle.get_time_of_last_new_value()

            print(f"Hello world!  Data was just submitted to TellorFlex on: {t}")

    asyncio.run(hello_world())
