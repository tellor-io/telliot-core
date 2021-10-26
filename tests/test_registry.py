from telliot.model.registry import ModelRegistry
from telliot.model.registry import RegisteredModel

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

    print(ModelRegistry._registry)


