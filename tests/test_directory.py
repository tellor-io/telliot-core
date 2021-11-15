from telliot_core.directory.tellorx import TelliotDirectory


def test_telliot_directory():
    # Assert chain_id 1 and 4
    assert 1 in TelliotDirectory
    assert 4 in TelliotDirectory

    rinkeby_master_address = TelliotDirectory[4]['master']['address']
    assert isinstance(rinkeby_master_address, str)

    rinkeby_master_abi = TelliotDirectory[4]['master']['abi']
    assert isinstance(rinkeby_master_abi, list)
