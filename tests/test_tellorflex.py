import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.queries.price.spot_price import SpotPrice
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp


@pytest.mark.skip("Failing on github action runs")
@pytest.mark.asyncio
async def test_main(mumbai_cfg):
    async with TelliotCore(config=mumbai_cfg) as core:

        chain_id = core.config.main.chain_id

        flex = core.get_tellorflex_contracts()

        governance_address = await flex.oracle.get_governance_address()
        if chain_id == 137:
            assert governance_address == "0x2cFC5bCE14862D46fBA3bb46A36A8b2d7E4aC040"
        elif chain_id == 80001:
            # Old one, TODO confirm w/ Tim it switched
            # assert governance_address == "0x0Fe623d889Ad1c599E5fF3076A57D1D4F2448CDe"
            # New one
            assert governance_address == "0x8A868711e3cE97429faAA6be476F93907BCBc2bc"

        stake_amount = await flex.oracle.get_stake_amount()
        assert stake_amount == 10.0
        print(stake_amount)

        tlnv, status = await flex.oracle.get_time_of_last_new_value()
        assert isinstance(status, ResponseStatus)
        if status.ok:
            assert isinstance(tlnv, TimeStamp)
        else:
            assert tlnv is None
        print(tlnv)

        lock = await flex.oracle.get_reporting_lock()
        print(lock)

        token_address = await flex.oracle.get_token_address()
        if chain_id == 137:
            assert token_address == "0xE3322702BEdaaEd36CdDAb233360B939775ae5f1"
        elif chain_id == 80001:
            assert token_address == "0x45cAF1aae42BA5565EC92362896cc8e0d55a2126"

        total_stake = await flex.oracle.get_total_stake_amount()
        print(f"Total Stake: {total_stake}")

        staker_info, status = await flex.oracle.get_staker_info(core.get_account().address)
        assert isinstance(status, ResponseStatus)
        if status.ok:
            for info in staker_info:
                assert isinstance(info, int)
        else:
            assert staker_info is None

        q = SpotPrice(asset="btc", currency="USD")
        count, status = await flex.oracle.get_new_value_count_by_qeury_id(q.query_id)

        assert isinstance(status, ResponseStatus)
        if status.ok:
            assert isinstance(count, int)
        else:
            assert count is None


@pytest.mark.asyncio
async def test_tellorflex_fuse(fuse_cfg):
    async with TelliotCore(config=fuse_cfg) as core:
        chain_id = core.config.main.chain_id
        assert chain_id == 122

        flex = core.get_tellorflex_contracts()
        assert flex.token.address == "0x0BE9e53fd7EDaC9F859882AfdDa116645287C629"

        stake_amount = await flex.oracle.get_stake_amount()
        assert stake_amount == 100.0
