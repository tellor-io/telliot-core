from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from typing import Dict
from typing import List

import pytest
import yaml
from clamfig.base import deserialize
from clamfig.base import Serializable
from clamfig.base import serialize


@dataclass
class Dates(Serializable):
    d: date = date(1999, 12, 31)
    t: time = time()
    dt: datetime = datetime(1999, 12, 13, 23, 59, 59)


@dataclass
class Options(Serializable):
    a: bool = False
    b: str = ""


@dataclass
class User(Serializable):
    options: Options = Options()


@dataclass
class File(Serializable):
    id: str = ""
    name: str = ""
    data: bytes = b""


@dataclass
class Page(Serializable):
    files: List[File] = field(default_factory=list)


@dataclass
class PageDict(Serializable):
    files: Dict[str, File] = field(default_factory=list)


@dataclass
class Tree(Serializable):
    name: str = ""
    related: Tree = field(default_factory=lambda: Tree)


@dataclass
class Amount(Serializable):
    total: Decimal = Decimal(0)


def test_json_dates():
    now = datetime.now()
    obj = Dates(d=now.date(), t=now.time(), dt=now)

    state = obj.get_state()
    state2 = serialize(obj)
    assert state == state2
    data = json.dumps(state, indent=2)
    print(data)
    print(yaml.dump(state, sort_keys=False))
    r = Dates.from_state(json.loads(data))
    assert r.d == obj.d and r.t == obj.t and r.dt == r.dt


def test_json_decimal():
    d = Decimal("3.9")
    obj = Amount(total=d)
    state = obj.get_state()
    data = json.dumps(state, sort_keys=False)
    r = Amount.from_state(json.loads(data))
    assert r.total == d


def test_json_nested():
    obj = User(options=Options(a=True, b="Yes"))
    state = obj.get_state()
    data = json.dumps(state, indent=2)
    print(data)
    print(yaml.dump(state, sort_keys=False))
    state2 = json.loads(data)
    r = User.from_state(state2)
    assert r.options.a == obj.options.a and r.options.b == obj.options.b


def test_json_bytes():
    obj = File(name="test.png", data=b"abc")
    state = obj.get_state()
    data = json.dumps(state, indent=2)
    print(data)
    print(yaml.dump(state, sort_keys=False))
    r = File.from_state(json.loads(data))
    assert r.name == obj.name and r.data == obj.data


def test_json_list():
    f1 = File(name="test.png", data=b"abc")
    f2 = File(name="blueberry.jpg", data=b"123")
    obj = Page(files=[f1, f2])
    state = obj.get_state()
    data = json.dumps(state, indent=2)
    print(data)
    print(yaml.dump(state, sort_keys=False))
    r = Page.from_state(json.loads(data))
    assert len(r.files) == 2
    assert r.files[0].name == f1.name and r.files[0].data == f1.data
    assert r.files[1].name == f2.name and r.files[1].data == f2.data
    assert r.files[1].id == f2.id
    r2 = deserialize(json.loads(data))
    assert isinstance(r2, Page)
    assert r2.files[0].name == f1.name and r2.files[0].data == f1.data
    assert r2.files[1].name == f2.name and r2.files[1].data == f2.data
    assert r2.files[1].id == f2.id


def test_json_cyclical():
    b = Tree(name="b")
    a = Tree(name="a", related=b)

    # Create a cyclical ref
    b.related = a

    obj = a
    with pytest.raises(RecursionError):
        state = obj.get_state()
        data = json.dumps(state, indent=2)
        print(data)
        r = Tree.from_state(json.loads(data))
        assert r.name == "a"
        assert r.related.name == b.name
        assert r.related.related == r


def test_json_dict():
    f1 = File(name="test.png", data=b"abc")
    f2 = File(name="blueberry.jpg", data=b"123")
    obj = PageDict(files={"id1": f1, "id2": f2, "id_dup": f2})
    state = obj.get_state()
    data = json.dumps(state, indent=2)
    print(data)
    print(yaml.dump(state, sort_keys=False))
    r = PageDict.from_state(json.loads(data))
    assert len(r.files) == 3
    assert r.files["id1"].name == f1.name and r.files["id1"].data == f1.data
    assert r.files["id2"].name == f2.name and r.files["id2"].data == f2.data
    assert r.files["id2"].id == f2.id


def test_fields():
    obj = User(options=Options(a=True, b="Yes"))
    print(obj.__repr__())
    print(asdict(obj))


def test_dup_classes():
    with pytest.raises(NameError):

        class Options(Serializable):
            a: bool = False
            b: str = ""
