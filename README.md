![CI](https://github.com/tellor-io/telliot-core/actions/workflows/py312.yml/badge.svg)
![Docs](https://github.com/tellor-io/telliot-core/actions/workflows/docs.yml/badge.svg)
[![codecov](https://codecov.io/gh/tellor-io/pytelliot/branch/main/graph/badge.svg?token=S1199HQ2EK)](https://codecov.io/gh/tellor-io/pytelliot)
[![Discord Chat](https://img.shields.io/discord/461602746336935936)](https://discord.com/invite/n7drGjh)
[![Twitter Follow](https://img.shields.io/twitter/follow/wearetellor?style=social)](https://twitter.com/WeAreTellor)

# Telliot Core

Telliot is a command line tool and software development kit (SDK) for interacting with the [Tellor protocol](https://docs.tellor.io/tellor/whitepaper/introduction).

Documentation for this package lives in this README. The
[telliot-core site](https://tellor-io.github.io/telliot-core/) pages are placeholders that link
back here, and general Tellor client documentation (datafeeds, spot prices, reporting) lives in
the [telliot-feeds docs](https://tellor-io.github.io/telliot-feeds/).

To become a Tellor reporter, begin by installing the
[telliot-feeds](https://github.com/tellor-io/telliot-feeds) package.

## Install

    pip install telliot-core

Requires Python >=3.12,<3.13.

## Development

Prerequisites: Python 3.12 and [uv](https://docs.astral.sh/uv/).

    uv sync    # create .venv and install all dev tools from uv.lock

Run the unit tests (a local Hardhat node is required for the ape fixtures):

    npm ci && npx hardhat node
    uv run pytest

Check typing and style:

    uv run mypy --strict src --implicit-reexport --ignore-missing-imports --disable-error-code misc
    uv run pre-commit run --all-files

Once all those pass, make your pull request to `main`, link any related issues, tag desired
reviewers, and watch the [#telliot-core](https://discord.gg/URXVQdGjAT) channel in the community
discord for updates.

## Adding support for a new chain

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

## New release checklist

1. Ensure all tests are passing on main.
2. Update **version** in `src/telliot_core/__init__.py`.
3. On GitHub, draft a new release with a tag matching the version (Example: `v0.4.3`), titled
   "Release 0.4.3", with auto-generated release notes, and check "This is a pre-release".
4. Publishing the release runs the Publish workflow, which ships the package to Test PyPI.
   Test the new version there (`pip install -i https://test.pypi.org/simple/ telliot-core==<version>`).
5. Edit the release and uncheck "This is a pre-release", then publish again; the workflow
   releases the final package to [PyPI](https://pypi.org/project/telliot-core/).
6. Bump **version** in `__init__.py` to the next development version.
