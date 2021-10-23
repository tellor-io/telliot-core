""" Telliot application helpers

"""
import logging
import threading
from pathlib import Path
from typing import Any
from typing import Optional

from pydantic import Field
from pydantic import PrivateAttr
from telliot.apps.telliot_config import TelliotConfig
from telliot.model.base import Base
from telliot.utils.home import telliot_homedir

logger = logging.getLogger(__name__)


class Application(Base):
    """Application base class"""

    #: Application Name
    name: str

    #: Home directory
    homedir: Path = Field(default_factory=telliot_homedir)

    #: Application configuration object
    config: Optional[TelliotConfig]

    #: Private thread storage
    _thread: Optional[threading.Thread] = PrivateAttr()
    _shutdown: threading.Event = PrivateAttr(default_factory=threading.Event)

    def __init__(self, **kwargs: Any) -> None:

        super().__init__(**kwargs)

        # Init configuration
        self.config = TelliotConfig(config_dir=self.homedir)

        # Logging
        self.configure_logging()

        logger.info("Created new {} application object".format(self.name))
        logger.info("Home Directory: {}".format(self.homedir))

    def configure_logging(self) -> None:
        """Configure Application logging

        Subclasses may override this method as required
        """

        # type checking does not seem to recognize that config
        # and homedir were validated/coerced in __init__
        assert self.config is not None
        assert isinstance(self.homedir, Path)

        # Convert loglevel text to log type
        loglevel = eval("logging." + self.config.main.loglevel.upper())

        logfile = self.homedir / (self.name + ".log")
        logging.basicConfig(filename=str(logfile), level=loglevel)

    def startup(self) -> None:
        """Startup Application

        Start the main application thread
        """
        logger.info("Starting {} Application".format(self.name))
        self._thread = threading.Thread(target=self.main, name=self.name)
        self._thread.start()

    def shutdown(self) -> None:
        """Startup Application

        Send a shutdown event to the main application thread and wait
        for it to terminate.
        """
        if self._thread:
            logger.info("Terminating {} Application".format(self.name))

            self._shutdown.set()

            #: Join worker thread
            self._thread.join()

            self._thread = None

    def main(self) -> None:
        """Main worker thread

        This method defined the main application processing.
        The main thread must monitor and respond to the self._shutdown event.

        This method *must* be overridded by subclasses.
        """
        seconds = 0
        while not self._shutdown.wait(1.0):
            print("Main thread processing: {}".format(seconds))
            seconds += 1

        print("Application {} received shutdown event".format(self.name))
        self._shutdown.clear()
