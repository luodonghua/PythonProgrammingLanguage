import pytest

from practice import load

m = load(__file__)


def make_flaky(failures, error=ConnectionError):
    state = {"calls": 0}

    def func(x=1):
        """Flaky doc."""
        state["calls"] += 1
        if state["calls"] <= failures:
            raise error("fail")
        return x * 10

    return func, state


def test_success_first_try_no_sleep():
    slept = []
    func, state = make_flaky(0)
    wrapped = m.retry(3, sleep=slept.append)(func)
    assert wrapped(2) == 20
    assert state["calls"] == 1
    assert slept == []


def test_retries_until_success():
    slept = []
    func, state = make_flaky(2)
    wrapped = m.retry(3, sleep=slept.append)(func)
    assert wrapped() == 10
    assert state["calls"] == 3
    assert slept == [1.0, 2.0]


def test_gives_up_and_reraises_last_error():
    slept = []
    func, state = make_flaky(10)
    wrapped = m.retry(3, sleep=slept.append)(func)
    with pytest.raises(ConnectionError):
        wrapped()
    assert state["calls"] == 3
    assert slept == [1.0, 2.0]


def test_custom_delay_and_backoff():
    slept = []
    func, _ = make_flaky(3)
    wrapped = m.retry(4, delay=0.5, backoff=3, sleep=slept.append)(func)
    assert wrapped() == 10
    assert slept == [0.5, 1.5, 4.5]


def test_other_exceptions_propagate_immediately():
    slept = []
    func, state = make_flaky(5, error=KeyError)
    wrapped = m.retry(3, exceptions=(ConnectionError,), sleep=slept.append)(func)
    with pytest.raises(KeyError):
        wrapped()
    assert state["calls"] == 1
    assert slept == []


def test_exceptions_tuple_accepts_several_types():
    slept = []
    func, _ = make_flaky(1, error=TimeoutError)
    wrapped = m.retry(2, exceptions=(ConnectionError, TimeoutError), sleep=slept.append)(func)
    assert wrapped() == 10


def test_keeps_metadata():
    func, _ = make_flaky(0)
    wrapped = m.retry(2, sleep=lambda s: None)(func)
    assert wrapped.__name__ == "func"
    assert wrapped.__doc__ == "Flaky doc."


def test_used_with_decorator_syntax():
    slept = []
    calls = []

    @m.retry(2, exceptions=(ValueError,), sleep=slept.append)
    def work():
        calls.append(1)
        if len(calls) == 1:
            raise ValueError
        return "done"

    assert work() == "done"
    assert slept == [1.0]
