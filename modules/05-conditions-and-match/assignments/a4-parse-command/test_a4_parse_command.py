import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("", ("noop",)),
        ("   ", ("noop",)),
        ("quit", ("quit",)),
        ("EXIT", ("quit",)),
        ("look", ("look",)),
        ("  GO   North ", ("move", "north")),
        ("go west", ("move", "west")),
        ("go up", ("unknown", "go up")),
        ("take lamp", ("take", "lamp")),
        ("Take Brass Lamp", ("take", "brass lamp")),
        ("take", ("unknown", "take")),
        ("dance wildly", ("unknown", "dance wildly")),
    ],
)
def test_parse(text, expected):
    assert m.parse(text) == expected
