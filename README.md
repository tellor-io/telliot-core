![CI](https://github.com/tellor-io/pytelliot/actions/workflows/py38.yml/badge.svg)
![Docs](https://github.com/tellor-io/pytelliot/actions/workflows/docs.yml/badge.svg)
[![codecov](https://codecov.io/gh/tellor-io/pytelliot/branch/main/graph/badge.svg?token=S1199HQ2EK)](https://codecov.io/gh/tellor-io/pytelliot)
[![Discord Chat](https://img.shields.io/discord/461602746336935936)](https://discord.com/invite/n7drGjh)
[![Twitter Follow](https://img.shields.io/twitter/follow/wearetellor?style=social)](https://twitter.com/WeAreTellor)

# Telliot

Telliot is a Python framework for interacting with the decentralized TellorX network.

Please refer to the following for additional information:

- [DRAFT Telliot Documentation](https://tellor-io.github.io/pytelliot/)
- [TellorX Whitepaper](https://www.tellor.io/static/media/tellorX-whitepaper.f6527d55.pdf)

# Installation

This package should not be installed directly.
Instead, it will be automatically installed by any Tellor feed that uses it,
such as `telliot-feed-examples`.


# Telliot Configuration

After installation, Telliot must be personalized to use your own private keys and endpoints.

First, create the default configuration files:

    telliot config init

The default configuration files are created in a folder called `telliot` in your user home folder:

    Saved config 'main' to ~/telliot/main.yaml
    Saved config 'endpoints' to ~/telliot/endpoints.yaml
    Saved config 'chains' to ~/telliot/chains.json

## Main Configuration File

The main configuration file allows you to choose which network Telliot will interact with.
By default, Telliot is configured to run on Rinkeby testnet, as shown in the example below.
To run on Etherium mainnet, use `chain_id: 1` and `network: mainnet`.

To submit values to the Tellor oracle, a `private_key` must also be configured.

* Example main configuration file.*
```yaml
type: MainConfig
loglevel: INFO
chain_id: 4
network: rinkeby
private_key: ''

```



## Configure endpoints

Edit `endpoints.yaml` to use to your own endpoints.

If you don't have an endpoint, a free one is available at [Infura.io](www.infura.io).  Simply replace `INFURA_API_KEY` with the one provided by Infura

We recommend configuring endpoints for both Etherium mainnet and Rinkeby testnet.

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
  url: wss://rinkeby.infura.io/ws/v3{INFURA_API_KEY}
  explorer: https://rinkeby.etherscan.io

```


## Development setup

1. Make sure that both Python and `pip` are available on the search path.
2. Clone the Telliot Core git repository to your computer, for example in `~/myproject/telliot-core`.
3. Change to the folder containg the repository
4. Perform an [editable installation](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)
5. Install project dependencies
6. Test the development environment


    cd ~/myproject/telliot-core
    pip install -e .
    pip install -r requirements-dev.txt
    pytest
