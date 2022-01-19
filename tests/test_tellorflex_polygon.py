import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.utils.timestamp import TimeStamp


@pytest.mark.asyncio
async def test_main(mumbai_cfg):
    async with TelliotCore(config=mumbai_cfg) as core:

        chain_id = core.config.main.chain_id

        flex = core.get_tellorflex_contracts()

        governance_address = await flex.oracle.get_governance_address()
        if chain_id == 137:
            assert governance_address == "0x2cFC5bCE14862D46fBA3bb46A36A8b2d7E4aC040"
        elif chain_id == 80001:
            assert governance_address == "0x0Fe623d889Ad1c599E5fF3076A57D1D4F2448CDe"

        stake_amount = await flex.oracle.get_stake_amount()
        assert stake_amount == 10.0
        print(stake_amount)

        tlnv = await flex.oracle.get_time_of_last_new_value()
        assert isinstance(tlnv, TimeStamp)
        print(tlnv)

        lock = await flex.oracle.get_reporting_lock()
        print(lock)

        token_address = await flex.oracle.get_token_address()
        if chain_id == 137:
            assert token_address == "0xE3322702BEdaaEd36CdDAb233360B939775ae5f1"
        elif chain_id == 80001:
            assert token_address == "0x002E861910D7f87BAa832A22Ac436F25FB66FA24"

        total_stake = await flex.oracle.get_total_stake_amount()
        print(f"Total Stake: {total_stake}")
