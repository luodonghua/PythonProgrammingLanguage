import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("celsius", "expected"),
    [
        (-5, "freezing"),
        (0, "freezing"),
        (0.1, "cold"),
        (9.9, "cold"),
        (10, "mild"),
        (19.9, "mild"),
        (20, "warm"),
        (29.9, "warm"),
        (30, "hot"),
        (45, "hot"),
    ],
)
def test_classify(celsius, expected):
    assert m.classify(celsius) == expected
