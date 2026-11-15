import collections.abc
import typing
from typing import get_args, get_origin, get_type_hints

from practice import load

m = load(__file__)


def hints(func):
    return get_type_hints(func)


def test_total():
    assert hints(m.total) == {"prices": list[float], "tax_rate": float, "return": float}
    assert m.total([10.0, 5.0], 0.1) == 16.5


def test_find_user():
    assert hints(m.find_user) == {"users": dict[str, int], "name": str, "return": int | None}
    assert m.find_user({"ann": 1}, "ann") == 1
    assert m.find_user({"ann": 1}, "bob") is None


def test_shout():
    assert hints(m.shout) == {"words": list[str], "return": str}
    assert m.shout(["hi", "there"]) == "HI THERE!"


def test_apply_twice():
    h = hints(m.apply_twice)
    assert set(h) == {"f", "x", "return"}
    assert h["x"] is int and h["return"] is int
    assert get_origin(h["f"]) is collections.abc.Callable
    assert get_args(h["f"]) == ([int], int)
    assert m.apply_twice(lambda n: n + 3, 1) == 7


def test_set_mode():
    h = hints(m.set_mode)
    assert h == {"mode": typing.Literal["r", "w"], "return": str}
    assert m.set_mode("r") == "mode=r"


def test_log(capsys):
    assert hints(m.log) == {"message": str, "return": type(None)}
    m.log("hello")
    assert capsys.readouterr().out == "hello\n"
