"""
Tests covering the IntervalReporter class from
telliot's reporter subpackage.
"""
import os

import pytest
from telliot.apps.telliot_config import TelliotConfig
from telliot.examples.btc_usd_feed import data_feeds
from telliot.reporter.interval import IntervalReporter
from web3.datastructures import AttributeDict

# Tellor playground contract used for test
playground_address = "0x4699845F22CA2705449CFD532060e04abE3F1F31"


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


def test_reporter_config(cfg):
    """Test instantiating an IntervalReporter using default telliot configs."""

    rinkeby_endpoint = cfg.get_endpoint()

    _ = IntervalReporter(
        endpoint=rinkeby_endpoint,
        private_key=cfg.main.private_key,
        contract_address=playground_address,
        datafeeds=data_feeds,
    )

    assert rinkeby_endpoint.network == "rinkeby"
    assert rinkeby_endpoint.provider
    assert rinkeby_endpoint.url

    assert rinkeby_endpoint.chain_id == 4


@pytest.mark.skip(reason="fails sometimes due to wrong gasprice & connection failures")
@pytest.mark.asyncio
async def test_interval_reporter_submit_once(cfg):
    """Test reporting once to the TellorX playground on Rinkeby
    with three retries."""

    rinkeby_endpoint = cfg.get_endpoint()

    reporter = IntervalReporter(
        endpoint=rinkeby_endpoint,
        private_key=cfg.main.private_key,
        contract_address=playground_address,
        datafeeds=data_feeds,
    )

    for _ in range(3):
        tx_receipts = await reporter.report_once(name="BTC USD Median Price Feed")
        if tx_receipts:
            break

    assert tx_receipts

    for receipt in tx_receipts:
        assert isinstance(receipt, AttributeDict)
        assert receipt.status == 1
        assert receipt.to == "0x4699845F22CA2705449CFD532060e04abE3F1F31"


# TODO: choose datafeeds in reporter config
