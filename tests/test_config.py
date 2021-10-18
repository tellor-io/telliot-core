"""
Unit tests covering telliot config options.
"""
import os
from pathlib import Path

import pytest
from telliot.utils.config import ConfigOptions

tmpdir = Path("./temp").resolve().absolute()


def test_config_constructor():
    """Test Constructor"""
    cfg = ConfigOptions()
    assert cfg.config_version == "0.0.1"

    assert cfg.config_file is None
    with pytest.raises(AttributeError):
        cfg.save()


def test_config_save():
    """Test Constructor"""
    config_file = tmpdir / "myconfig.yaml"
    cfg = ConfigOptions(config_file=config_file)
    print(cfg.config_file)
    print(cfg.config_file.parent)
    cfg.save()

    os.remove(config_file)
    os.rmdir(tmpdir)


def test_config_load():
    """Test configuration loading"""

    # Create a config file
    config_file = tmpdir / "myconfig.yaml"
    config_file.parent.mkdir(parents=True, exist_ok=True)

    lines = ["config_version: 9.9.9"]
    with open(config_file, "w") as f:
        f.write("\n".join(lines))

    # Test from_file class method
    cfg1 = ConfigOptions.from_file(config_file)
    assert cfg1.config_version == "9.9.9"
    assert cfg1.config_file == config_file

    os.remove(config_file)
    os.rmdir(tmpdir)


def test_subclass_example():
    class MyConfigOptions(ConfigOptions):
        network: str
        id: int

    config_file = tmpdir / "subclass.yaml"

    cfg = MyConfigOptions(network="rinkeby", id=4, config_file=config_file)
    cfg.save()

    # Create a new config from file
    cfg2 = cfg.from_file(config_file)
    assert cfg2.config_version == cfg.config_version
    assert cfg2.id == 4
    assert cfg2.network == "rinkeby"

    os.remove(config_file)
    os.rmdir(tmpdir)
