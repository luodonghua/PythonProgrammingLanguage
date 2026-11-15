import pytest

from practice import load

m = load(__file__)


def test_commit_on_success():
    db = {"a": 1}
    with m.transaction(db) as tx:
        tx["a"] = 2
        tx["b"] = 3
    assert db == {"a": 2, "b": 3}


def test_commit_includes_deletions():
    db = {"a": 1, "b": 2}
    with m.transaction(db) as tx:
        del tx["a"]
    assert db == {"b": 2}


def test_db_untouched_inside_block():
    db = {"a": 1}
    with m.transaction(db) as tx:
        tx["a"] = 99
        assert db == {"a": 1}
        assert tx is not db


def test_rollback_on_error_and_error_propagates():
    db = {"ann": 10, "bob": 0}
    with pytest.raises(RuntimeError, match="crash"):
        with m.transaction(db) as tx:
            tx["ann"] -= 5
            tx["bob"] += 5
            raise RuntimeError("crash")
    assert db == {"ann": 10, "bob": 0}


def test_same_dict_object_is_kept():
    db = {"a": 1}
    same = db
    with m.transaction(db) as tx:
        tx["a"] = 5
    assert same is db
    assert same == {"a": 5}


def test_collector_swallows_listed_error():
    with m.ErrorCollector(ValueError) as c:
        int("x")
    assert len(c.errors) == 1
    assert isinstance(c.errors[0], ValueError)
    assert c.ok is False


def test_collector_ok_when_no_error():
    with m.ErrorCollector(ValueError) as c:
        pass
    assert c.errors == []
    assert c.ok is True


def test_collector_lets_other_errors_through():
    with pytest.raises(KeyError):
        with m.ErrorCollector(ValueError) as c:
            {}["missing"]
    assert c.errors == []


def test_collector_default_collects_exception_but_not_base_exception():
    with m.ErrorCollector() as c:
        raise RuntimeError("x")
    assert c.ok is False
    with pytest.raises(KeyboardInterrupt):
        with m.ErrorCollector():
            raise KeyboardInterrupt


def test_collector_multiple_types_and_reuse_in_loop():
    collected = []
    for text in ["1", "x", "2", None]:
        with m.ErrorCollector(ValueError, TypeError) as c:
            int(text)
        collected.append(c.ok)
    assert collected == [True, False, True, False]
