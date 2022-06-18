import time

import pytest

from telliot_core.directory import contract_directory
from telliot_core.directory import ContractInfo


def test_contract_info():
    """Test the ContractInfo class"""
    c = ContractInfo(
        org="tellor",
        name="tellorx-master",
        address={
            1: "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
            4: "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0",
        },
        abi_file="tellorx-master-abi.json",
    )

    # Make sure we can get ABI
    assert isinstance(c.get_abi(), list)


def test_contract_directory():
    """Test the contract directory"""
    cd = contract_directory
    assert len(cd.entries) > 6

    master = cd.find(name="tellorx-master")[0]
    assert isinstance(master.get_abi(), list)

    treasury = cd.find(address="0x2dB91443f2b562B8b2B2e8E4fC0A3EDD6c195147")[0]
    assert isinstance(treasury.get_abi(0), list)

    tellorx = cd.find(name="tellorx")
    assert len(tellorx) == 5

    mainnet_contracts = cd.find(chain_id=1)
    assert isinstance(mainnet_contracts[0], ContractInfo)


def test_directory_config_file():
    """Test the contract directory config file"""
    cd = contract_directory
    assert len(cd.entries) > 6


@pytest.mark.skip("Runs into API rate limits with other tests")
def test_abi_mainnet_retrieval():
    """Test the ABI retrieval from mainnet"""
    cd = contract_directory
    entries = cd.find(name="tellor-provider-id41", chain_id=1)
    info = entries[0]
    print(info)
    abi = info.get_abi(chain_id=1)
    assert abi[0]["name"] == "tellorReport"


@pytest.mark.skip("Long test")
def test_abis():
    """Make sure that ABI is provided or can be retrieved for all contracts.
    Very slow due to etherscan rate limits with no api_key.
    """
    for info in contract_directory.entries.values():
        print(f"Getting ABI for {info.name}")
        time.sleep(2)
        abi = info.get_abi()
        assert isinstance(abi, list)
        assert len(abi) > 0
