""" Test application utilities

"""
import logging
import threading
import time

from telliot_core.apps.app import ThreadedApplication

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def test_threaded_application():
    """Test application startup and shutdown"""

    app = ThreadedApplication()
    assert isinstance(app._shutdown, threading.Event)

    app = ThreadedApplication()
    app.startup()
    time.sleep(2)
    app.shutdown()
