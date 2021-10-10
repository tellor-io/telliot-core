""" Telliot application helpers

"""
import enum
import logging
import pathlib
import threading
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Type
from typing import Union

from pydantic import BaseModel
from pydantic import Field
from pydantic import PrivateAttr
from telliot.utils.config import ConfigOptions
from telliot.utils.rpc_endpoint import RPCEndpoint

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


class LogLevel(str, enum.Enum):
    """Enumeration of supported log levels"""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


DefaultRPCEndpoint = RPCEndpoint(
    network="Network Name (e.g. 'mainnet', 'testnet', 'rinkebey')",
    provider="Provider Name (e.g. 'Infura')",
    url="URL (e.g. 'https://mainnet.infura.io/v3/<project_id>')",
)


class TelliotConfig(ConfigOptions):
    """Shared telliot configuration object

    This class maintains configuration entries shared by all
    telliot `Applications`.  It should be updated as needed.
    """

    default_endpoint: RPCEndpoint = Field(default=DefaultRPCEndpoint)


class AppConfig(ConfigOptions):
    """Base class for Application Configuration

    Default values must be provided for all options so that
    constructor can be called with zero arguments
    """

    #: Control application logging level
    loglevel: LogLevel = LogLevel.INFO


class Application(BaseModel):
    """Application base class"""

    #: Application Name
    name: str

    #: Home directory
    homedir: Path

    #: Application configuration object
    config: AppConfig

    #: Default constructor for configuration
    config_class: Type[AppConfig]

    # Shared Telliot Configuration
    telliot_config: TelliotConfig

    #: Private thread storage
    _thread: Optional[threading.Thread] = PrivateAttr()
    _shutdown: threading.Event = PrivateAttr(default_factory=threading.Event)

    def __init__(
        self,
        config: Optional[AppConfig] = None,
        homedir: Optional[Path] = None,
        **kwargs: Any
    ) -> None:

        # Home Directory
        homedir = self._set_homedir(homedir)

        # Shared Telliot Configuration
        # Try to load configuration from file
        telliot_config_file = Path(homedir) / "telliot.yaml"
        if telliot_config_file.exists():
            telliot_config = TelliotConfig.from_file(telliot_config_file)
        else:
            # Create a default configuration and save it
            telliot_config = TelliotConfig(config_file=telliot_config_file)
            telliot_config.save()

        # App-Specific Configuration
        if "name" not in kwargs:
            raise AttributeError("name is required")
        else:
            name = kwargs["name"]

        if "config_class" not in kwargs:
            raise AttributeError("config_class is required")
        else:
            config_class = kwargs["config_class"]

        if config is None:
            # Try to load configuration from file
            config_file = Path(homedir) / (name + ".yaml")
            if config_file.exists():
                config = config_class.from_file(config_file)
            else:
                # Create a default configuration and save it
                config = config_class(config_file=config_file)
                config.save()

        # Initialize object with required homedir and configuration
        super().__init__(
            config=config, telliot_config=telliot_config, homedir=homedir, **kwargs
        )

        # Logging
        self.configure_logging()

        logger.info("Created new {} application object".format(self.name))
        logger.info("Home Directory: {}".format(self.homedir))
        logger.info("Config file: {}".format(self.config.config_file))

    def configure_logging(self) -> None:
        """Configure Application logging

        Subclasses may override this method as required
        """

        # type checking does not seem to recognize that config
        # and homedir were validated/coerced in __init__
        assert self.config is not None
        assert isinstance(self.homedir, Path)

        # Convert loglevel text to log type
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

    @staticmethod
    def _set_homedir(homedir: Optional[Union[str, Path]] = None) -> Path:
        """Set homedir

        Sets home directory, using a default if none is provided.
        The default directory is created if it does not exist.
        A homedir that is provided must exist
        """
        if homedir is None:
            # Set default homedir and create if necessary
            result = default_homedir()
            if not result.exists():
                result.mkdir(parents=True)
        else:
            # Use specified home directory
            if isinstance(homedir, str):
                homedir = Path(homedir)
            result = homedir.resolve().absolute()
            if not result.exists():
                raise FileExistsError("Directory does not exist: {}".format(homedir))

        return result
