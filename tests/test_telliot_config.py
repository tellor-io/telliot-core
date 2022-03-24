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
    api_keys_file = tmpdir / "api_keys.yaml"
    chain_file = tmpdir / "chains.json"
    directory_file = tmpdir / "directory.json"

    if clean:
        if main_file.exists():
            os.remove(main_file)
        if ep_file.exists():
            os.remove(ep_file)
        if api_keys_file.exists():
            os.remove(api_keys_file)
        if chain_file.exists():
            os.remove(chain_file)
        if directory_file.exists():
            os.remove(directory_file)

    return tmpdir


def test_telliot_config():
    """Test main telliot_core configuration"""
    tmpdir = prep_dir()

    cfg = TelliotConfig(config_dir=tmpdir)

    ep = cfg.get_endpoint()
    assert isinstance(ep, RPCEndpoint)

    api_key = cfg.api_keys.find("anyblock")[0]
    assert api_key.url == "https://api.anyblock.tools/"

    tmpdir = prep_dir(clean=True)
