from unittest.mock import AsyncMock

import pytest

from practice import load

m = load(__file__)


class RecordingSleep:
    def __init__(self):
        self.delays = []

    async def __call__(self, seconds):
        self.delays.append(seconds)


async def test_success_needs_one_call_and_no_sleep():
    client = AsyncMock()
    client.get.return_value = "body"
    sleep = RecordingSleep()
    fetcher = m.RetryingFetcher(client, sleep=sleep)
    assert await fetcher.fetch("/a") == "body"
    client.get.assert_awaited_once_with("/a")
    assert sleep.delays == []
    assert fetcher.attempts == 1


async def test_retries_then_succeeds_with_exponential_delays():
    client = AsyncMock()
    client.get.side_effect = [ConnectionError("1"), TimeoutError("2"), "body"]
    sleep = RecordingSleep()
    fetcher = m.RetryingFetcher(client, retries=2, delay=0.5, sleep=sleep)
    assert await fetcher.fetch("/a") == "body"
    assert client.get.await_count == 3
    assert sleep.delays == [0.5, 1.0]
    assert fetcher.attempts == 3


async def test_gives_up_after_retries_and_raises_last_error():
    client = AsyncMock()
    client.get.side_effect = [ConnectionError("first"), ConnectionError("second"), ConnectionError("third")]
    sleep = RecordingSleep()
    fetcher = m.RetryingFetcher(client, retries=2, delay=1, sleep=sleep)
    with pytest.raises(ConnectionError, match="third"):
        await fetcher.fetch("/a")
    assert client.get.await_count == 3
    assert sleep.delays == [1, 2]  # no sleep after the last failure


async def test_other_exceptions_are_not_retried():
    client = AsyncMock()
    client.get.side_effect = [ValueError("bad"), "never used"]
    sleep = RecordingSleep()
    fetcher = m.RetryingFetcher(client, sleep=sleep)
    with pytest.raises(ValueError):
        await fetcher.fetch("/a")
    assert client.get.await_count == 1
    assert sleep.delays == []


async def test_retries_zero():
    client = AsyncMock()
    client.get.side_effect = [ConnectionError("x"), "ok"]
    fetcher = m.RetryingFetcher(client, retries=0, sleep=RecordingSleep())
    with pytest.raises(ConnectionError):
        await fetcher.fetch("/a")
    assert client.get.await_count == 1


async def test_custom_retry_on():
    client = AsyncMock()
    client.get.side_effect = [KeyError("k"), "ok"]
    sleep = RecordingSleep()
    fetcher = m.RetryingFetcher(client, retry_on=(KeyError,), sleep=sleep)
    assert await fetcher.fetch("/a") == "ok"
    assert sleep.delays == [1.0]


async def test_attempts_add_up_over_several_fetches():
    client = AsyncMock()
    client.get.side_effect = [ConnectionError("x"), "one", "two"]
    fetcher = m.RetryingFetcher(client, sleep=RecordingSleep())
    await fetcher.fetch("/a")
    await fetcher.fetch("/b")
    assert fetcher.attempts == 3
    assert [call.args for call in client.get.await_args_list] == [("/a",), ("/a",), ("/b",)]
