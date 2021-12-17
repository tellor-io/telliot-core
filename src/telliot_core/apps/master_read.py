from dataclasses import dataclass
from typing import Optional

from telliot_core.apps.core import TelliotCore
from telliot_core.apps.oracle_read import ReadRespType

staker_status_map = {
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


async def getStakerInfo(address: Optional[str] = None) -> ReadRespType:
    """Get Staker Info"""
    core = TelliotCore.get()

    if address is None:
        staker = core.get_default_staker()
        address = staker.address

    result, status = await core.tellorx.master.read("getStakerInfo", _staker=address)

    currentStatus, date_staked = result

    return (staker_status_map[currentStatus], date_staked), status


async def disputesById(dispute_id: int) -> ReadRespType:
    core = TelliotCore.get()

    response, status = await core.tellorx.master.read("disputesById", dispute_id)

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
