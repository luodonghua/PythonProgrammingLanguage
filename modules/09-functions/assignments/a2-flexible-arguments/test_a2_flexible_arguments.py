import inspect

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("parts", "expected"),
    [
        (("a", "b", "c"), "a/b/c"),
        (("a/", "/b"), "a/b"),
        (("/usr", "local", "bin"), "/usr/local/bin"),
        (("a", "", "b"), "a/b"),
        (("solo",), "solo"),
        ((), ""),
    ],
)
def test_join_path(parts, expected):
    assert m.join_path(*parts) == expected


def test_join_path_custom_separator():
    assert m.join_path("a", "", "b", sep="\\") == "a\\b"
    assert m.join_path("x", "y", sep="-") == "x-y"


def test_join_path_sep_is_keyword_only():
    kinds = {p.name: p.kind for p in inspect.signature(m.join_path).parameters.values()}
    assert kinds["sep"] is inspect.Parameter.KEYWORD_ONLY
    assert m.join_path("a", "b") == "a/b"


def test_clamp():
    assert m.clamp(150) == 100
    assert m.clamp(-5) == 0
    assert m.clamp(50) == 50
    assert m.clamp(5, 10, 20) == 10
    assert m.clamp(5, high=3, low=1) == 3


def test_clamp_value_is_positional_only():
    kind = inspect.signature(m.clamp).parameters["value"].kind
    assert kind is inspect.Parameter.POSITIONAL_ONLY
    assert m.clamp(1) == 1


def test_greet():
    assert m.greet("Ada") == "Hello, Ada!"
    assert m.greet("Ada", greeting="Hi") == "Hi, Ada!"
    assert m.greet("Ada", punctuation="?") == "Hello, Ada?"


def test_greet_needs_keywords():
    assert m.greet("Ada", greeting="Hi") == "Hi, Ada!"
    with pytest.raises(TypeError):
        m.greet("Ada", "Hi")


def test_average():
    assert m.average(4) == 4
    assert m.average(1, 2, 3, 4) == 2.5


def test_make_tag():
    assert m.make_tag("br") == "<br></br>"
    assert m.make_tag("p", "hi") == "<p>hi</p>"


def test_make_tag_attributes_keep_order():
    assert m.make_tag("a", "home", href="/", id="top") == '<a href="/" id="top">home</a>'
    assert m.make_tag("a", "home", id="top", href="/") == '<a id="top" href="/">home</a>'


def test_call_with():
    assert m.call_with(max, 3, 9, 4) == 9
    assert m.call_with(sorted, [3, 1, 2], reverse=True) == [3, 2, 1]
    assert m.call_with(lambda: "no args") == "no args"
