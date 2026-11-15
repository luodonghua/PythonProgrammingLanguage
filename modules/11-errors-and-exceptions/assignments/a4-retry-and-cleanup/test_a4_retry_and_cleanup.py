import pytest

from practice import load

m = load(__file__)


def flaky(failures, exc=ConnectionError, result="done"):
    """Return (function, calls). The function raises `failures` times, then works."""
    calls = []

    def func():
        calls.append(1)
        if len(calls) <= failures:
            raise exc("fail")
        return result

    return func, calls


def test_retry_first_try():
    func, calls = flaky(0)
    assert m.retry(func) == "done"
    assert len(calls) == 1


def test_retry_succeeds_after_failures():
    func, calls = flaky(2)
    assert m.retry(func, 3) == "done"
    assert len(calls) == 3


def test_retry_gives_up_and_raises_last_error():
    func, calls = flaky(10)
    with pytest.raises(ConnectionError):
        m.retry(func, 3)
    assert len(calls) == 3


def test_retry_only_catches_listed_exceptions():
    func, calls = flaky(5, exc=KeyError)
    with pytest.raises(KeyError):
        m.retry(func, 3, (ConnectionError,))
    assert len(calls) == 1


def test_retry_listed_exception_is_retried():
    func, calls = flaky(2, exc=KeyError)
    assert m.retry(func, 3, (KeyError,)) == "done"
    assert len(calls) == 3


def test_retry_needs_at_least_one_attempt():
    func, calls = flaky(0)
    with pytest.raises(ValueError):
        m.retry(func, 0)
    assert calls == []


def test_run_with_cleanup_success():
    log = []
    assert m.run_with_cleanup(lambda: 5, log) == 5
    assert log == ["cleanup"]


def test_run_with_cleanup_error_is_not_hidden():
    log = []
    with pytest.raises(ZeroDivisionError):
        m.run_with_cleanup(lambda: 1 / 0, log)
    assert log == ["cleanup"]


def test_run_with_cleanup_runs_action_once():
    log = []
    calls = []
    m.run_with_cleanup(lambda: calls.append(1), log)
    assert calls == [1]
    assert log == ["cleanup"]


def test_first_success():
    assert m.first_success([lambda: 1 / 0, lambda: "ok", lambda: "later"]) == "ok"
    assert m.first_success([lambda: 0]) == 0


def test_first_success_stops_after_a_success():
    calls = []

    def second():
        calls.append("second")
        return 2

    assert m.first_success([lambda: 1, second]) == 1
    assert calls == []


def test_first_success_all_fail_is_chained():
    with pytest.raises(RuntimeError, match="all failed") as info:
        m.first_success([lambda: 1 / 0, lambda: [][0]])
    assert isinstance(info.value.__cause__, IndexError)


def test_first_success_empty():
    with pytest.raises(RuntimeError, match="all failed"):
        m.first_success([])


def test_parse_or_none():
    assert m.parse_or_none("12", int) == 12
    assert m.parse_or_none("x", int) is None
    assert m.parse_or_none("2.5", float) == 2.5


def test_parse_or_none_lets_other_errors_through():
    assert m.parse_or_none("1", int) == 1
    with pytest.raises(TypeError):
        m.parse_or_none(None, int)
