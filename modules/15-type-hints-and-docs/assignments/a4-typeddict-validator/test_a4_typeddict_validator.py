from typing import TypedDict

import pytest

from practice import load

m = load(__file__)

GOOD = {"title": "Dune", "pages": 412, "tags": ["sf", "classic"]}


def test_valid_data():
    assert m.validate(GOOD, m.Book) == []
    assert m.validate({"title": "x", "pages": 1, "tags": []}, m.Book) == []


def test_missing_keys_in_schema_order():
    assert m.validate({}, m.Book) == [
        "missing key: title",
        "missing key: pages",
        "missing key: tags",
    ]
    assert m.validate({"title": "x", "tags": []}, m.Book) == ["missing key: pages"]


def test_wrong_types():
    data = {"title": 5, "pages": "412", "tags": "sf"}
    assert m.validate(data, m.Book) == [
        "title must be str",
        "pages must be int",
        "tags must be list[str]",
    ]


def test_bool_is_not_an_int():
    data = dict(GOOD, pages=True)
    assert m.validate(data, m.Book) == ["pages must be int"]


def test_list_items_are_checked():
    data = dict(GOOD, tags=["ok", 3])
    assert m.validate(data, m.Book) == ["tags must be list[str]"]


def test_unexpected_keys_are_sorted_and_come_last():
    data = dict(GOOD, zeta=1, alpha=2)
    assert m.validate(data, m.Book) == ["unexpected key: alpha", "unexpected key: zeta"]


def test_mixed_problems():
    data = {"title": 5, "extra": 1}
    assert m.validate(data, m.Book) == [
        "title must be str",
        "missing key: pages",
        "missing key: tags",
        "unexpected key: extra",
    ]


def test_works_with_other_schemas():
    class Point(TypedDict):
        x: float
        ok: bool
        ids: list[int]

    assert m.validate({"x": 1.5, "ok": False, "ids": [1, 2]}, Point) == []
    assert m.validate({"x": "1", "ok": 0, "ids": [True]}, Point) == [
        "x must be float",
        "ok must be bool",
        "ids must be list[int]",
    ]


def test_describe():
    assert m.describe(GOOD) == "Dune (412 pages, 2 tags)"
    assert m.describe({"title": "A", "pages": 1, "tags": []}) == "A (1 pages, 0 tags)"
