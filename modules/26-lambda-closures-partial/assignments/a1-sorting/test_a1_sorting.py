import pytest

from practice import load

m = load(__file__)


def test_rank_students_by_score_then_name_ignoring_case():
    students = [
        {"name": "bo", "score": 80},
        {"name": "Al", "score": 80},
        {"name": "Cy", "score": 95},
        {"name": "dee", "score": 60},
    ]
    assert m.rank_students(students) == ["Cy", "Al", "bo", "dee"]


def test_rank_students_does_not_change_input():
    students = [{"name": "b", "score": 1}, {"name": "a", "score": 2}]
    snapshot = [dict(s) for s in students]
    assert m.rank_students(students) == ["a", "b"]
    assert students == snapshot


def test_rank_students_empty():
    assert m.rank_students([]) == []


def test_longest_words():
    words = ["pear", "fig", "banana", "kiwi", "apple", "plum"]
    assert m.longest_words(words, 3) == ["banana", "apple", "kiwi"]


def test_longest_words_n_too_big_or_zero():
    assert m.longest_words(["bb", "a", "cc"], 10) == ["bb", "cc", "a"]
    assert m.longest_words(["bb", "a"], 0) == []


ROWS = [
    {"city": "Oslo", "age": 40, "name": "a"},
    {"city": "Bern", "age": 31, "name": "b"},
    {"city": "Oslo", "age": 25, "name": "c"},
    {"city": "Bern", "age": 22, "name": "d"},
]


def test_sort_by_one_field():
    assert [r["name"] for r in m.sort_by_fields(ROWS, "age")] == ["d", "c", "b", "a"]


def test_sort_by_two_fields():
    assert [r["name"] for r in m.sort_by_fields(ROWS, "city", "age")] == ["d", "b", "c", "a"]


def test_sort_by_fields_reverse():
    assert [r["name"] for r in m.sort_by_fields(ROWS, "age", reverse=True)] == ["a", "b", "c", "d"]


def test_sort_by_no_fields_returns_copy():
    result = m.sort_by_fields(ROWS)
    assert result == ROWS
    assert result is not ROWS


def test_sort_by_fields_does_not_change_input():
    before = list(ROWS)
    result = m.sort_by_fields(ROWS, "age")
    assert [r["name"] for r in result] == ["d", "c", "b", "a"]
    assert ROWS == before


def test_cheapest_and_priciest():
    prices = {"tea": 2.5, "coffee": 3.0, "water": 1.0, "wine": 12.0}
    assert m.cheapest_and_priciest(prices) == ("water", "wine")


def test_cheapest_and_priciest_empty():
    with pytest.raises(ValueError):
        m.cheapest_and_priciest({})
