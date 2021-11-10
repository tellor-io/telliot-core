from dataclasses import dataclass

from telliot_core.queries.query import OracleQuery


def test_main():
    @dataclass
    class MyQuery(OracleQuery):
        text: str
        val: int = 3

    q = MyQuery("asdf")
    state = q.get_state()
    print(state)
    assert state == {"type": "MyQuery", "text": "asdf", "val": 3}
