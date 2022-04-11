# Getting Started


## Telliot Configuration

After installation of the `telliot-core` or any telliot data feeds,
Telliot must be personalized to use your own private keys and endpoints.

First, create the default configuration files:

    telliot config init

The default configuration files are created in a folder called `telliot` in the user home folder.

To show the current configuration:

    telliot config show

### Main Configuration File

The main configuration file allows you to choose the default network Telliot will interact with.
By default, Telliot is configured to run on Rinkeby testnet, as shown in the example below.
Edit the `~/telliot/main.yaml` config file for the desired configuration.

- To run on Ethereum mainnet, use `chain_id: 1` and `network: mainnet`.

- To submit values to the Tellor oracle, a `private_key` must also be configured.

*Example main configuration file:*

```yaml
type: MainConfig
loglevel: INFO
chain_id: 4

```

### Configure Accounts

Telliot needs to know which accounts are available for contract writes, such as submitting values to the oracle.
Use the command line to add necessary accounts/private keys.

For example, to add an account called `my-matic-acct` for reporting on polygon mainnet (EVM chain_id=137):

    >> chained add my-matic-acct 0x57fe7105302229455bcfd58a8b531b532d7a2bb3b50e1026afa455cd332bf706 137
    Enter encryption password for my-matic-acct: 
    Confirm password: 
    Added new account my-matic-acct (address= 0xcd19cf65af3a3aea1f44a7cb0257fc7455f245f0) for use on chains (137,)

Note that reporting accounts can be used for ETH mainnet (chain_id=1), Rinkeby testnet (chain_id=4), or Polygon testnet
(chain_id=80001).  Also note that a single account/private key can be associated with multiple chains.

Detailed instructions for managing EVM accounts can be found in the
[`chained_accounts` package documentation](https://github.com/pydefi/chained-accounts). 


### Configure endpoints

Edit `~/telliot/endpoints.yaml` to configure Telliot to use your own endpoints.

If you don't have an endpoint, a free one is available at [Infura.io](http://www.infura.io).  Simply replace `INFURA_API_KEY` with the one provided by Infura.

Endpoints should be configured for both Ethereum mainnet and Rinkeby testnet.  

!!! warning

    All telliot software and reporter feeds should be validated on Rinkeby prior to deploying on mainnet. 

Note that endpoints must use the websocket protocol because HTTPS endpoints do not support event listeners.

*Example `endpoints.yaml` file:*
```yaml
type: EndpointList
endpoints:
- type: RPCEndpoint
  chain_id: 1
  network: mainnet
  provider: Infura
  url: wss://mainnet.infura.io/ws/v3/{INFURA_API_KEY}
  explorer: https://etherscan.io
- type: RPCEndpoint
  chain_id: 4
  network: rinkeby
  provider: Infura
  url: wss://rinkeby.infura.io/ws/v3/{INFURA_API_KEY}
  explorer: https://rinkeby.etherscan.io

```

### Add API Keys

Some data sources used for reporting require you to set up an account and use an API key for authenticating requests. Edit `~/telliot/api_keys.yaml` to add any API keys needed for reporting data like AMPL/USD/VWAP and BCT/USD.

*Example `api_keys.yaml` file:*
```yaml
type: ApiKeyList
api_keys:
- type: ApiKey
  name: anyblock
  key: 'YOUR API KEY GOES HERE'
  url: https://api.anyblock.tools/
- type: ApiKey
  name: bravenewcoin
  key: 'YOUR API KEY GOES HERE'
  url: https://bravenewcoin.p.rapidapi.com/
...
```
