from telliot.model.registry import Serializer
from telliot.model.registry import RegisteredModel
from telliot.model.registry import SimpleSerial
import dataclasses

def test_main():
    """Test model creation, serialization and deserialization"""

    class ModelA(RegisteredModel):
        a: str = "a"

    a = ModelA()

    ad = a.to_state()
    assert ad[0] == "ModelA"
    assert ad[1]["a"] == "a"

    jstr = a.to_json()
    print(jstr)

    a_new = RegisteredModel.from_json(jstr)

    assert isinstance(a_new, ModelA)
    assert a_new.a == "a"

    print(Serializer._registry)

def test_simple_serial():

    @dataclasses.dataclass
    class ModelB(SimpleSerial):
        a: str = "a"

    a = ModelB()

    ad = a.to_state()
    assert ad[0] == "ModelB"
    assert ad[1]["a"] == "a"

    jstr = a.to_json()
    print(jstr)

    a_new = RegisteredModel.from_json(jstr)

    assert isinstance(a_new, ModelB)
    assert a_new.a == "a"

    print(Serializer._registry)

