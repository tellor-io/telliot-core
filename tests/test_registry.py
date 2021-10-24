from telliot.model.registry import RegisteredModel


def test_main():
    """Test model creation, serialization and deserialization"""

    class ModelA(RegisteredModel):
        a: str = "a"

    a = ModelA()

    ad = a.dict()
    assert ad.get("type") == "ModelA"
    assert ad.get("inputs")["a"] == "a"

    jstr = a.json()
    print(jstr)

    a_new = RegisteredModel.parse_raw(jstr)

    assert isinstance(a_new, ModelA)
    assert a_new.a == "a"
