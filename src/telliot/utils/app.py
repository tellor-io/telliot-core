""" Telliot application helpers

"""
import logging
import pathlib
import threading
from pathlib import Path
from typing import Any
from typing import Optional

from pydantic import BaseModel
from pydantic import PrivateAttr
from telliot.utils.config import ConfigOptions

logger = logging.getLogger(__name__)


def default_homedir() -> pathlib.Path:
    """Return default home directory, creating it if necessary

    Returns:
        pathlib.Path : Path to home directory
    """
    homedir = Path.home() / ("telliot")
    homedir = homedir.resolve().absolute()
    if not homedir.is_dir():
        homedir.mkdir()

    return homedir


class Application(BaseModel):
    """Application base class"""

    #: Application Name
    name: str

    #: Home directory
    homedir: Optional[Path]

    #: Configuration file
    #: If not provided, default is <name>.yaml in homedir
    config_file: Optional[Path]

    #: Application configuration object
    config: Optional[ConfigOptions]

    #: Private thread storage
    _thread: Optional[threading.Thread] = PrivateAttr()
    _shutdown: threading.Event = PrivateAttr(default_factory=threading.Event)

    def __init__(self, **kwargs: Any) -> None:

        # Pydantic initialization
        super().__init__(**kwargs)

        # Home Directory
        if self.homedir is None:
            # Set default homedir and create if necessary
            self.homedir = default_homedir()
            if not self.homedir.exists():
                self.homedir.mkdir(parents=True)
        else:
            # Use specified home directory
            self.homedir = self.homedir.resolve().absolute()
            if not self.homedir.exists():
                raise FileExistsError(
                    "Directory does not exist: {}".format(self.homedir)
                )

        # Configuration

        if self.config_file is None:
            # If no config file was passed in, use default file
            self.config_file = self.homedir / (self.name + ".yaml")
        elif isinstance(self.config_file, str):
            self.config_file = Path(self.config_file)

        if not self.config:
            # If a config was not passed in, try to load it from the file
            if self.config_file.exists():
                self.config = ConfigOptions.from_file(self.config_file)

            # Otherwise, create and store a default config
            else:
                self.config = self.get_default_config()
                self.config.to_file(self.config_file)

        # Logging
        self.configure_logging()

        logger.info("Created new {} application object".format(self.name))
        logger.info("Home Directory: {}".format(self.homedir))
        logger.info("Config file: {}".format(self.config_file))

    def get_default_config(self) -> ConfigOptions:
        """Return the default application configuration object

        Subclasses may override this method as required
        """
        return ConfigOptions()

    def configure_logging(self) -> None:
        """Configure Application logging

        Subclasses may override this method as required
        """

        # type checking does not seem to recognize that config
        # and homedir were validated/coerced in __init__
        assert self.config is not None
        assert isinstance(self.homedir, Path)

        # Convert loglevel string to log type
        loglevel = eval("logging." + self.config.loglevel.upper())

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
