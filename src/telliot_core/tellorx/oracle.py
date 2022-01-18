from typing import Any
from typing import Optional
from typing import Tuple

from telliot_core.contract.contract import Contract
from telliot_core.directory import directory_config_file
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp

ReadRespType = Tuple[Any, ResponseStatus]


class TellorxOracleContract(Contract):
    def __init__(self, node: RPCEndpoint, private_key: str = ""):
        directory = directory_config_file().get_config()
        contract_info = directory.find(chain_id=node.chain_id, name="oracle")[0]
        if not contract_info:
            raise Exception(
                f"TellorX oracle contract not found on chain_id {node.chain_id}"
            )
        assert contract_info.abi

        super().__init__(
            address=contract_info.address[node.chain_id],
            abi=contract_info.abi,
            node=node,
            private_key=private_key,
        )

    async def getBlockNumberByTimestamp(
        self, queryId: str, timestamp: int
    ) -> ReadRespType:

        result, status = await self.read(
            "getBlockNumberByTimestamp", _queryId=queryId, _timestamp=timestamp
        )

        return result, status

    async def getCurrentReward(self, queryId: str) -> ReadRespType:

        result, status = await self.read("getCurrentReward", _queryId=queryId)

        if status.ok:
            (tips, reward) = result
            return (tips / 1.0e18, reward / 1.0e18), status
        else:
            return (0, 0), status

    async def getCurrentValue(self, queryId: str) -> ReadRespType:

        result, status = await self.read("getCurrentValue", _queryId=queryId)

        return result, status

    async def getReportingLock(self) -> ReadRespType:

        result, status = await self.read("getReportingLock")

        return result, status

    async def getReporterByTimestamp(
        self, queryId: str, timestamp: int
    ) -> ReadRespType:

        result, status = await self.read(
            "getReporterByTimestamp", _queryId=queryId, _timestamp=timestamp
        )

        return result, status

    async def getReporterLastTimestamp(
        self, reporter: Optional[str] = None
    ) -> ReadRespType:

        result, status = await self.read("getReporterLastTimestamp", _reporter=reporter)

        return result, status

    async def getReportsSubmittedByAddress(
        self, reporter: Optional[str] = None
    ) -> ReadRespType:

        result, status = await self.read(
            "getReportsSubmittedByAddress", _reporter=reporter
        )

        return result, status

    async def getReportTimestampByIndex(self, queryId: str, index: int) -> ReadRespType:

        result, status = await self.read(
            "getReportTimestampByIndex", _queryId=queryId, _index=index
        )

        return result, status

    async def getTimeBasedReward(self) -> Tuple[float, ResponseStatus]:
        result, status = await self.read("getTimeBasedReward")
        if status.ok:
            trb_reward = float(result) / 1.0e18  # type: ignore
        else:
            trb_reward = float(0)
        return trb_reward, status

    async def getTimestampCountById(self, queryId: str) -> ReadRespType:

        result, status = await self.read("getTimestampCountById", _queryId=queryId)

        return result, status

    async def getTimeOfLastNewValue(self) -> ReadRespType:

        result, status = await self.read("getTimeOfLastNewValue")

        if status.ok:
            t = TimeStamp(result)
        else:
            t = None

        return t, status

    async def getTimestampIndexByTimestamp(
        self, queryId: str, timestamp: int
    ) -> ReadRespType:

        result, status = await self.read(
            "getTimestampIndexByTimestamp", _queryId=queryId, _timestamp=timestamp
        )

        return result, status

    async def getTipsById(self, queryId: str) -> ReadRespType:

        tips, status = await self.read("getTipsById", _queryId=queryId)

        return float(tips) / 1.0e18, status  # type: ignore

    async def getTipsByUser(self, user: Optional[str] = None) -> ReadRespType:

        result, status = await self.read("getTipsByUser", _user=user)

        return result, status

    async def getValueByTimestamp(self, queryId: str, timestamp: int) -> ReadRespType:

        result, status = await self.read(
            "getValueByTimestamp", _queryId=queryId, _timestamp=timestamp
        )

        return result, status

    async def verify(self) -> ReadRespType:

        result, status = await self.read("verify")

        return result, status
