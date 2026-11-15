import inspect

import pytest

from practice import load

m = load(__file__)


def boom(n):
    return 1 / n


def outer(n):
    return boom(n)


def fails_with_key(data):
    return data["missing"]


def raised(func, *args):
    try:
        func(*args)
    except Exception as exc:
        return exc
    raise AssertionError("expected an exception")


def line_of(func, text):
    """Absolute line number of the first line in func's source that contains text."""
    lines, start = inspect.getsourcelines(func)
    for offset, line in enumerate(lines):
        if text in line:
            return start + offset
    raise AssertionError(text)


def test_last_frame_is_where_it_was_raised():
    exc = raised(outer, 0)
    name, lineno, code = m.last_frame(exc)
    assert name == "boom"
    assert lineno == line_of(boom, "1 / n")
    assert code == "return 1 / n"


def test_last_frame_for_a_different_error():
    name, lineno, code = m.last_frame(raised(fails_with_key, {}))
    assert (name, code) == ("fails_with_key", 'return data["missing"]')
    assert lineno == line_of(fails_with_key, "missing")


def test_last_frame_without_traceback():
    with pytest.raises(ValueError):
        m.last_frame(ValueError("never raised"))


def test_call_chain_lists_outermost_first():
    exc = raised(outer, 0)
    assert m.call_chain(exc) == ["raised", "outer", "boom"]


def test_call_chain_without_traceback():
    assert m.call_chain(RuntimeError("never raised")) == []


def test_run_safely_success_returns_none():
    assert m.run_safely(outer, 0) is not None  # an error is reported
    assert m.run_safely(boom, 4) is None


def test_run_safely_reports_the_error():
    info = m.run_safely(outer, 0)
    assert info == {
        "type": "ZeroDivisionError",
        "message": "division by zero",
        "function": "boom",
        "line": line_of(boom, "1 / n"),
        "code": "return 1 / n",
        "depth": 3,
    }


def test_run_safely_key_error():
    info = m.run_safely(fails_with_key, {"a": 1})
    assert info["type"] == "KeyError"
    assert info["message"] == "'missing'"
    assert info["function"] == "fails_with_key"
    assert info["depth"] == 2


def test_run_safely_does_not_catch_keyboard_interrupt():
    def interrupt():
        raise KeyboardInterrupt

    assert m.run_safely(boom, 0)["type"] == "ZeroDivisionError"  # normal errors are caught
    with pytest.raises(KeyboardInterrupt):
        m.run_safely(interrupt)
