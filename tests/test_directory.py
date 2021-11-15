from telliot_core.directory.tellorx import TellorDirectory


def test_telliot_directory():
    # Assert chain_id 1 and 4
    assert 1 in TellorDirectory
    assert 4 in TellorDirectory

    rinkeby_master_address = TellorDirectory[4]["master"]["address"]
    assert isinstance(rinkeby_master_address, str)

    rinkeby_master_abi = TellorDirectory[4]["master"]["abi"]
    assert isinstance(rinkeby_master_abi, list)
