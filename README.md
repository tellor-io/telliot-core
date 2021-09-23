# telliot
A Python implementation of Telliot, a tool for interacting with the [Tellor Oracle](https://www.tellor.io/static/media/tellorX-whitepaper.f6527d55.pdf).

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
#### 2. update environment variables
In `src/telliot/reporter_plugins/rinkeby_eth_usd`, rename `.env.example` to `.env` and update the placeholder values for `PRIVATE_KEY` and `NODE_URL` to your own private key and Rinkeby network endpoint.
#### 3. start reporting
```
telliot report
```

## Contributing
### dev environment setup
