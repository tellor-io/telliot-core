""" Test application utilities

"""
import os
import pathlib
import shutil
import threading
import time
from pathlib import Path

import pytest
from telliot.utils.app import AppConfig
from telliot.utils.app import Application
from telliot.utils.app import default_homedir


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

    with pytest.raises(FileExistsError):
        app = Application(name="appname", homedir=testhome, config_class=AppConfig)

    testhome.mkdir(parents=True)
    app = Application(name="appname", homedir=testhome, config_class=AppConfig)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)


def test_application_default_home():
    """Test default appliaction directory"""

    app = Application(name="appname", config_class=AppConfig)
    assert app.homedir == default_homedir()
    assert "telliot" in str(app.homedir)


def test_application_subclassing():
    """Test application features"""

    # Create an application-specific configuration
    # Note that ALL OPTIONS MUST HAVE DEFAULTS DEFINED
    # so that a default config can be constructed with no arguments.
    class MyAppConfig(AppConfig):
        app_specific_option: int = 0

    # Create Application subclass
    # Note: other attributes-specific can be added as required
    class MyApp(Application):

        # Insert other attributes here

        def __init__(self, **data):
            super().__init__(name="myapp", config_class=MyAppConfig, **data)

    # Make sure temp dir exists
    testhome.mkdir(parents=True, exist_ok=True)

    #: Instantiate application subclass
    app = MyApp(homedir=testhome)
    assert app.homedir == testhome
    assert app.config.app_specific_option == 0

    os.remove(app.config.config_file)
    os.remove(app.telliot_config.config_file)
    os.rmdir(testhome)


def test_application_processing():
    """Test application startup and shutdown"""
    testhome.mkdir(parents=True, exist_ok=True)

    app = Application(name="myapp", config_class=AppConfig, homedir=testhome)
    assert isinstance(app._shutdown, threading.Event)

    app = Application(name="myapp", config_class=AppConfig, homedir=testhome)
    app.startup()
    time.sleep(2)
    app.shutdown()

    os.remove(app.config.config_file)
    os.remove(app.telliot_config.config_file)
    os.rmdir(testhome)
