import httpx
import pytest

from practice import load

m = load(__file__)


class FakeSleep:
    def __init__(self):
        self.delays = []

    async def __call__(self, seconds):
        self.delays.append(seconds)


def make_client(script):
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return script[len(calls) - 1]

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://api.test")
    return client, calls


@pytest.mark.parametrize(
    ("headers", "expected"),
    [
        ({"Retry-After": "3"}, 3.0),
        ({"Retry-After": "2.5"}, 2.5),
        ({}, 1.0),
        ({"Retry-After": "soon"}, 1.0),
        ({"Retry-After": "-4"}, 1.0),
        ({"Retry-After": "600"}, 30.0),
    ],
)
def test_retry_after_seconds(headers, expected):
    assert m.retry_after_seconds(httpx.Response(429, headers=headers)) == expected


def test_retry_after_custom_default_and_maximum():
    response = httpx.Response(429, headers={"Retry-After": "50"})
    assert m.retry_after_seconds(response, maximum=10) == 10
    assert m.retry_after_seconds(httpx.Response(429), default=7) == 7


async def test_waits_for_retry_after_then_succeeds():
    script = [
        httpx.Response(429, headers={"Retry-After": "2"}),
        httpx.Response(429, headers={"Retry-After": "4"}),
        httpx.Response(200, json={"ok": True}),
    ]
    client, calls = make_client(script)
    fake = FakeSleep()
    async with client:
        response = await m.get_with_rate_limit(client, "/x", sleep=fake)
    assert response.json() == {"ok": True}
    assert fake.delays == [2.0, 4.0]
    assert len(calls) == 3


async def test_no_sleep_when_not_limited():
    client, calls = make_client([httpx.Response(200, json=1)])
    fake = FakeSleep()
    async with client:
        await m.get_with_rate_limit(client, "/x", sleep=fake)
    assert fake.delays == []
    assert len(calls) == 1


async def test_raises_after_max_attempts_without_extra_sleep():
    script = [httpx.Response(429, headers={"Retry-After": "1"})] * 3
    client, calls = make_client(script)
    fake = FakeSleep()
    async with client:
        with pytest.raises(m.RateLimitError):
            await m.get_with_rate_limit(client, "/x", max_attempts=3, sleep=fake)
    assert len(calls) == 3
    assert len(fake.delays) == 2


async def test_other_errors_are_raised_not_retried():
    client, calls = make_client([httpx.Response(500), httpx.Response(200, json=1)])
    fake = FakeSleep()
    async with client:
        with pytest.raises(httpx.HTTPStatusError):
            await m.get_with_rate_limit(client, "/x", sleep=fake)
    assert len(calls) == 1
