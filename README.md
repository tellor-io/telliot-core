![CI](https://github.com/tellor-io/pytelliot/actions/workflows/py38.yml/badge.svg)
![Docs](https://github.com/tellor-io/pytelliot/actions/workflows/docs.yml/badge.svg)
[![codecov](https://codecov.io/gh/tellor-io/pytelliot/branch/main/graph/badge.svg?token=S1199HQ2EK)](https://codecov.io/gh/tellor-io/pytelliot)
[![Discord Chat](https://img.shields.io/discord/461602746336935936)](https://discord.com/invite/n7drGjh)
[![Twitter Follow](https://img.shields.io/twitter/follow/wearetellor?style=social)](https://twitter.com/WeAreTellor)

# Telliot

Telliot is a Python framework for interacting with the decentralized TellorX network.

Please refer to the following for additional information:

- [DRAFT Telliot Documentation](https://tellor-io.github.io/pytelliot/)
- [TellorX Whitepaper](https://www.tellor.io/static/media/tellorX-whitepaper.f6527d55.pdf).

# Development Setup

You'll need Python and `pip` on the search path.
Clone the Telliot Core git repository to your computer, for example in `/work/telliot-core`.
Now create an [editable install](https://pip.pypa.io/en/stable/reference/pip_install/#editable-installs)
and download the dependencies of code and test suite by executing:

    cd /work/telliot-core
    pip install -e .
    pip install -r requirements-dev.txt

To test your development environment, run

    pytest
