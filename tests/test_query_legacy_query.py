from telliot.queries.legacy_query import LegacyQuery
from telliot.queries.legacy_query import LegacyPriceQuery


def test_legacy_query():
    """Test legacy query"""
    q = LegacyQuery(uid='qid-100',
                    name='name',
                    legacy_request_id=100,
                    legacy_question=b'legacy question')
    assert q.response_type.abi_type == 'ufixed256x6'
    assert q.response_type.packed == False
    assert q.request_id.hex() == '0000000000000000000000000000000000000000000000000000000000000064'
    assert q.tip_data == b'qid-100?legacy question?abi_type=ufixed256x6,packed=false'


def test_legacy_price_query():
    """Test legacy price query"""
    q = LegacyPriceQuery(name='BTC/USD Current Price',
                         uid='qid-99',
                         legacy_request_id=99,
                         asset='btc',
                         currency='usd',
                         price_type='current')

    assert q.tip_data == b'qid-99?what is the current value of btc in usd (warning:deprecated)?abi_type=ufixed256x6,packed=false'
    assert q.request_id.hex() == '0000000000000000000000000000000000000000000000000000000000000063'
