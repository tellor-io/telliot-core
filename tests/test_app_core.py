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


def test_application_homedir():
    """Test home directory handling"""
    if testhome.exists():
        shutil.rmtree(testhome)

    testhome.mkdir(parents=True)
    app = TelliotCore(homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)
    TelliotCore.destroy()


def test_application_default_home():
    """Test default application directory"""

    app = TelliotCore()
    assert app.homedir == default_homedir()
    assert "telliot" in str(app.homedir)
    TelliotCore.destroy()


def test_app_connect(rinkeby_cfg):
    app = TelliotCore(config=rinkeby_cfg)
    assert app.connect()
    TelliotCore.destroy()


def test_app_constrctor():
    # Create a default application
    _ = TelliotCore()

    # Prevent creating two Applications
    with pytest.raises(RuntimeError):
        _ = TelliotCore()

    # Destroy existing app
    TelliotCore.destroy()

    # Create a new app using local home folder
    tmpdir = Path(".tmp")
    if not tmpdir.exists():
        tmpdir.mkdir()
    _ = TelliotCore(homedir=Path(".tmp"))
    TelliotCore.destroy()
