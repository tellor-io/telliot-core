"""Pytest Fixtures used for testing Pytelliot"""
import os

import pytest
from brownie import chain
from chained_accounts import ChainedAccount
from chained_accounts import find_accounts

from telliot_core.apps.telliot_config import TelliotConfig


@pytest.fixture(scope="session", autouse=True)
def sepolia_cfg():
    """Get sepolia endpoint from config

    If environment variables are defined, they will override the values in config files
    """
    cfg = TelliotConfig()

    # Override configuration for sepolia testnet
    cfg.main.chain_id = 11155111

    sepolia_endpoint = cfg.get_endpoint()
    # assert sepolia_endpoint.network == "sepolia"

    if os.getenv("NODE_URL", None):
        sepolia_endpoint.url = os.environ["NODE_URL"]

    sepolia_accounts = find_accounts(chain_id=11155111)
    if not sepolia_accounts:
        # Create a test account using PRIVATE_KEY defined on github.
        key = os.getenv("PRIVATE_KEY", None)
        if key:
            ChainedAccount.add("git-sepolia-key", chains=11155111, key=os.environ["PRIVATE_KEY"], password="")
        else:
            raise Exception("Need a sepolia account")

    return cfg


@pytest.fixture(scope="session", autouse=True)
def amoy_cfg():
    """Return a test telliot configuration for use on polygon-amoy

    If environment variables are defined, they will override the values in config files
    """
    cfg = TelliotConfig()

    # Override configuration for amoy testnet
    cfg.main.chain_id = 80002

    endpt = cfg.get_endpoint()
    if "INFURA_API_KEY" in endpt.url:
        endpt.url = f'https://polygon-amoy.infura.io/v3/{os.environ["INFURA_API_KEY"]}'

    amoy_accounts = find_accounts(chain_id=80002)
    if not amoy_accounts:
        # Create a test account using PRIVATE_KEY defined on github.
        key = os.getenv("PRIVATE_KEY", None)
        if key:
            ChainedAccount.add(
                "git-amoy-key",
                chains=80002,
                key=os.environ["PRIVATE_KEY"],
                password="",
            )
        else:
            raise Exception("Need a amoy account")

    return cfg


def local_node_cfg(chain_id: int):
    """Return a test telliot configuration for use of tellorFlex contracts. Overrides
    the default Web3 provider with a local Ganache endpoint.
    """

    cfg = TelliotConfig()

    # Use a chain_id with TellorFlex contracts deployed
    cfg.main.chain_id = chain_id

    endpt = cfg.get_endpoint()

    # Configure testing using local Ganache node
    endpt.url = "http://127.0.0.1:8545"

    # Advance block number to avoid assertion error in endpoint.connect():
    # connected = self._web3.eth.get_block_number() > 1
    chain.mine(10)

    accounts = find_accounts(chain_id=chain_id)
    if not accounts:
        # Create a test account using PRIVATE_KEY defined on github.
        key = os.getenv("PRIVATE_KEY", None)
        if key:
            ChainedAccount.add(
                "git-tellorflex-test-key",
                chains=chain_id,
                key=os.environ["PRIVATE_KEY"],
                password="",
            )
        else:
            raise Exception(f"Need an account for {chain_id}")

    return cfg


@pytest.fixture
def amoy_test_cfg(scope="session", autouse=True):
    return local_node_cfg(chain_id=80002)


@pytest.fixture
def sepolia_test_cfg(scope="session", autouse=True):
    return local_node_cfg(chain_id=11155111)
