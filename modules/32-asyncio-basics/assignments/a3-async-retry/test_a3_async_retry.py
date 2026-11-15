import pytest

from practice import load

m = load(__file__)


class FakeSleep:
    """Records the requested waits and returns at once."""

    def __init__(self):
        self.calls = []

    async def __call__(self, seconds):
        self.calls.append(seconds)


def flaky(failures, error=ConnectionError("down")):
    """Return an async function that fails `failures` times, then returns "ok"."""
    state = {"calls": 0}

    async def func():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise error
        return "ok"

    func.state = state
    return func


async def test_success_first_try_never_sleeps():
    sleep = FakeSleep()
    func = flaky(0)
    assert await m.retry_async(func, sleep=sleep) == "ok"
    assert func.state["calls"] == 1
    assert sleep.calls == []


async def test_retries_with_doubling_delay():
    sleep = FakeSleep()
    func = flaky(2)
    assert await m.retry_async(func, attempts=5, delay=0.5, sleep=sleep) == "ok"
    assert func.state["calls"] == 3
    assert sleep.calls == [0.5, 1.0]


async def test_last_exception_is_raised_after_all_attempts():
    sleep = FakeSleep()
    func = flaky(10, error=TimeoutError("slow"))
    with pytest.raises(TimeoutError, match="slow"):
        await m.retry_async(func, attempts=4, delay=1, sleep=sleep)
    assert func.state["calls"] == 4
    assert sleep.calls == [1, 2, 4]


async def test_other_exceptions_are_not_retried():
    sleep = FakeSleep()
    func = flaky(5, error=KeyError("bug"))
    with pytest.raises(KeyError):
        await m.retry_async(func, retry_on=(ConnectionError,), sleep=sleep)
    assert func.state["calls"] == 1
    assert sleep.calls == []


async def test_retry_on_a_specific_type():
    sleep = FakeSleep()
    func = flaky(1, error=ConnectionError("x"))
    assert await m.retry_async(func, retry_on=(ConnectionError, TimeoutError), sleep=sleep) == "ok"
    assert sleep.calls == [1.0]


async def test_single_attempt_means_no_retry():
    sleep = FakeSleep()
    func = flaky(1)
    with pytest.raises(ConnectionError):
        await m.retry_async(func, attempts=1, sleep=sleep)
    assert sleep.calls == []


@pytest.mark.parametrize("attempts", [0, -2])
async def test_bad_attempts(attempts):
    async def func():
        return 1

    with pytest.raises(ValueError, match="at least 1"):
        await m.retry_async(func, attempts=attempts)
