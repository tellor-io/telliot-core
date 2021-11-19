from telliot_core.directory.tellorx import tellor_directory


def test_telliot_directory():

    tellor_contracts = tellor_directory.find(org="tellor")
    assert len(tellor_contracts) == 8

    rinkeby_contracts = tellor_directory.find(org="tellor", chain_id=4)
    assert len(rinkeby_contracts) == 4

    tellor_master_rinkeby = tellor_directory.find(
        org="tellor", name="master", chain_id=4
    )
    assert len(tellor_master_rinkeby) == 1
