"""
Tests covering the IntervalReporter class from
telliot's reporter subpackage.
"""
import os
from pathlib import Path

import yaml
from telliot.datafeed.example import data_feeds
from telliot.reporter.config import ReporterConfig
from telliot.reporter.single import IntervalReporter


tmpdir = Path("./temp").resolve().absolute()


def test_interval_reporter_instantiation_from_file():
    """Test instantiating an IntervalReporter from config file."""
    # create reporter config file
    reporter_config_data = {
        "private_key": os.environ["PRIVATE_KEY"],
        "node_url": os.environ["NODE_URL"],
        "contract_address": "0x4699845F22CA2705449CFD532060e04abE3F1F31",
        "provider": "pokt",
        "network": "rinkeby",
        "chain_id": 4,
        "gasprice_speed": "fast",
        "loglevel": "info",
    }

    config_file = tmpdir / "reporter.yaml"

    with open(config_file, "w") as outfile:
        yaml.dump(reporter_config_data, outfile, default_flow_style=False)

    # create instance
    reporter = IntervalReporter(
        config=ReporterConfig.from_file("reporter.yaml"),
        datafeeds=data_feeds,
    )

    assert reporter.config.provider == "pokt"
    assert reporter.config.chain_id == 4
    assert reporter.config.node_url

    os.remove(config_file)
    os.rmdir(tmpdir)


def test_interval_reporter_submit_once():
    """Test reporting once to the TellorX playground on Rinkeby."""
    pass
