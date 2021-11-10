""" Test application utilities

"""
import pathlib
import shutil
import threading
import time
from pathlib import Path

from telliot_core.apps.app import Application
from telliot_core.utils.home import default_homedir

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
    app = Application(name="appname", homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)


def test_application_default_home():
    """Test default application directory"""

    app = Application(name="appname")
    assert app.homedir == default_homedir()
    assert "telliot" in str(app.homedir)


def test_application_subclassing():
    """Test application features"""

    # Create Application subclass
    # Note: other attributes-specific can be added as required
    class MyApp(Application):

        # Insert other attributes here

        def __init__(self, **data):
            super().__init__(name="myapp", **data)

    # Make sure temp dir exists
    testhome.mkdir(parents=True, exist_ok=True)

    #: Instantiate application subclass
    app = MyApp(homedir=testhome)
    assert app.homedir == testhome

    shutil.rmtree(testhome)


def test_application_processing():
    """Test application startup and shutdown"""
    testhome.mkdir(parents=True, exist_ok=True)

    app = Application(name="myapp", homedir=testhome)
    assert isinstance(app._shutdown, threading.Event)

    app = Application(name="myapp", homedir=testhome)
    app.startup()
    time.sleep(2)
    app.shutdown()

    shutil.rmtree(testhome)
