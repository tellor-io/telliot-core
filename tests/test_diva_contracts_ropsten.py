import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorflex.diva import DivaOracleTellorContract
from telliot_core.tellor.tellorflex.diva import DivaProtocolContract
from telliot_core.tellor.tellorflex.diva import PoolParameters


@pytest.mark.asyncio
async def test_diva_protocol_contract(ropsten_cfg):
    async with TelliotCore(config=ropsten_cfg) as core:
        account = core.get_account()
        diva = DivaProtocolContract(core.endpoint, account)
        diva.connect()

        assert diva.address == "0x07F0293a07703c583F4Fb4ce3aC64043732eF3bf"

        p = await diva.get_pool_parameters(pool_id=3)
        print(p)
        assert isinstance(p, PoolParameters)
        assert isinstance(p.reference_asset, str)
        assert isinstance(p.expiry_time, int)
        assert isinstance(p.floor, int)
        assert isinstance(p.inflection, int)
        assert isinstance(p.cap, int)
        assert isinstance(p.supply_initial, int)
        assert isinstance(p.collateral_token, str)
        assert isinstance(p.collateral_balance_short_initial, int)
        assert isinstance(p.collateral_balance_long_initial, int)
        assert isinstance(p.collateral_balance, int)
        assert isinstance(p.short_token, str)
        assert isinstance(p.long_token, str)
        assert isinstance(p.final_reference_value, int)
        assert isinstance(p.status_final_reference_value, int)
        assert isinstance(p.redemption_amount_long_token, int)
        assert isinstance(p.redemption_amount_short_token, int)
        assert isinstance(p.status_timestamp, int)
        assert isinstance(p.data_provider, str)
        assert isinstance(p.redemption_fee, int)
        assert isinstance(p.settlement_fee, int)
        assert isinstance(p.capacity, int)

        assert p.reference_asset == "ETH/USD"
        assert p.expiry_time == 1657349074
        assert p.floor == 2000000000000000000000
        assert p.inflection == 2000000000000000000000
        assert p.cap == 4500000000000000000000
        assert p.supply_initial == 100000000000000000000
        assert p.collateral_token == "0x867e53feDe91d27101E062BF7002143EbaEA3e30"
        assert p.collateral_balance_short_initial == 50000000000000000000
        assert p.collateral_balance_long_initial == 50000000000000000000
        assert p.collateral_balance >= 214199598796389167516
        assert p.short_token == "0x91E75Aebda86a6B02d5510438f2981AC4Af1A44d"
        assert p.long_token == "0x945b1fA4DB6Fb1f8d3C7501968F6549C8c147D4e"
        assert p.final_reference_value == 0
        assert p.status_final_reference_value == 0
        assert p.redemption_amount_long_token == 0
        assert p.redemption_amount_short_token == 0
        assert p.status_timestamp == 1647349398
        assert p.data_provider == "0xED6D661645a11C45F4B82274db677867a7D32675"
        assert p.redemption_fee == 2500000000000000
        assert p.settlement_fee == 500000000000000
        assert p.capacity == 0


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
