import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import Union

from telliot_core.apps.singleton import Singleton
from telliot_core.apps.staker import Staker
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.contract.contract import Contract
from telliot_core.directory.tellorx import tellor_directory
from telliot_core.model.endpoints import RPCEndpoint
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


class TelliotCore(metaclass=Singleton):
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

    def __init__(
        self,
        *,
        homedir: Optional[Union[str, Path]] = None,
        config: Optional[TelliotConfig] = None,
        endpoint: Optional[RPCEndpoint] = None,
    ):

        self._homedir = telliot_homedir(homedir)

        self._config = config or TelliotConfig(config_dir=self.homedir)

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

        show_telliot_versions()

    def get_default_staker(self) -> Optional[Staker]:
        stakers = self.config.stakers.find(chain_id=self.config.main.chain_id)
        if len(stakers) > 0:
            default_staker = stakers[0]
            assert isinstance(default_staker, Staker)
            return default_staker
        else:
            return None

    def connect(self) -> bool:
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

        self._tellorx = ContractSet(
            master=get_contract("master", chain_id, self.endpoint, private_key),
            oracle=get_contract("oracle", chain_id, self.endpoint, private_key),
            governance=get_contract("governance", chain_id, self.endpoint, private_key),
            treasury=get_contract("treasury", chain_id, self.endpoint, private_key),
        )

        default_staker = self.get_default_staker()
        if not default_staker:
            raise Exception("No staker found")

        if connected:
            msg = f"connected: {networks[chain_id]} [staker: {default_staker.tag}]"
            print(msg)
            logger.info(msg)

        return bool(connected)

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
