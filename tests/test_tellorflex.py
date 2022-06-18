import pytest
from brownie import accounts
from brownie import TellorFlex

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorflex.oracle import TellorFlexOracleContract
from telliot_core.utils.response import ResponseStatus
from telliot_core.utils.timestamp import TimeStamp

# from telliot_core.queries.price.spot_price import SpotPrice


@pytest.fixture(scope="module")
def mock_flex_contract():
    """Mock the TellorFlex contract"""
    return accounts[0].deploy(
        TellorFlex,
        "0x0000000000000000000000000000000000000123",
        "0x0000000000000000000000000000000000000456",
        42e18,
        60 * 60,
    )


@pytest.mark.asyncio
async def test_main(mumbai_test_cfg, mock_flex_contract):
    """Test the TellorFlex contract"""
    async with TelliotCore(config=mumbai_test_cfg) as core:
        account = core.get_account()
        # Override contract addresses with locally deployed mock contract addresses
        oracle = TellorFlexOracleContract(core.endpoint, account)
        oracle.address = mock_flex_contract.address
        oracle.connect()

        governance_address = await oracle.get_governance_address()
        assert governance_address == "0x0000000000000000000000000000000000000456"

        stake_amount = await oracle.get_stake_amount()
        assert stake_amount == 42

        tlnv, status = await oracle.get_time_of_last_new_value()
        assert isinstance(status, ResponseStatus)
        if status.ok:
            assert isinstance(tlnv, TimeStamp)
        else:
            assert tlnv is None

        lock = await oracle.get_reporting_lock()
        assert lock == 60 * 60

        token_address = await oracle.get_token_address()
        assert token_address == "0x0000000000000000000000000000000000000123"

        total_stake = await oracle.get_total_stake_amount()
        assert total_stake == 0

        staker_info, status = await oracle.get_staker_info(core.get_account().address)
        assert isinstance(status, ResponseStatus)
        if status.ok:
            for info in staker_info:
                assert isinstance(info, int)
        else:
            assert staker_info is None

        # q = SpotPrice(asset="btc", currency="USD")
        qid = b"0000000000000000000000000000000000000000000000000000000000000064"
        count, status = await oracle.get_new_value_count_by_qeury_id(qid)

        assert isinstance(status, ResponseStatus)
        if status.ok:
            assert isinstance(count, int)
        else:
            assert count is None
