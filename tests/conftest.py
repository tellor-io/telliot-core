"""Pytest Fixtures used for testing Pytelliot"""
import os

import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.directory.tellorx import tellor_directory


@pytest.fixture(scope="session", autouse=True)
def rinkeby_cfg():
    """Get rinkeby endpoint from config

    If environment variables are defined, they will override the values in config files
    """
    cfg = TelliotConfig()

    # Override configuration for rinkeby testnet
    cfg.main.chain_id = 4

    rinkeby_endpoint = cfg.get_endpoint()
    # assert rinkeby_endpoint.network == "rinkeby"

    # Optionally override private key and URL with ENV vars for testing
    if os.getenv("PRIVATE_KEY", None):
        cfg.main.private_key = os.environ["PRIVATE_KEY"]

    if os.getenv("NODE_URL", None):
        rinkeby_endpoint.url = os.environ["NODE_URL"]

    return cfg


@pytest.fixture()
def rinkeby_core(rinkeby_cfg):

    app = TelliotCore(config=rinkeby_cfg)

    # Replace staker private key
    staker = app.get_default_staker()
    if os.getenv("PRIVATE_KEY", None):
        staker.private_key = rinkeby_cfg.main.private_key
        staker.address = "0x8D8D2006A485FA4a75dFD8Da8f63dA31401B8fA2"

    app.connect()
    yield app
    app.destroy()


@pytest.fixture(scope="session")
def master(rinkeby_cfg):
    """Helper function for connecting to a contract at an address"""
    tellor_master = tellor_directory.find(chain_id=4, name="master")[0]
    endpoint = rinkeby_cfg.get_endpoint()
    endpoint.connect()
    master = Contract(
        address=tellor_master.address,  # "0x657b95c228A5de81cdc3F85be7954072c08A6042",
        abi=tellor_master.abi,
        node=endpoint,
        private_key=rinkeby_cfg.main.private_key,
    )
    master.connect()
    return master


@pytest.fixture(scope="session", autouse=True)
def oracle(rinkeby_cfg):
    """Helper function for connecting to a contract at an address"""
    tellor_oracle = tellor_directory.find(chain_id=4, name="oracle")[0]
    endpoint = rinkeby_cfg.get_endpoint()
    endpoint.connect()
    oracle = Contract(
        address=tellor_oracle.address,  # "0x07b521108788C6fD79F471D603A2594576D47477",
        abi=tellor_oracle.abi,
        node=endpoint,
        private_key=rinkeby_cfg.main.private_key,
    )
    oracle.connect()
    return oracle
