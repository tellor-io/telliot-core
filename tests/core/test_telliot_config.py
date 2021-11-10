import os
from pathlib import Path

from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.model.endpoints import RPCEndpoint


def prep_dir(clean=False):
    """Prepare temporary test directory"""
    tmpdir = Path("./temp").resolve().absolute()
    tmpdir.mkdir(parents=True, exist_ok=True)

    main_file = tmpdir / "main.yaml"
    ep_file = tmpdir / "endpoints.yaml"
    chain_file = tmpdir / "chains.json"

    if clean:
        if main_file.exists():
            os.remove(main_file)
        if ep_file.exists():
            os.remove(ep_file)
        if chain_file.exists():
            os.remove(chain_file)

    return tmpdir


def test_telliot_config():
    """Test main telliot_core configuration"""
    tmpdir = prep_dir()

    cfg = TelliotConfig(config_dir=tmpdir)

    ep = cfg.get_endpoint()
    assert isinstance(ep, RPCEndpoint)

    tmpdir = prep_dir(clean=True)
