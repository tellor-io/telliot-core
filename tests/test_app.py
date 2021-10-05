""" Test application utilities

"""
import os
import pathlib
import shutil
import threading
import time

import pytest
from telliot.utils.app import Application
from telliot.utils.app import default_homedir


def test_homedir():
    """Test default home directory"""
    hd = default_homedir()
    assert isinstance(hd, pathlib.Path)
    assert hd.exists()


def test_application():
    """Test application features"""

    testhome = "./tmpapp"
    if pathlib.Path(testhome).exists():
        shutil.rmtree(testhome)

    #: Create an application with the default home directory
    app = Application(name="appname")
    assert app.homedir == default_homedir()

    with pytest.raises(FileExistsError):
        app = Application(name="appname", homedir=testhome)

    os.mkdir(testhome)
    app = Application(name="appname", homedir=testhome)
    assert isinstance(app.homedir, pathlib.Path)

    shutil.rmtree(testhome)


def test_application_proc():
    """Test application startup and shutdown"""
    app = Application(name="testapp")
    assert isinstance(app._shutdown, threading.Event)
    a = Application(name="myapp")
    a.startup()
    time.sleep(2)
    a.shutdown()
