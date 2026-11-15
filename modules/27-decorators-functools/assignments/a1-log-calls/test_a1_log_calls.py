import pytest

from practice import load

m = load(__file__)


def test_count_calls_counts():
    @m.count_calls
    def hello():
        return "hi"

    assert hello.calls == 0
    assert hello() == "hi"
    hello()
    assert hello.calls == 2


def test_count_calls_passes_arguments():
    @m.count_calls
    def add(a, b=1):
        return a + b

    assert add(2, b=5) == 7


def test_count_calls_keeps_metadata():
    @m.count_calls
    def documented():
        """Doc text."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Doc text."


def test_log_calls_success():
    messages = []

    @m.log_calls(messages.append)
    def add(a, b):
        return a + b

    assert add(1, 2) == 3
    assert messages == ["add(1, 2) -> 3"]


def test_log_calls_keyword_and_repr():
    messages = []

    @m.log_calls(messages.append)
    def greet(name, punctuation="!"):
        return "hi " + name + punctuation

    greet("Ada", punctuation="?")
    assert messages == ["greet('Ada', punctuation='?') -> 'hi Ada?'"]


def test_log_calls_error_is_logged_and_raised():
    messages = []

    @m.log_calls(messages.append)
    def boom(x):
        raise ValueError("bad")

    with pytest.raises(ValueError):
        boom(3)
    assert messages == ["boom(3) raised ValueError"]


def test_log_calls_keeps_metadata():
    @m.log_calls(lambda text: None)
    def documented():
        """Doc text."""

    assert documented.__name__ == "documented"
    assert documented.__doc__ == "Doc text."
