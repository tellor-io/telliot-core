import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorflex.diva import DivaOracleTellorContract
from telliot_core.tellor.tellorflex.diva import DivaProtocolContract


@pytest.mark.asyncio
async def test_diva_protocol_contract(ropsten_cfg):
    async with TelliotCore(config=ropsten_cfg) as core:
        account = core.get_account()
        diva = DivaProtocolContract(core.endpoint, account)
        diva.connect()

        assert diva.address == "0x6455A2Ae3c828c4B505b9217b51161f6976bE7cf"

        params = await diva.get_pool_parameters(pool_id=159)
        print(params)
        assert isinstance(params, tuple)
        assert params[0] == "BTC/USD"


# @pytest.mark.skip("Tx will revert")
@pytest.mark.asyncio
async def test_diva_tellor_oracle_contract(ropsten_cfg):
    async with TelliotCore(config=ropsten_cfg) as core:
        account = core.get_account()
        oracle = DivaOracleTellorContract(core.endpoint, account)
        oracle.connect()

        assert oracle.address == "0xED6D661645a11C45F4B82274db677867a7D32675"

        t = await oracle.get_min_period_undisputed()
        print(t)
        assert isinstance(t, int)
        assert t == 3600  # seconds

        # TODO:
        # status = await oracle.set_final_reference_value(pool_id=159,legacy_gas_price=100)
        # assert isinstance(status, ResponseStatus)
        # assert status.ok
