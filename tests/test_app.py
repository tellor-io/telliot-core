""" Test application utilities

"""
import logging
import pathlib
import shutil
import threading
import time
from pathlib import Path

from telliot_core.apps.app import BaseApplication
from telliot_core.apps.app import ThreadedApplication
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
    app = BaseApplication(name="appname", homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)


def test_application_default_home():
    """Test default application directory"""

    app = BaseApplication(name="appname")
    assert app.homedir == default_homedir()
    assert "telliot" in str(app.homedir)


def test_application_subclassing():
    """Test application features"""

    # Create BaseApplication subclass
    # Note: other attributes-specific can be added as required
    class MyApp(BaseApplication):

        # Insert other attributes here

        def __init__(self, **data):
            super().__init__(name="myapp", **data)

    # Make sure temp dir exists
    testhome.mkdir(parents=True, exist_ok=True)

    #: Instantiate application subclass
    app = MyApp(homedir=testhome)
    assert app.homedir == testhome

    shutil.rmtree(testhome)


def test_app_connect(rinkeby_cfg):
    app = BaseApplication(name="testapp", config=rinkeby_cfg)
    assert app.connect()


def test_threaded_application():
    """Test application startup and shutdown"""
    testhome.mkdir(parents=True, exist_ok=True)

    app = ThreadedApplication(name="myapp", homedir=testhome)
    assert isinstance(app._shutdown, threading.Event)

    app = ThreadedApplication(name="myapp", homedir=testhome)
    app.startup()
    time.sleep(2)
    app.shutdown()

    shutil.rmtree(testhome)
