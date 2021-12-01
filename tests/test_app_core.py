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
    app = TelliotCore(name="appname", homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)
    app.destroy()


def test_application_default_home():
    """Test default application directory"""

    app = TelliotCore(name="appname")
    assert app.homedir == default_homedir()
    assert "telliot" in str(app.homedir)
    app.destroy()


def test_application_subclassing():
    """Test application features"""

    # Create BaseApplication subclass
    # Note: other attributes-specific can be added as required
    class MyApp(TelliotCore):

        # Insert other attributes here

        def __init__(self, **data):
            super().__init__(name="myapp", **data)

    # Make sure temp dir exists
    testhome.mkdir(parents=True, exist_ok=True)

    #: Instantiate application subclass
    app = MyApp(homedir=testhome)
    assert app.homedir == testhome

    shutil.rmtree(testhome)
    app.destroy()


def test_app_connect(rinkeby_cfg):
    app = TelliotCore(name="testapp", config=rinkeby_cfg)
    assert app.connect()
    app.destroy()


def test_app_constrctor():
    # Create a default application
    app = TelliotCore()

    # Prevent creating two Applications
    with pytest.raises(RuntimeError):
        app = TelliotCore()

    # Destroy existing app
    app.destroy()

    # Create a new app using local home folder
    tmpdir = Path(".tmp")
    if not tmpdir.exists():
        tmpdir.mkdir()
    app = TelliotCore(homedir=Path(".tmp"))
    app.destroy()

    # Test app getter (create from scratch)
    app.destroy()
    app1 = TelliotCore().get()

    # Re-get existing app object
    app2 = TelliotCore.get()

    assert app1 is app2

    app1.destroy()
    app2.destroy()
