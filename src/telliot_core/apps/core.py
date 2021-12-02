# type: ignore
import logging
from pathlib import Path
from typing import Optional

from atom.api import Atom
from atom.api import Str
from atom.api import Typed

import telliot_core
from telliot_core.apps.app import get_contract
from telliot_core.apps.staker import Staker
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.home import telliot_homedir

logger = logging.getLogger(__name__)
networks = {1: "eth-mainnet", 4: "eth-rinkeby"}


class ContractSet(Atom):
    master = Typed(Contract)
    oracle = Typed(Contract)
    governance = Typed(Contract)
    treasury = Typed(Contract)


class TelliotCore(Atom):
    """Telliot core application"""

    #: BaseApplication Name
    name = Str("telliot-core")

    #: Home directory
    homedir = Typed(Path, factory=telliot_homedir)

    #: BaseApplication configuration object
    config = Typed(TelliotConfig)

    #: Endpoint storage
    endpoint = Typed(RPCEndpoint)

    #: Contract storage
    tellorx = Typed(ContractSet)

    # Private instance storage
    _instance = None

    def __init__(self, *args, **kwargs):

        super(TelliotCore, self).__init__(*args, **kwargs)

        if not self.config:
            self.config = TelliotConfig(config_dir=self.homedir)

        # Logging
        self.configure_logging()

        logger.info(f"Initialized {self.name}")
        logger.info(f"Home Folder: {self.homedir}")

        self.endpoint = self.config.get_endpoint()

    def __new__(cls, *args, **kwargs):
        """Create a new App"""
        if TelliotCore._instance is not None:
            raise RuntimeError("An application already exists")
        self = super(TelliotCore, cls).__new__(cls, *args, **kwargs)
        TelliotCore._instance = self
        return self

    @staticmethod
    def get() -> "TelliotCore":
        """Get the global app instance"""
        return TelliotCore._instance

    @staticmethod
    def destroy() -> None:
        """Destroy the instance.

        This method must be called prior to creating another instance of this class.
        """
        TelliotCore._instance = None

    def get_default_staker(self) -> Optional[Staker]:
        stakers = self.config.stakers.get(chain_id=self.config.main.chain_id)
        if len(stakers) > 0:
            return stakers[0]
        else:
            return None

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

        default_staker = self.get_default_staker()

        if connected:
            msg = (
                f"{self.name} application connected to {networks[chain_id]} "
                f"with staker {default_staker.tag} "
                f"(using telliot-core {telliot_core.__version__})"
            )
            print(msg)
            logger.info(msg)

        return connected

    def configure_logging(self) -> None:
        """Configure logging"""

        # type checking does not seem to recognize that config
        # and homedir were validated/coerced in __init__
        assert self.config is not None
        assert isinstance(self.homedir, Path)

        # Convert loglevel text to log type
        loglevel = eval("logging." + self.config.main.loglevel.upper())

        logfile = self.homedir / (self.name + ".log")
        logging.basicConfig(filename=str(logfile), level=loglevel)
