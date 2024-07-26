import logging
import pathlib
import shutil
from pathlib import Path

import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.utils.home import default_homedir

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Temp file location
testhome = Path("./temp").resolve().absolute()


def test_homedir():
    """Test default home directory"""
    hd = default_homedir()
    assert isinstance(hd, pathlib.Path)
    assert hd.exists()


@pytest.mark.asyncio
async def test_application_homedir(amoy_test_cfg):
    """Test home directory handling"""
    if testhome.exists():
        shutil.rmtree(testhome)

    testhome.mkdir(parents=True)
    app = TelliotCore(config=amoy_test_cfg, homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)


@pytest.mark.asyncio
async def test_application_default_home(amoy_test_cfg):
    """Test default application directory"""

    async with TelliotCore(config=amoy_test_cfg) as app:
        assert app.homedir == default_homedir()
        assert "telliot" in str(app.homedir)


@pytest.mark.asyncio
async def test_app_constructor(amoy_test_cfg):
    tmpdir = Path(".tmp")
    if not tmpdir.exists():
        tmpdir.mkdir()

    # Create a default application
    async with TelliotCore(config=amoy_test_cfg, homedir=Path(".tmp")) as app:
        assert app.homedir.absolute() == tmpdir.absolute()
