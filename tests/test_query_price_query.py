from telliot.queries.price_query import PriceQuery


def test_constructor():
    q = PriceQuery(asset='BTC', currency='USD')

    assert q.tip_data == b"qid-101?what is the current value of btc in usd?abi_type=ufixed64x6,packed=true"

    assert q.request_id.hex() == '58a476e45522ad46d48b17bdac8600bb63656435ee938f0d72990cc3007fb7ad'



def test_price_type():
    q = PriceQuery(asset='ETH', currency='USD', price_type='24hr_twap')

    assert q.tip_data == b"qid-101?what is the 24hr_twap value of eth in usd?abi_type=ufixed64x6,packed=true"

    assert q.request_id.hex() == 'c89db5d2c69b59e8a4260ad119dc1710683341a69d985437717b6b92aadd203e'

