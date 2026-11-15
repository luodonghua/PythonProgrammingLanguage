import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("items", "size", "expected"),
    [
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
        ([1, 2, 3], 3, [[1, 2, 3]]),
        ([1, 2, 3], 10, [[1, 2, 3]]),
        ([1, 2, 3], 1, [[1], [2], [3]]),
        ([], 4, []),
    ],
)
def test_chunk(items, size, expected):
    assert m.chunk(items, size) == expected


@pytest.mark.parametrize("size", [0, -1])
def test_chunk_bad_size(size):
    with pytest.raises(ValueError):
        m.chunk([1, 2], size)


def test_parse_records_valid_lines():
    result = m.parse_records(["apple, 3, 0.5", " pear,2,1.25 ", "fig,0,0"])
    assert result == [("apple", 3, 0.5), ("pear", 2, 1.25), ("fig", 0, 0.0)]
    assert all(isinstance(record, tuple) for record in result)
    assert isinstance(result[0][1], int)
    assert isinstance(result[0][2], float)


@pytest.mark.parametrize(
    "bad_line",
    ["", "   ", "bad line", "a,1", "a,1,2,3", ",1,2", "a,x,2", "a,1.5,2", "a,1,x", "a,-1,2", "a,1,-2"],
)
def test_parse_records_skips_bad_lines(bad_line):
    assert m.parse_records(["ok,1,1.0", bad_line, "ok2,2,2.0"]) == [("ok", 1, 1.0), ("ok2", 2, 2.0)]


def test_parse_records_all_bad():
    assert m.parse_records(["x", "", "y,z,w"]) == []


def test_summarize():
    assert m.summarize([("apple", 3, 0.5), ("pear", 2, 1.25)]) == (2, 5, 4.0)
    assert m.summarize([]) == (0, 0, 0.0)


def test_summarize_rounds():
    assert m.summarize([("a", 3, 0.1), ("b", 1, 0.2)]) == (2, 4, 0.5)


def test_most_valuable():
    assert m.most_valuable([("apple", 3, 0.5), ("pear", 2, 1.25)]) == "pear"
    assert m.most_valuable([("apple", 10, 1.0), ("pear", 5, 2.0)]) == "apple"
    assert m.most_valuable([("only", 1, 1.0)]) == "only"


def test_most_valuable_empty():
    assert m.most_valuable([]) is None
    assert m.most_valuable([("a", 1, 1.0)]) == "a"
