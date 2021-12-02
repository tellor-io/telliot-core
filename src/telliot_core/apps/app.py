""" Telliot application helpers

"""
import logging
import threading
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Optional

import telliot_core
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.directory.tellorx import tellor_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.home import telliot_homedir

logger = logging.getLogger(__name__)


def get_contract(name: str, chain_id: int, endpoint: RPCEndpoint, key: str) -> Contract:
    contract_info = tellor_directory.find(chain_id=chain_id, name=name)[0]
    if not contract_info:
        raise Exception(f"contract not found: {name}, {chain_id}")
    assert contract_info.abi

    contract = Contract(
        address=contract_info.address,
        abi=contract_info.abi,
        node=endpoint,
        private_key=key,
    )
    contract.connect()
    return contract


@dataclass
class ContractSet:
    master: Contract
    oracle: Contract
    governance: Contract
    treasury: Contract


networks = {1: "eth-mainnet", 4: "eth-rinkeby"}


@dataclass
class BaseApplication:
    """BaseApplication base class"""

    #: BaseApplication Name
    name: str

    #: Home directory
    homedir: Path = field(default_factory=telliot_homedir)

    #: BaseApplication configuration object
    config: Optional[TelliotConfig] = None

    #: Endpoint storage
    endpoint: Optional[RPCEndpoint] = None

    #: Contract storage
    tellorx: Optional[ContractSet] = None

    def __post_init__(self) -> None:
        if not self.config:
            self.config = TelliotConfig(config_dir=self.homedir)

        # Logging
        self.configure_logging()

        logger.info(f"Initialized {self.name}")
        logger.info(f"Home Folder: {self.homedir}")

        self.endpoint = self.config.get_endpoint()

    def connect(self) -> bool:
        """Connect to the tellorX network"""
        # re-get endpoint to make sure it matches chain_id
        assert self.config
        self.endpoint = self.config.get_endpoint()
        assert self.endpoint
        assert self.config

        connected = self.endpoint.connect()
        if not connected:
            raise Exception(f"Could not connect to endpoint: {self.endpoint.url}")

        chain_id = self.config.main.chain_id
        private_key = self.config.main.private_key

        self.tellorx = ContractSet(
            master=get_contract("master", chain_id, self.endpoint, private_key),
            oracle=get_contract("oracle", chain_id, self.endpoint, private_key),
            governance=get_contract("governance", chain_id, self.endpoint, private_key),
            treasury=get_contract("treasury", chain_id, self.endpoint, private_key),
        )

        if connected:
            msg = (
                f"{self.name} application connected to {networks[chain_id]} "
                f"(using telliot-core {telliot_core.__version__})"
            )
            print(msg)
            logger.info(msg)

        return connected

    def configure_logging(self) -> None:
        """Configure BaseApplication logging

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


@dataclass
class ThreadedApplication(BaseApplication):
    #: Private thread storage
    _thread: Optional[threading.Thread] = None
    _shutdown: threading.Event = field(default_factory=threading.Event)

    def startup(self) -> None:
        """Startup BaseApplication

        Start the main application thread
        """
        logger.info("Starting {} BaseApplication".format(self.name))
        self._thread = threading.Thread(target=self.main, name=self.name)
        self._thread.start()

    def shutdown(self) -> None:
        """Startup BaseApplication

        Send a shutdown event to the main application thread and wait
        for it to terminate.
        """
        if self._thread:
            logger.info("Terminating {} BaseApplication".format(self.name))

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
            logger.info("Main thread processing: {}".format(seconds))
            seconds += 1

        logger.info("BaseApplication {} received shutdown event".format(self.name))
        self._shutdown.clear()
