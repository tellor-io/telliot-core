from telliot.queries.static_query import StaticQuery
from telliot.queries.query import ResponseType

def test_static_query():
    q = StaticQuery(uid='qid-999',
                    name='Fundamental Question',
                    static_question='What is the meaning of life',
                    static_response_type=ResponseType(abi_type='string')
                    )

    assert q.tip_data == b'qid-999?what is the meaning of life?abi_type=string,packed=false'

    response = q.response_type.encode(
        'Please refer to: https://en.wikipedia.org/wiki/Meaning_of_life')
    assert isinstance(response, bytes)
