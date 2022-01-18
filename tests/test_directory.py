from telliot_core.directory import ContractDirectory
from telliot_core.directory import ContractInfo
from telliot_core.directory import directory_config_file


def test_contract_info():
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
    assert isinstance(c.abi, list)


def test_contract_directory():
    cd = ContractDirectory()
    assert len(cd.entries) == 6

    master = cd.find(name="tellorx-master")[0]
    assert isinstance(master.abi, list)

    treasury = cd.find(address="0x2dB91443f2b562B8b2B2e8E4fC0A3EDD6c195147")[0]
    assert isinstance(treasury.abi, list)

    tellorx = cd.find(name="tellorx")
    assert len(tellorx) == 5

    mainnet_contracts = cd.find(chain_id=1)
    assert isinstance(mainnet_contracts[0], ContractInfo)


def test_directory_config_file():
    cd = directory_config_file().get_config()
    assert len(cd.entries) == 6
