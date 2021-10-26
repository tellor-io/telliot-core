
from telliot.queries.query import OracleQuery
from dataclasses import dataclass


def test_main():

    @dataclass
    class MyQuery(OracleQuery):
        text: str
        val: int = 3

    q = MyQuery('asdf')
    state = q.to_state()
    print(state)
    assert state == ('MyQuery', {'text': 'asdf', 'val': 3})
