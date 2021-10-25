"""
Test covering Pytelliot EVM contract connection utils.
"""
import os

import pytest
from telliot.apps.telliot_config import TelliotConfig
from telliot.contract.contract import Contract
from telliot.reporter.profitcalc import profitable
from telliot.utils.abi import tellor_playground_abi


@pytest.fixture
def cfg():
    """Get rinkeby endpoint from config

    If environment variables are defined, they will override the values in config files
    """
    cfg = TelliotConfig()

    # Override configuration for rinkeby testnet
    cfg.main.chain_id = 4

    rinkeby_endpoint = cfg.get_endpoint()
    assert rinkeby_endpoint.network == "rinkeby"

    # Optionally override private key and URL with ENV vars for testing
    if os.getenv("PRIVATE_KEY", None):
        cfg.main.private_key = os.environ["PRIVATE_KEY"]

    if os.getenv("NODE_URL", None):
        rinkeby_endpoint.url = os.environ["NODE_URL"]

    return cfg


@pytest.fixture
def contract(cfg):
    """TellorX playground contract setup"""
    endpoint = cfg.get_endpoint()
    endpoint.connect()

    address = "0xb539Cf1054ba02933f6d345937A612332C842827"
    # url = "https://rinkeby.infura.io/v3/1a09c4705f114af2997548dd901d655b"

    c = Contract(
        address=address,
        abi=tellor_playground_abi,
        node=endpoint,
        private_key=cfg.main.private_key,
    )

    c.connect()

    return c


@pytest.fixture
def rewards(contract):
    request_id = "0x0000000000000000000000000000000000000000000000000000000000000002"

    time_based_reward, _ = contract.read(func_name="timeBasedReward")
    current_tip, _ = contract.read(func_name="getCurrentReward", _id=request_id)

    return time_based_reward, current_tip[0]


def test_is_not_profitable(rewards):
    time_based_reward, current_tip = rewards

    assert time_based_reward == 5e17
    assert current_tip == 0
    assert not profitable(
        tb_reward=time_based_reward, tip=current_tip, gas=1, gas_price=1e1000
    )


def test_is_profitable(rewards):
    time_based_reward, _ = rewards

    assert time_based_reward == 5e17
    assert profitable(tb_reward=time_based_reward, tip=1, gas=1, gas_price=1)
