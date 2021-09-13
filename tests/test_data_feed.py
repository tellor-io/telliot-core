""" Simple example of creating a "plug-in" data feed

"""
import telliot.registry


def test_AssetPriceFeed():
    btc_usd_median = telliot.registry.data_feeds['btc-usd-median']

    x = btc_usd_median.update_value()


