"""
Test covering Pytelliot EVM contract connection utils.
"""
import pytest
import web3

from telliot.model.endpoints import RPCEndpoint
from telliot.submitter.profitcalc import profitable
from telliot.utils.abi import tellor_playground_abi
from telliot.utils.contract import Contract


@pytest.fixture
def contract():
    """TellorX playground contract setup"""
    address = "0xb539Cf1054ba02933f6d345937A612332C842827"
    url = "https://rinkeby.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network='rinkeby', provider='infura', url=url)
    endpt.connect()

    c = Contract(node=endpt, address=address, abi=tellor_playground_abi)
    c.connect()

    return c


def test_is_profitable(contract):
    time_based_reward = contract.read(func_name='timeBasedReward')[0][0]
    request_id = "0x0000000000000000000000000000000000000000000000000000000000000002"
    current_tip = contract.read(func_name='getCurrentReward', _id=request_id)[0][0][0]

    assert time_based_reward == 5e17
    assert current_tip == 0

    assert not profitable(
        tb_reward=time_based_reward,
        tip=current_tip,
        gas=1,
        gas_price=1e20
    )

