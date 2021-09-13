from datetime import datetime

import pytest
from pydantic.error_wrappers import ValidationError
from telliot.base import Answer
from telliot.base import TimeStampedAnswer
from telliot.base import TimeStampedFixed
from telliot.base import TimeStampedFloat


def test_Answer():
    _ = Answer[int](5.0)

    with pytest.raises(ValidationError):
        _ = Answer[int]("not_an_int")


def test_TimeStampedAnswer():
    v1 = TimeStampedAnswer[int](5.0)

    assert isinstance(v1.ts, datetime)


def test_TimeStampedFixed():
    f = TimeStampedFixed(2.123456)
    assert f.decimals == 6
    assert f.int == 2123456
    assert f.val == 2.123456


def test_TimeStampedFixed_resolution():
    f = TimeStampedFixed(2.1234567)
    assert f.int == 2123457
    assert f.val == 2.123457


def test_TimeStampedFloat():
    obj = TimeStampedFloat(3.14)
    assert obj.val == 3.14

    obj = TimeStampedFloat("3.14")
    assert obj.val == 3.14

    obj = TimeStampedFloat(3.14, ts=datetime.now())

    obj.ts = datetime.now()

    with pytest.raises(TypeError):
        _ = TimeStampedFloat()
