import pytest

from practice import load

m = load(__file__)


@pytest.fixture(autouse=True)
def fresh_registry(monkeypatch):
    monkeypatch.setattr(m, "COMMANDS", {})


def test_plain_decorator_uses_function_name():
    @m.command
    def start():
        return "started"

    assert "start" in m.COMMANDS
    assert m.run("start") == "started"


def test_named_decorator():
    @m.command("stop")
    def halt():
        return "stopped"

    assert list(m.COMMANDS) == ["stop"]
    assert m.run("stop") == "stopped"


def test_decorator_returns_original_function():
    def add(a, b):
        return a + b

    assert m.command(add) is add
    assert m.command("plus")(add) is add


def test_arguments_are_passed_as_strings():
    @m.command
    def echo(*words):
        return "-".join(words)

    assert m.run("echo a b  c") == "a-b-c"


def test_blank_line():
    assert m.run("") == ""
    assert m.run("   ") == ""


def test_unknown_command():
    assert m.run("dance now") == "unknown command: dance"


def test_decorated_function_still_callable():
    @m.command
    def double(x):
        return x * 2

    assert double(4) == 8
