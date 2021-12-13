import pytest
from telliot_core.apps.singleton import Singleton


class SomeClass(metaclass=Singleton):
    pass


class OtherClass(metaclass=Singleton):
    pass


def test_main():

    # Create the new instance
    m = SomeClass()
    assert isinstance(m, SomeClass)

    # Get the enw instance
    n = SomeClass.get()
    assert n is m

    with pytest.raises(Exception):
        _ = SomeClass()

    # Create the new instance
    x = OtherClass()
    assert isinstance(x, OtherClass)

    # Get the enw instance
    y = OtherClass.get()
    assert y is x

    with pytest.raises(Exception):
        _ = OtherClass()

    SomeClass.destroy()
    with pytest.raises(LookupError):
        SomeClass.get()
