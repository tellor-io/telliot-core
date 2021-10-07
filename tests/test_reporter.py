"""
Tests covering the IntervalReporter class from
telliot's reporter subpackage.
"""
import os
from pathlib import Path

import yaml
from telliot.datafeed.example import data_feeds
from telliot.reporter.config import ReporterConfig
from telliot.reporter.interval import IntervalReporter
from web3.datastructures import AttributeDict

import pytest


@pytest.fixture
def tmpdir():
    """Create temp dir for config file."""
    return Path("./temp").resolve().absolute()

@pytest.fixture
def config_file(tmpdir):
    """Create config file for use in tests."""
    reporter_config_data = {
        "private_key": os.getenv("PRIVATE_KEY"),
        "node_url": os.getenv("NODE_URL"),
        "contract_address": "0x4699845F22CA2705449CFD532060e04abE3F1F31",
        "provider": "pokt",
        "network": "rinkeby",
        "chain_id": 4,
        "gasprice_speed": "fast",
        "loglevel": "info",
    }

    # create reporter config file
    config_file = tmpdir / "reporter.yaml"
    config_file.parent.mkdir(parents=True, exist_ok=True)

    with open(config_file, "w") as outfile:
        yaml.dump(reporter_config_data, outfile, default_flow_style=False)

    return config_file
    

def test_interval_reporter_instantiation_from_file(tmpdir, config_file):
    """Test instantiating an IntervalReporter from config file."""
    reporter = IntervalReporter(
        config=ReporterConfig.from_file(config_file),
        datafeeds=data_feeds,
    )

    assert reporter.config.provider == "pokt"
    assert reporter.config.chain_id == 4
    assert reporter.config.node_url

    os.remove(config_file)
    os.rmdir(tmpdir)


@pytest.mark.asyncio
async def test_interval_reporter_submit_once(tmpdir, config_file):
    """Test reporting once to the TellorX playground on Rinkeby."""
    reporter = IntervalReporter(
        config=ReporterConfig.from_file(config_file),
        datafeeds=data_feeds,
    )
    tx_receipts = await reporter.report_once()
    
    assert tx_receipts
    for receipt in tx_receipts:
        assert isinstance(receipt, AttributeDict)
        assert receipt.status == 1
        assert receipt.to == "0x4699845F22CA2705449CFD532060e04abE3F1F31"

    os.remove(config_file)
    os.rmdir(tmpdir)
