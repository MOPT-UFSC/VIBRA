from vibra.utils.bidict import bidict


def test_insertions():
    my_dict = bidict()

    my_dict["a"] = 1
    my_dict["b"] = 2
    my_dict["c"] = 1
    my_dict["d"] = (8, 9)

    assert my_dict.inverse == {1: ["a", "c"], 2: ["b"], (8, 9): ["d"]}
    assert my_dict == {"a": 1, "b": 2, "c": 1, "d": (8, 9)}

def test_popitem():
    my_dict = bidict()

    my_dict["a"] = 1
    my_dict["b"] = 2
    my_dict["c"] = (8, 9)
    my_dict["d"] = 1

    another_dict = bidict({"a": 1, "b": 2})
    my_dict.popitem()
    my_dict.popitem()

    assert my_dict == another_dict
    assert my_dict.inverse == another_dict.inverse

def test_pop():
    my_dict = bidict({"a": 1, "b": 2, "c": 1, "d": 2})
    another_dict = bidict({"a": 1, "b": 2})

    my_dict.pop("c")
    my_dict.pop("d")

    assert my_dict == another_dict
    assert my_dict.inverse == another_dict.inverse

def test_update():
    my_dict = bidict({"a": (2, 3), (6, 7): "test", 9: "d"})
    another_dict = bidict({"a": (2, 3), (6, 7): "test", 9: "d", "lva": "ufsc", 12: 12})

    my_dict.update({"lva": "ufsc", 12: 12})

    assert my_dict == another_dict
    assert my_dict.inverse == another_dict.inverse

def test_setdefault():
    my_dict = bidict({"a": 2})
    another_dict = bidict({"a": 2, (8, 9): "test", 3: ()})

    my_dict.setdefault((8, 9), "test")
    my_dict.setdefault(3, ())

    assert my_dict == another_dict
    assert my_dict.inverse == another_dict.inverse