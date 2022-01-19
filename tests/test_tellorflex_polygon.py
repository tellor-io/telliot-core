

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorflex.oracle import TellorflexOracleContract
import pytest


# CID = 80001
from telliot_core.utils.timestamp import TimeStamp

CID = 137


@pytest.mark.asyncio
async def test_main():

    async with TelliotCore(chain_id=CID) as core:

        c = TellorflexOracleContract(node=core.endpoint)
        c.connect()

        governance_address = await c.get_governance_address()
        assert governance_address == '0x2cFC5bCE14862D46fBA3bb46A36A8b2d7E4aC040'

        stake_amount = await c.get_stake_amount()
        assert stake_amount == 10.0
        print(stake_amount)

        tlnv = await c.get_time_of_last_new_value()
        assert isinstance(tlnv, TimeStamp)
        print(tlnv)

        lock = await c.get_reporting_lock()
        print(lock)

        token_address = await c.get_token_address()
        assert token_address == '0xE3322702BEdaaEd36CdDAb233360B939775ae5f1'

        total_stake = await c.get_total_stake_amount()
        print(f"Total Stake: {total_stake}")
        assert total_stake > 0