from practice import load

m = load(__file__)

CONFIG = {"db": {"host": "localhost", "port": 5432}, "debug": False}


def test_get_path_found():
    assert m.get_path(CONFIG, "db.host") == "localhost"
    assert m.get_path(CONFIG, "db.port") == 5432


def test_get_path_returns_nested_dict():
    assert m.get_path(CONFIG, "db") == {"host": "localhost", "port": 5432}


def test_get_path_falsy_value_is_not_missing():
    assert m.get_path(CONFIG, "debug", "fallback") is False


def test_get_path_missing_uses_default():
    assert m.get_path(CONFIG, "db.user", "admin") == "admin"
    assert m.get_path(CONFIG, "cache.size") is None


def test_get_path_through_non_dict():
    assert m.get_path(CONFIG, "db.host.name", "nope") == "nope"
    assert m.get_path(CONFIG, "") is None


def test_set_path_creates_dicts():
    d = {}
    assert m.set_path(d, "a.b.c", 1) is None
    assert d == {"a": {"b": {"c": 1}}}


def test_set_path_keeps_siblings():
    d = {"a": {"x": 1}}
    m.set_path(d, "a.y", 2)
    m.set_path(d, "top", 3)
    assert d == {"a": {"x": 1, "y": 2}, "top": 3}


def test_merge_inventories():
    one = {"apple": 2, "pear": 1}
    two = {"apple": 3}
    assert m.merge_inventories(one, two) == {"apple": 5, "pear": 1}
    assert one == {"apple": 2, "pear": 1}
    assert two == {"apple": 3}


def test_merge_inventories_edge_cases():
    assert m.merge_inventories() == {}
    result = m.merge_inventories({"a": 1}, {}, {"b": 2}, {"a": 1})
    assert result == {"a": 2, "b": 2}
    assert type(result) is dict


def test_low_stock():
    assert m.low_stock({"apple": 5, "pear": 1, "fig": 0}) == ["fig", "pear"]
    assert m.low_stock({"apple": 5, "pear": 1}, threshold=6) == ["apple", "pear"]
    assert m.low_stock({}) == []


def test_count_by_field():
    records = [{"c": "red"}, {"c": "red"}, {"c": "blue"}, {}]
    assert m.count_by_field(records, "c") == {"red": 2, "blue": 1, None: 1}


def test_count_by_field_empty():
    assert m.count_by_field([], "c") == {}
