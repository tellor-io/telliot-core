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
async def test_application_homedir():
    """Test home directory handling"""
    if testhome.exists():
        shutil.rmtree(testhome)

    testhome.mkdir(parents=True)
    app = TelliotCore(homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)
    await app.destroy()


@pytest.mark.asyncio
async def test_application_default_home():
    """Test default application directory"""

    app = TelliotCore()
    assert app.homedir == default_homedir()
    assert "telliot" in str(app.homedir)
    await app.destroy()


@pytest.mark.asyncio
async def test_app_connect(rinkeby_cfg):
    app = TelliotCore(config=rinkeby_cfg)
    assert await app.startup()
    await app.destroy()


@pytest.mark.asyncio
async def test_app_constructor():
    # Create a default application
    app = TelliotCore()

    # Prevent creating two Applications
    with pytest.raises(RuntimeError):
        _ = TelliotCore()

    # Destroy existing app
    await app.destroy()

    # Create a new app using local home folder
    tmpdir = Path(".tmp")
    if not tmpdir.exists():
        tmpdir.mkdir()
    app2 = TelliotCore(homedir=Path(".tmp"))
    await app2.destroy()


@pytest.mark.asyncio
async def test_context_manager():

    async with TelliotCore() as core:
        await core.startup()
        print(core.name)
