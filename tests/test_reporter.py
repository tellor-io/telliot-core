"""
Tests covering the IntervalReporter class from
telliot's reporter subpackage.
"""
import os

import pytest
from telliot.datafeed.example import data_feeds
from telliot.reporter.interval import IntervalReporter
from telliot.utils.app import AppConfig
from telliot.utils.app import Application
from web3.datastructures import AttributeDict


@pytest.fixture
def app():
    class NewAppConfig(AppConfig):
        private_key: str = ""
        contract_address: str = (
            "0x4699845F22CA2705449CFD532060e04abE3F1F31"  # tellorX playground
        )
        chain_id: int = 4  # rinkeby

    class TestApp(Application):
        def __init__(self, **data):
            super().__init__(name="reporter", config_class=NewAppConfig, **data)

    test_app = TestApp()

    if not test_app.config.private_key:
        test_app.config.private_key = os.environ["PRIVATE_KEY"]

    if not test_app.telliot_config.default_endpoint.url:
        test_app.telliot_config.default_endpoint.url = os.environ["NODE_URL"]

    return test_app


def test_reporter_config(app):
    """Test instantiating an IntervalReporter using default telliot configs."""
    reporter = IntervalReporter(
        config=app.config,
        telliot_config=app.telliot_config,
        datafeeds=data_feeds,
    )

    assert reporter.telliot_config.default_endpoint.network == "rinkeby"
    assert reporter.telliot_config.default_endpoint.provider == "pokt"
    assert reporter.telliot_config.default_endpoint.url

    assert reporter.config.chain_id == 4
    assert reporter.config.private_key
    assert (
        reporter.config.contract_address == "0x4699845F22CA2705449CFD532060e04abE3F1F31"
    )


@pytest.mark.asyncio
async def test_interval_reporter_submit_once(app):
    """Test reporting once to the TellorX playground on Rinkeby
    with three retries."""
    reporter = IntervalReporter(
        config=app.config,
        telliot_config=app.telliot_config,
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
