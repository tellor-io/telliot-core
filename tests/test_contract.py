"""
Test covering Pytelliot EVM contract connection utils.
"""
import pytest
import web3

from telliot_core.apps.core import TelliotCore


@pytest.mark.asyncio
async def test_connect_to_tellor(rinkeby_test_cfg):
    """Contract object should access Tellor functions"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        tellorx = core.get_tellorx_contracts()
        assert len(tellorx.master.contract.all_functions()) > 0
        assert isinstance(
            tellorx.master.contract.all_functions()[0],
            web3.contract.ContractFunction,
        )


@pytest.mark.asyncio
async def test_mixed_gas_inputs(rinkeby_test_cfg):
    """Contract.write() should refuse a combination of
    legacy gas args and EIP-1559 gas args"""

    with pytest.raises(ValueError):

        async with TelliotCore(config=rinkeby_test_cfg) as core:
            tellorx = core.get_tellorx_contracts()

            tx_receipt, status = await tellorx.oracle.write(
                func_name="transfer",
                _to="0xF90cd1D6C1da49CE2cF5C39f82999D7145aa66aD",
                _amount=1,
                extra_gas_price=0,
                gas_limit=350000,
                legacy_gas_price=1,
                max_fee_per_gas=2,
            )
