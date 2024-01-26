# Support new chain

1. Add chain ID & explorer URL to `telliot_core.directory.ContractInfo.get_abi()`.
2. Add chain ID & name to `telliot_core.apps.core.NETWORKS`.
3. Add chain info to `telliot_core.model.chain.default_chains_list`.
4. Add endpoint info to `telliot_core.model.endpoints.default_endpoint_list`.
5. Add deployed oracle contract and autopay info to `telliot_core.data.contract_directory.json`:
    - Add address for `tellor360-autopay`.
    - Add address for `tellor360-oracle`.
    - Add address for `trb-token`.
    - Add address for `tellor-governance`. 
6. Follow steps to support a new chain in [telliot-feeds](https://tellor-io.github.io/telliot-feeds/add-chain/).
