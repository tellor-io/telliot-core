import pytest
from brownie import accounts
from brownie import AutopayMock

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellor360.autopay import Tellor360AutopayContract


@pytest.fixture(scope="module")
def mock_autopay_contract():
    return accounts[0].deploy(AutopayMock)


@pytest.mark.asyncio
async def test_get_current_tip(amoy_test_cfg, mock_autopay_contract):
    async with TelliotCore(config=amoy_test_cfg) as core:
        account = core.get_account()

        autopay = Tellor360AutopayContract(core.endpoint, account)
        autopay.address = mock_autopay_contract.address
        autopay.connect()

        query_id = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000002")

        result, status = await autopay.get_current_tip(query_id=query_id)
        assert status.ok
        assert result == len(query_id)
