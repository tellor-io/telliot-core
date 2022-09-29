from dataclasses import dataclass
from typing import Optional

from chained_accounts import ChainedAccount
from eth_utils import to_checksum_address

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory as directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.tellor.tellorx.oracle import ReadRespType
from telliot_core.utils.timestamp import TimeStamp

account_status_map = {
    0: "NotStaked",
    1: "Staked",
    2: "LockedForWithdraw",
    3: "InDispute",
    4: "disbursed",
    5: "slashed",
}


@dataclass
class DisputeReport:
    hash: str
    tally: int
    executed: bool
    disputeVotePassed: bool
    isPropFork: bool
    reportedMiner: str
    reportingParty: str
    proposedForkAddress: str


class TellorxMasterContract(Contract):
    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):

        chain_id = node.chain_id
        assert chain_id is not None

        entries = directory.find(name="tellorx-master", chain_id=chain_id)
        if not entries:
            raise Exception(f"TellorX master contract not found on chain_id {chain_id}")
        contract_info = entries[0]
        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def getStakerInfo(self, address: str) -> ReadRespType:
        """Get Staker Info"""

        address = to_checksum_address(address)

        result, status = await self.read("getStakerInfo", _staker=address)

        if status.ok:
            current_status, ts_staked = result
            staker_status = account_status_map[current_status]
            date_staked = TimeStamp(ts_staked)
            return (staker_status, date_staked), status
        else:
            return (None, None), status

    async def disputesById(self, dispute_id: int) -> ReadRespType:

        response, status = await self.read("disputesById", dispute_id)

        if status.ok:
            result = DisputeReport(
                hash=f"0x{response[0].hex()}",
                tally=response[1],
                executed=response[2],
                disputeVotePassed=response[3],
                isPropFork=response[4],
                reportedMiner=response[5],
                reportingParty=response[6],
                proposedForkAddress=response[7],
            )
            return result, status
        else:
            return None, status
