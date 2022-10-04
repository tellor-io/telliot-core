import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from traceback import format_tb
from typing import Optional
from typing import Union

import aiohttp
from chained_accounts import ChainedAccount
from chained_accounts import find_accounts

from telliot_core.apps.session_manager import ClientSessionManager
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.contract.listener import Listener
from telliot_core.directory import contract_directory
from telliot_core.logs import init_logging
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.tellor.tellor360.autopay import Tellor360AutopayContract
from telliot_core.tellor.tellor360.oracle import Tellor360OracleContract
from telliot_core.tellor.tellorflex.autopay import TellorFlexAutopayContract
from telliot_core.tellor.tellorflex.oracle import TellorFlexOracleContract
from telliot_core.tellor.tellorflex.token import TokenContract
from telliot_core.tellor.tellorx.master import TellorxMasterContract
from telliot_core.tellor.tellorx.oracle import TellorxOracleContract
from telliot_core.utils.home import telliot_homedir
from telliot_core.utils.versions import show_telliot_versions

NETWORKS = {
    1: "eth-mainnet",
    3: "eth-ropsten",
    4: "eth-rinkeby",
    5: "eth-goerli",
    137: "polygon-mainnet",
    80001: "polygon-mumbai",
    122: "fuse-mainnet",
    69: "optimism-kovan",
    1666600000: "harmony-mainnet",
    1666700000: "harmony-testnet",
    421611: "arbitrum-rinkeby",
    941: "pulsechain-testnet",
    42161: "arbitrum",
    1337: "brownie-local-network",
}

LOGLEVEL_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
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
    autopay: TellorFlexAutopayContract
    token: TokenContract


@dataclass
class Tellor360ContractSet:
    """Tellor360 contract set"""

    oracle: Tellor360OracleContract
    autopay: Tellor360AutopayContract
    token: TokenContract


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
            account = self.get_account()

            oracle = TellorFlexOracleContract(node=self.endpoint, account=account)
            oracle.connect()

            token = TokenContract(node=self.endpoint, account=account)
            token.connect()

            autopay = TellorFlexAutopayContract(node=self.endpoint, account=account)
            autopay.connect()

            self._tellorflex = TellorFlexContractSet(oracle=oracle, token=token, autopay=autopay)

        return self._tellorflex

    _tellorflex: Optional[TellorFlexContractSet]

    def get_tellorx_contracts(self) -> TellorxContractSet:
        """Get or create TellorX contracts"""

        if not self._tellorx:
            account = self.get_account()

            master = TellorxMasterContract(node=self.endpoint, account=account)
            master.connect()

            oracle = TellorxOracleContract(node=self.endpoint, account=account)
            oracle.connect()

            self._tellorx = TellorxContractSet(
                master=master,
                oracle=oracle,
                governance=self.get_contract(name="tellorx-governance"),
                treasury=self.get_contract(name="tellorx-treasury"),
            )

        return self._tellorx

    _tellorx: Optional[TellorxContractSet]

    def get_tellor360_contracts(self) -> Tellor360ContractSet:
        """Get or create Tellor360 contracts"""

        if not self._tellor360:
            account = self.get_account()

            oracle = Tellor360OracleContract(node=self.endpoint, account=account)
            oracle.connect()

            autopay = Tellor360AutopayContract(node=self.endpoint, account=account)
            autopay.connect()

            token = TokenContract(node=self.endpoint, account=account)
            token.connect()

            self._tellor360 = Tellor360ContractSet(oracle=oracle, autopay=autopay, token=token)

        return self._tellor360

    _tellor360: Optional[Tellor360ContractSet]

    #: User-specified account name
    account_name = property(lambda self: self._account_name)
    _account_name: Optional[str] = None

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

    @property
    def log(self) -> logging.Logger:
        """Provide access to the main telliot logger"""
        return self._log

    def __init__(
        self,
        *,
        homedir: Optional[Union[str, Path]] = None,
        config: Optional[TelliotConfig] = None,
        chain_id: Optional[int] = None,
        account_name: Optional[str] = None,
    ):

        self._homedir = telliot_homedir(homedir)
        self._config = config or TelliotConfig(config_dir=self.homedir)
        self._endpoint = None
        self._listener = None
        self._tellorx = None
        self._tellorflex = None
        self._tellor360 = None

        loglevel = LOGLEVEL_MAP[self._config.main.loglevel]
        self._log = init_logging(loglevel)

        if chain_id is not None:
            # Override chain ID
            self._config.main.chain_id = chain_id

        if account_name is not None:
            self.set_account_name(account_name)

        self._session_manager = ClientSessionManager()

        show_telliot_versions(self.log.info)

    def set_account_name(self, account_name: str) -> None:
        _ = self.get_account(name=account_name)  # Make sure it exists
        self._account_name = account_name

    async def startup(self) -> None:
        """Connect to the tellorX network"""
        assert self.config

        chain_id = self.config.main.chain_id

        account = self.get_account()
        if account is None:
            raise RuntimeError("Cannot start tellor-core application.  No account found.")

        await self._session_manager.open()

        msg = f"Connected to {NETWORKS[chain_id]} [default account: {account.name}], time: {datetime.now()}"
        self.log.info(msg)

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
        account: Optional[ChainedAccount] = None,
    ) -> Contract:

        assert self.config is not None

        if not chain_id:
            chain_id = self.config.main.chain_id
            assert chain_id is not None

        if not account:
            account = self.get_account()

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
            account=account,
        )
        contract.connect()
        return contract

    def get_account(
        self,
        *,
        name: Optional[str] = None,
        address: Optional[str] = None,
        chain_id: Optional[int] = None,
    ) -> ChainedAccount:
        """Retrieve the user specified account

        If None configured, the default first matching account will be used
        """

        if name:
            acc_name = name
        else:
            acc_name = self.account_name

        if not chain_id:
            chain_id = self.config.main.chain_id

        accounts = find_accounts(
            name=acc_name,
            address=address,
            chain_id=chain_id,
        )

        if len(accounts) > 0:
            return accounts[0]
        else:
            raise Exception("No accounts found")

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

    async def __aenter__(self) -> "TelliotCore":
        await self.startup()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        if exc_type:
            self.log.error("Exception occurred in telliot-core app")
            self.log.error(exc_type)
            self.log.error(exc_val)
            self.log.error(format_tb(exc_tb))
        await self.shutdown()
