from telliot.model.serializable import SerializableModel


def test_main():
    """Test model creation, serialization and deserialization"""

    class ModelA(SerializableModel):
        a: str = "a"

    a = ModelA()

    ad = a.dict()
    assert ad.get("type") == "ModelA"
    assert ad.get("inputs")["a"] == "a"

    jstr = a.json()
    print(jstr)

    a_new = SerializableModel.parse_raw(jstr)

    assert isinstance(a_new, ModelA)
    assert a_new.a == "a"
