import pytest
from pydantic import ValidationError

from practice import load

m = load(__file__)

GOOD = {"name": "Ada", "age": 36, "email": "ada@example.com"}


def test_valid_user_and_defaults():
    user = m.parse_user(GOOD)
    assert user.name == "Ada"
    assert user.age == 36
    assert user.tags == []


def test_name_is_stripped_and_age_coerced():
    user = m.parse_user({**GOOD, "name": "  Ada  ", "age": "36"})
    assert user.name == "Ada"
    assert user.age == 36
    assert isinstance(user.age, int)


def test_email_is_lowercased():
    assert m.parse_user({**GOOD, "email": "Ada@Example.COM"}).email == "ada@example.com"


def test_tags_default_is_not_shared():
    a = m.parse_user(GOOD)
    b = m.parse_user(GOOD)
    a.tags.append("x")
    assert b.tags == []


@pytest.mark.parametrize(
    "bad",
    [
        {"name": "", "age": 3, "email": "a@b.c"},
        {"name": "   ", "age": 3, "email": "a@b.c"},
        {"name": "x" * 51, "age": 3, "email": "a@b.c"},
        {"name": "A", "age": -1, "email": "a@b.c"},
        {"name": "A", "age": 151, "email": "a@b.c"},
        {"name": "A", "age": "old", "email": "a@b.c"},
        {"name": "A", "age": 3, "email": "no-at-sign"},
        {"name": "A", "age": 3, "email": "@host"},
        {"name": "A", "age": 3, "email": "me@"},
        {"name": "A", "age": 3, "email": "a@b@c"},
        {"name": "A", "age": 3},
    ],
)
def test_invalid_users(bad):
    with pytest.raises(ValidationError):
        m.parse_user(bad)


def test_boundary_values_are_valid():
    assert m.parse_user({**GOOD, "age": 0}).age == 0
    assert m.parse_user({**GOOD, "age": 150}).age == 150
    assert m.parse_user({**GOOD, "name": "x" * 50}).name == "x" * 50


def test_problems_lists_failing_fields_sorted_once():
    with pytest.raises(ValidationError) as info:
        m.parse_user({"name": "", "age": -5, "email": "bad"})
    assert m.problems(info.value) == ["age", "email", "name"]


def test_problems_missing_field():
    with pytest.raises(ValidationError) as info:
        m.parse_user({"name": "A", "age": 3})
    assert m.problems(info.value) == ["email"]


def test_parse_users_splits_valid_and_bad():
    rows = [
        GOOD,
        {"name": "", "age": 1, "email": "a@b.c"},
        {"name": "Bo", "age": "7", "email": "bo@x.org"},
        {"name": "Cy", "age": "n/a", "email": "nope"},
    ]
    users, bad = m.parse_users(rows)
    assert [u.name for u in users] == ["Ada", "Bo"]
    assert bad == {1: ["name"], 3: ["age", "email"]}


def test_parse_users_empty():
    assert m.parse_users([]) == ([], {})
