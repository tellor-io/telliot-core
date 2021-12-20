from datetime import datetime

from telliot_core.utils.timestamp import TimeStamp


def test_main():
    dt = datetime(1999, 12, 31, 12, 59, 59)
    dt_ts = TimeStamp(dt.timestamp())

    print(dt_ts.dt)

    d = datetime(1999, 12, 31)
    d_ts = TimeStamp(d.timestamp())
    print(d_ts.dt)

    print(d_ts.age)


def test_repr():
    ts = 1639756400
    ts = TimeStamp(ts)
    assert repr(ts) == "TimeStamp(1639756400)"
