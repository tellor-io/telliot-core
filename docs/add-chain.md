# Support new chain

1. Add chain ID & explorer URL to `telliot_core.directory.ContractInfo.get_abi()`
2. Add chain ID & name to `telliot_core.apps.core.NETWORKS`
3. Add chain info to `telliot_core.model.chain.default_chains_list`
4. Add chain ID & gas/fee info retrieval to `telliot_core.gas.legacy_gas.gas_station`
5. Add endpoint info to `telliot_core.model.endpoints.default_endpoint_list`
6. Add deployed oracle contract and autopay info to `telliot_core.data.contract_directory.json`:
    - add address for tellor360-autopay
    - add address for tellor360-oracle
    - add playground address for trb-token if testnet
7. Follow steps to support a new chain in [telliot-feeds](https://tellor-io.github.io/telliot-feeds/add-chain/)
