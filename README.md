![CI](https://github.com/tellor-io/pytelliot/actions/workflows/tox.yml/badge.svg)
![Docs](https://github.com/tellor-io/pytelliot/actions/workflows/docs.yml/badge.svg)
[![codecov](https://codecov.io/gh/tellor-io/pytelliot/branch/main/graph/badge.svg?token=S1199HQ2EK)](https://codecov.io/gh/tellor-io/pytelliot)
[![Discord Chat](https://img.shields.io/discord/461602746336935936)](https://discord.com/invite/n7drGjh)
[![Twitter Follow](https://img.shields.io/twitter/follow/wearetellor?style=social)](https://twitter.com/WeAreTellor)

# Telliot

Telliot is a Python framework for interacting with the decentralized TellorX network.

Please refer to the following for additional information

- [DRAFT Telliot Documentation](https://tellor-io.github.io/pytelliot/)
- [TellorX Whitepaper](https://www.tellor.io/static/media/tellorX-whitepaper.f6527d55.pdf).

# Development Status

## Rough roadmap & spec
### by Nov 1st:
- test with TellorX rinkeby deployment
- publish to PyPI

### later:
- tipping, voting, disputing
- gui for data feed and submitter

## Setup & usage
Here's how to report the price of BTC in USD to the oracle on the Rinkeby test network.
#### 1. download package
```
pip install telliot
```
(not yet released to PyPI)

#### 2. Start reporting
```
telliot report btc-usd-median
```

## dev setup
- Clone repository
```
git clone https://github.com/tellor-io/pytelliot.git && cd pytelliot
```
- Create virtual environment
```
python -m venv env
```
- Activate virtual environment
```
source env/bin/activate
```
- Install dependencies
```
pip install -r requirements-dev.txt
```
- Once your dev environment is set up, make desired changes, create new tests for those changes,
and conform to the style & typing format of the project. To do so, in the project home directory:

Run tests:
```
pytest
```
Check typing:
```
mypy src --strict --implicit-reexport --ignore-missing-imports --disable-error-code misc
```
Check style:
```
tox -e style
```
(you may need to make changes and run again)
- Once all those pass, you're ready to make a pull request to the project's main branch.
- Link any related issues, tag desired reviewers, and watch the [#pytelliot](https://discord.gg/URXVQdGjAT) channel in the
community discord for updates.
