""" Unit tests for base module

"""
from datetime import datetime

import pytest
from telliot.answer import Answer
from telliot.answer import TimeStampedAnswer
from telliot.answer import TimeStampedFixed
from telliot.answer import TimeStampedFloat


def test_TimeStampedAnswer():
    """Test creating instance of TimeStampedAnswer & attribute types."""
    v1 = TimeStampedAnswer[int](5.0)

    assert isinstance(v1.ts, datetime)


def test_TimeStampedFixed():
    """Test creating instance of TimeStampedFixed & attribute types."""
    f = TimeStampedFixed(2.123456)
    assert f.decimals == 6
    assert f.int == 2123456
    assert f.val == 2.123456


def test_TimeStampedFixed_resolution():
    """Test creating instance of TimeStampedFixed & type casting."""
    f = TimeStampedFixed(2.1234567)
    assert f.int == 2123457
    assert f.val == 2.123457


def test_TimeStampedFloat():
    """Test creating instances of TimeStampedFloat & type casting."""
    obj = TimeStampedFloat(3.14)
    assert obj.val == 3.14

    obj = TimeStampedFloat("3.14")
    assert obj.val == 3.14

    obj = TimeStampedFloat(3.14, ts=datetime.now())

    obj.ts = datetime.now()

    with pytest.raises(TypeError):
        _ = TimeStampedFloat()
