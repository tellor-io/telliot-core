import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.queries.price.spot_price import SpotPrice
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp


@pytest.mark.asyncio
async def test_main(ropsten_cfg):
    async with TelliotCore(config=ropsten_cfg) as core:

        # Playground contract address used for all tellorflex contract addresses
        # since it contains all functions needed.
        flex = core.get_tellorflex_contracts()

        assert flex.oracle.address == "0xF281e2De3bB71dE348040b10B420615104359c10"
        assert flex.token.address == "0xF281e2De3bB71dE348040b10B420615104359c10"

        tlnv, status = await flex.oracle.get_time_of_last_new_value()
        assert isinstance(status, ResponseStatus)
        if status.ok:
            assert isinstance(tlnv, TimeStamp)
        else:
            assert tlnv is None
        print(tlnv)

        lock = await flex.oracle.get_reporting_lock()
        print(lock)

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
