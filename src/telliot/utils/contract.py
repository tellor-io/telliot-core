"""
Utils for connecting to an EVM contract
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import web3
from eth_typing.evm import ChecksumAddress
from telliot.utils.app import TelliotConfig
from telliot.utils.base import Base
from telliot.utils.rpc_endpoint import RPCEndpoint
from web3 import Web3


class Contract(Base):
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    # node: RPCEndpoint

    #: Contract address
    address: Union[str, ChecksumAddress]

    #: ABI specifications of contract
    abi: Union[List[Dict[str, Any]], str]

    #: web3 contract object
    contract: Optional[web3.contract.Contract]

    #: global pytelliot configurations
    config: TelliotConfig

    def connect(self) -> bool:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.config.default_endpoint.web3 is None:
            print("node is not instantiated")
            return False
        else:
            if not self.config.default_endpoint.connect():
                print("node is not connected")
                return False
            self.address = Web3.toChecksumAddress(self.address)
            self.contract = self.config.default_endpoint.web3.eth.contract(
                address=self.address, abi=self.abi
            )
            return True

    def read(self, func_name: str, **kwargs: Any) -> Tuple[Any, bool]:
        """
        Reads data from contract
        inputs:
        func_name (str): name of contract function to call

        returns:
        Tuple: contract function outpus
        Bool: success
        """

        if self.contract:
            try:
                contract_function = self.contract.get_function_by_name(func_name)
                return (contract_function(**kwargs).call(),), True
            except ValueError:
                print(f"function '{func_name}' not found in contract abi")
                return (), False
        else:
            if self.connect():
                print("now connected to contract")
                return self.read(func_name=func_name, **kwargs)
            else:
                print("unable to connect to contract")
                return (), False

    # def write(self, func_name: str, **kwargs: Any) -> bool:
    #     """
    #     Writes data to contract
    #     inputs:
    #     func_name (str): name of contract function to call

    #     returns:
    #     bool: success
    #     """
    #     try:
    #         # load account from private key
    #         self.acc = self.config.default_endpoint.web3.eth.account.from_key(self.config.private_key)
    #         # get account nonce
    #         acc_nonce = self.config.default_endpoint.web3.eth.get_transaction_count(self.acc.address)
    #         # get fast gas price
    #         req = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    #         prices = json.loads(req.content)
    #         gas_price = str(prices["fast"])
    #         print("retrieved gas price:", gas_price)
    #         # find function in contract
    #         contract_function = self.contract.get_function_by_name(func_name)
    #         tx = contract_function(**kwargs)
    #         # estimate gas
    #         estimated_gas = tx.estimateGas()
    #         # build transaction
    #         tx_built = tx.build_transaction(
    #             {
    #                 "nonce": acc_nonce,
    #                 "gas": estimated_gas,
    #                 "gasPrice": self.config.default_endpoint.web3.toWei(gas_price, "gwei"),
    #                 "chainId": self.config.chain_id,
    #             }
    #         )

    #         tx_signed = self.acc.sign_transaction(tx_built)

    #         tx_hash = self.config.default_endpoint.web3.eth.send_raw_transaction(tx_signed.rawTransaction)
    #         print(
    #             f"View reported data: https://rinkeby.etherscan.io/tx/{tx_hash.hex()}"
    #         )

    #         _ = self.config.default_endpoint.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=360)

    #         return True
    #     except Exception:
    #         print("tx was unsuccessful")
    #         return False

    def listen(self) -> None:
        """Wrapper for listening for contract events"""
        pass
