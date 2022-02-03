import logging
from typing import Any
from typing import Optional

from chained_accounts import ChainedAccount

from telliot_core.contract.contract import Contract
from telliot_core.directory import contract_directory
from telliot_core.model.endpoints import RPCEndpoint
from telliot_core.utils.response import ResponseStatus


logger = logging.getLogger(__name__)


class DivaProtocolContract(Contract):
    """Main Diva Protocol contract."""

    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None and chain_id in (137, 80001, 3)  # Polygon chains & Ropsten

        contract_info = contract_directory.find(chain_id=chain_id, name="diva-protocol")[0]
        if not contract_info:
            raise Exception(f"Diva Protocol contract not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_pool_parameters(self, pool_id: int) -> Optional[tuple[Any]]:
        """Fetches info about a specific pool.

        Used for getting the referenceAsset mostly ('BTC/USD', for example)."""

        pool_params, status = await self.read("getPoolParameters", _poolId=pool_id)

        if status.ok:
            return pool_params  # type: ignore
        else:
            logger.error("Error getting pool params from DivaProtocolContract")
            logger.error(status)
            return None

    async def get_latest_pool_id(self) -> None:
        raise NotImplementedError


class DivaOracleTellorContract(Contract):
    """Diva contract used for settling derivatives pools."""

    def __init__(self, node: RPCEndpoint, account: Optional[ChainedAccount] = None):
        chain_id = node.chain_id
        assert chain_id is not None and chain_id in (137, 80001, 3)  # Polygon chains & Ropsten

        contract_info = contract_directory.find(chain_id=chain_id, name="diva-oracle-tellor")[0]
        if not contract_info:
            raise Exception(f"diva-oracle-tellor contract info not found on chain_id {chain_id}")

        contract_abi = contract_info.get_abi(chain_id=chain_id)

        super().__init__(
            address=contract_info.address[chain_id],
            abi=contract_abi,
            node=node,
            account=account,
        )

    async def get_min_period_undisputed(self) -> Optional[int]:
        """How long the latest value reported must remain uncontested
        before the pool can be settled."""

        seconds, status = await self.read("getMinPeriodUndisputed")

        if status.ok:
            assert isinstance(seconds, int)
            return seconds
        else:
            logger.error("Error getting min period undisputed from DivaOracleTellorContract")
            logger.error(status)
            return None

    async def set_final_reference_value(
        self,
        pool_id: int,
        legacy_gas_price: Optional[int] = None,
        max_priority_fee_per_gas: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
        gas_limit: int = 320000,
    ) -> Optional[ResponseStatus]:
        """ "Settle a pool.

        Must be called after the the minimum period undisputed has elapsed."""

        assert self.node.chain_id is not None
        diva_protocol_info = contract_directory.find(chain_id=self.node.chain_id, name="diva-protocol")[0]
        diva_protocol_addr = diva_protocol_info.address[self.node.chain_id]

        print(diva_protocol_addr)

        _, status = await self.write(
            "setFinalReferenceValue",
            _divaDiamond=diva_protocol_addr,
            _poolId=pool_id,
            gas_limit=gas_limit,
            legacy_gas_price=legacy_gas_price,
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            max_fee_per_gas=max_fee_per_gas,
        )

        if status.ok:
            return status
        else:
            logger.error("Error setting final reference value on DivaOracleTellorContract")
            logger.error(status)
            return None
