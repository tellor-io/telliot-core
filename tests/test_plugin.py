from telliot.plugin import telliot_plugins


def test_discovered_plugins():

    assert "telliot_examples" in telliot_plugins
