![CI](https://github.com/tellor-io/pytelliot/actions/workflows/tox.yml/badge.svg)
![Docs](https://github.com/tellor-io/pytelliot/actions/workflows/docs.yml/badge.svg)
[![codecov](https://codecov.io/gh/tellor-io/pytelliot/branch/main/graph/badge.svg?token=S1199HQ2EK)](https://codecov.io/gh/tellor-io/pytelliot)
[![Discord Chat](https://img.shields.io/discord/461602746336935936)](https://discord.com/invite/n7drGjh)
[![Twitter Follow](https://img.shields.io/twitter/follow/wearetellor?style=social)](https://twitter.com/WeAreTellor)

# Telliot

Telliot is a Python framework for interacting with the decentralized TellorX network.

Please referto the following for additional information

- [DRAFT Telliot Documentation](https://tellor-io.github.io/pytelliot/) 
- [TellorX Whitepaper](https://www.tellor.io/static/media/tellorX-whitepaper.f6527d55.pdf).

# Development Status

## Rough roadmap & spec
### due October 1st:
- ✔️ cli interface
- ✔️ off-chain data getter & database
- ✔️ data submitter
- profit calculator
### later:
- tipping, voting, disputing
- gui for data feed and submitter

## Setup & usage
Here's how to report the price of ETH in USD to the oracle on the Rinkeby test network.
#### 1. download package
```
pip install telliot
```
(not yet released to PyPI)

#### 2. Start reporting
```
telliot report btc-usd-median
```

