import os

from telliot.utils.config import ConfigOptions
from telliot.utils.config import LogLevel


def test_config_constructor():
    """Test Constructor"""
    cfg = ConfigOptions()
    # state = cfg.__getstate__()
    assert cfg.loglevel.name == "INFO"


def test_store_and_load_file():
    # Create a configuration and store it to a file
    cfg = ConfigOptions(loglevel=LogLevel.CRITICAL)
    _ = cfg.to_file("tempfile.yaml")

    # Class constructor from file
    cfg2 = ConfigOptions.from_file("tempfile.yaml")
    assert cfg.loglevel == cfg2.loglevel

    os.remove("tempfile.yaml")
