from lib2to3.pgen2 import token
import logging
from dataclasses import dataclass
from pathlib import Path
from traceback import format_tb
from typing import Optional
from typing import Union

import aiohttp

from telliot_core.apps.session_manager import ClientSessionManager
from telliot_core.apps.staker import Staker
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.contract.listener import Listener
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.tellor.tellorflex.oracle import TellorFlexOracleContract
from telliot_core.tellor.tellorflex.token import TellorFlexTokenContract
from telliot_core.tellor.tellorx.master import TellorxMasterContract
from telliot_core.tellor.tellorx.oracle import TellorxOracleContract
from telliot_core.utils.home import telliot_homedir
from telliot_core.utils.versions import show_telliot_versions

logger = logging.getLogger(__name__)
networks = {
    1: "eth-mainnet",
    4: "eth-rinkeby",
    137: "polygon-mainnet",
    80001: "polygon-mumbai",
}


@dataclass
class TellorxContractSet:
    master: TellorxMasterContract
    oracle: TellorxOracleContract
    governance: Contract
    treasury: Contract


@dataclass
class TellorFlexContractSet:
    oracle: TellorFlexOracleContract
    token: TellorFlexTokenContract


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

    def get_tellorflex_contracts(self) -> TellorFlexContractSet:
        """Get or create tellorflex contracts."""
        if not self._tellorflex:
            staker = self.get_staker()
            private_key = staker.private_key

            oracle = TellorFlexOracleContract(node=self.endpoint, private_key=private_key)
            oracle.connect()

            token = TellorFlexTokenContract(node=self.endpoint, private_key=private_key)
            token.connect()

            self._tellorflex = TellorFlexContractSet(
                oracle=oracle,
                token=token,
                )

        return self._tellorflex

    _tellorflex: Optional[TellorFlexContractSet]

    def get_tellorx_contracts(self) -> TellorxContractSet:
        """Get or create TellorX contracts"""

        if not self._tellorx:
            staker = self.get_staker()
            private_key = staker.private_key

            master = TellorxMasterContract(node=self.endpoint, private_key=private_key)
            master.connect()

            oracle = TellorxOracleContract(node=self.endpoint, private_key=private_key)
            oracle.connect()

            self._tellorx = TellorxContractSet(
                master=master,
                oracle=oracle,
                governance=self.get_contract(name="tellorx-governance"),
                treasury=self.get_contract(name="tellorx-treasury"),
            )

        return self._tellorx

    _tellorx: Optional[TellorxContractSet]

    #: User-specified staker
    staker_tag = property(lambda self: self._staker_tag)
    _staker_tag: Optional[str] = None

    @property
    def shared_session(self) -> aiohttp.ClientSession:
        """Return the shared session"""
        return self._session_manager.session

    _session_manager: ClientSessionManager

    @property
    def listener(self) -> Listener:
        """Get or create listener object"""
        if not self._listener:
            self._listener = Listener(session=self.shared_session, ws_url=self.endpoint.url)

        return self._listener

    _listener: Optional[Listener]

    @property
    def endpoint(self) -> RPCEndpoint:
        """Get or create the endpoint for the current configuration"""
        if not self._endpoint:
            self._endpoint = self.get_endpoint()
            connected = self._endpoint.connect()
            if not connected:
                raise Exception(f"Could not connect to endpoint: {self._endpoint.url}")

        return self._endpoint

    _endpoint: Optional[RPCEndpoint]

    def __init__(
        self,
        *,
        homedir: Optional[Union[str, Path]] = None,
        config: Optional[TelliotConfig] = None,
        chain_id: Optional[int] = None,
        staker_tag: Optional[str] = None,
    ):

        self._homedir = telliot_homedir(homedir)
        self._config = config or TelliotConfig(config_dir=self.homedir)
        self._endpoint = None
        self._listener = None
        self._tellorx = None
        self._tellorflex = None

        if chain_id is not None:
            # Override chain ID
            self._config.main.chain_id = chain_id

        if staker_tag is not None:
            self.set_staker_tag(staker_tag)

        self._session_manager = ClientSessionManager()

        show_telliot_versions()

    def set_staker_tag(self, staker_tag: str) -> None:
        _ = self.get_staker(tag=staker_tag)  # Make sure it exists
        self._staker_tag = staker_tag

    async def startup(self) -> None:
        """Connect to the tellorX network"""
        assert self.config

        chain_id = self.config.main.chain_id

        staker = self.get_staker()
        if staker is None:
            raise RuntimeError("Cannot start tellor-core application.  No staker found.")

        await self._session_manager.open()

        msg = f"Using: {networks[chain_id]} [staker: {staker.tag}]"
        print(msg)

    def get_endpoint(
        self,
        *,
        chain_id: Optional[int] = None,
        provider: Optional[str] = None,
    ) -> RPCEndpoint:

        if not chain_id:
            chain_id = self.config.main.chain_id

        endpoints = self.config.endpoints.find(chain_id=chain_id, provider=provider)
        if len(endpoints) == 0:
            raise Exception("No endpoints found")

        return endpoints[0]  # type: ignore

    def get_contract(
        self,
        *,
        org: Optional[str] = None,
        name: Optional[str] = None,
        address: Optional[str] = None,
        chain_id: Optional[int] = None,
        private_key: Optional[str] = None,
    ) -> Contract:

        assert self.config is not None

        if not chain_id:
            chain_id = self.config.main.chain_id
            assert chain_id is not None

        if not private_key:
            staker = self.get_staker()
            private_key = staker.private_key

        entries = contract_directory.find(org=org, name=name, address=address, chain_id=chain_id)
        if len(entries) > 1:
            raise Exception("More than one contract found.")
        elif len(entries) == 0:
            raise Exception("No contracts found")

        contract_info = entries[0]

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        if self.endpoint.chain_id is not chain_id:
            raise Exception(f"Endpoint chain {self.endpoint.chain_id} does not match requested chain {chain_id}")

        contract = Contract(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=self.endpoint,
            private_key=private_key,
        )
        contract.connect()
        return contract

    def get_staker(
        self,
        *,
        tag: Optional[str] = None,
        address: Optional[str] = None,
        private_key: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> Staker:
        """Retrieve the user specified staker

        If None configured, the default first matching staker will be used

        """

        if tag:
            staker_tag = tag
        else:
            staker_tag = self.staker_tag

        if not chain_id:
            chain_id = self.config.main.chain_id

        stakers = self.config.stakers.find(
            tag=staker_tag,
            address=address,
            private_key=private_key,
            chain_id=chain_id,
        )

        if len(stakers) > 0:
            return stakers[0]  # type: ignore
        else:
            raise Exception("No stakers found")

    async def shutdown(self) -> None:
        """Cleanly shutdown core"""

        # Release/close endpoint
        if self._endpoint:
            self._endpoint = None

        # SHut down listeners
        if self._listener:
            await self._listener.shutdown()

        # Close aiohttp session
        await self._session_manager.close()

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
            logger.error(format_tb(exc_tb))
        await self.shutdown()
