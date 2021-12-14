"""Pytest Fixtures used for testing Pytelliot"""
import os

import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.apps.telliot_config import TelliotConfig


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

    # Destroy app instance after test
    TelliotCore.destroy()


