import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Union

from telliot_core.apps.session_manager import ClientSessionManager
from telliot_core.apps.staker import Staker
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.directory.tellorx import tellor_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.tellorx.master import TellorxMasterContract
from telliot_core.tellorx.oracle import TellorxOracleContract
from telliot_core.utils.home import telliot_homedir
from telliot_core.utils.versions import show_telliot_versions

logger = logging.getLogger(__name__)
networks = {1: "eth-mainnet", 4: "eth-rinkeby"}


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


class TelliotCore:
    """Telliot core application"""

    #: BaseApplication Name
    name: str = "telliot-core"

    #: Home directory
    homedir = property(lambda self: self._homedir)
    _homedir: Path

    #: BaseApplication configuration object
    config = property(lambda self: self._config)
    _config: TelliotConfig

    #: Endpoint storage
    endpoint = property(lambda self: self._endpoint)
    _endpoint: RPCEndpoint

    #: Contract storage
    tellorx = property(lambda self: self._tellorx)
    _tellorx: ContractSet

    #: User-specified staker
    staker_tag = property(lambda self: self._staker_tag)
    _staker_tag: Optional[str] = None

    #: Session manager
    _session_manager: ClientSessionManager

    @property
    def running(self) -> bool:
        """True if core application is running"""
        return self._running

    _running: bool

    def __init__(
        self,
        *,
        homedir: Optional[Union[str, Path]] = None,
        config: Optional[TelliotConfig] = None,
        endpoint: Optional[RPCEndpoint] = None,
        chain_id: Optional[int] = None,
        staker_tag: Optional[str] = None,
    ):

        self._homedir = telliot_homedir(homedir)

        self._config = config or TelliotConfig(config_dir=self.homedir)

        if chain_id is not None:
            # Override chain ID
            self._config.main.chain_id = chain_id

        if staker_tag is not None:
            self.set_staker_tag(staker_tag)

        if endpoint:
            self._endpoint = endpoint
        else:
            found_endpoint = self.config.get_endpoint()
            if found_endpoint:
                self._endpoint = found_endpoint
            else:
                raise Exception(
                    f"Endpoint not found for chain id: {self.config.main.chain_id}"
                )

        self._session_manager = ClientSessionManager()

        self._running = False

        show_telliot_versions()

    def set_staker_tag(self, staker_tag: str) -> None:
        _ = self.get_staker()  # Make sure it exists
        self._staker_tag = staker_tag

    def get_staker(self) -> Staker:
        """Retrieve the user specified staker

        If None configured, the default first matching staker will be used

        """
        if self.staker_tag:
            stakers = self.config.stakers.find(tag=self.staker_tag)
            if len(stakers) > 0:
                assert isinstance(stakers[0], Staker)
                return stakers[0]
            else:
                raise ValueError(f"Staker {self.staker_tag} not found.")
        else:
            return self.get_default_staker()

    def get_default_staker(self) -> Staker:
        stakers = self.config.stakers.find(chain_id=self.config.main.chain_id)
        if len(stakers) > 0:
            default_staker = stakers[0]
            assert isinstance(default_staker, Staker)
            return default_staker
        else:
            raise Exception(f"No staker found for chain id {self.config.main.chain_id}")

    async def startup(self) -> bool:
        """Connect to the tellorX network"""
        # re-get endpoint to make sure it matches chain_id
        assert self.config
        self._endpoint = self.config.get_endpoint()
        assert self.endpoint
        assert self.config

        connected = self.endpoint.connect()
        if not connected:
            raise Exception(f"Could not connect to endpoint: {self.endpoint.url}")

        chain_id = self.config.main.chain_id

        default_staker = self.get_default_staker()
        if default_staker is None:
            raise RuntimeError(
                "Cannot start tellor-core application.  No staker found."
            )

        private_key = default_staker.private_key

        master = TellorxMasterContract(node=self.endpoint, private_key=private_key)
        master.connect()

        oracle = TellorxOracleContract(node=self.endpoint, private_key=private_key)
        oracle.connect()

        self._tellorx = ContractSet(
            master=master,
            oracle=oracle,
            governance=get_contract("governance", chain_id, self.endpoint, private_key),
            treasury=get_contract("treasury", chain_id, self.endpoint, private_key),
        )

        staker = self.get_staker()
        if not staker:
            raise Exception("No staker found")

        if connected:
            msg = f"connected: {networks[chain_id]} [staker: {default_staker.tag}]"
            print(msg)
            # logger.info(msg)

        await self._session_manager.open()

        self._running = True

        return bool(connected)

    async def shutdown(self) -> None:
        """Cleanly shutdown core"""

        # Close aiohttp session
        await self._session_manager.close()

        self._running = False

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

    async def __aenter__(self) -> "TelliotCore":
        await self.startup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        if exc_type:
            logger.error("Exception occurred in telliot-core app")
            logger.error(exc_type)
            logger.error(exc_val)
            logger.error(exc_tb)
        await self.shutdown()
