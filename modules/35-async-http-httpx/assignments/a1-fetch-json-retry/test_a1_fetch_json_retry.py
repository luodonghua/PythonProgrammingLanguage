import httpx
import pytest

from practice import load

m = load(__file__)


def make_client(script):
    """Client whose responses come from ``script`` (a list of Response or Exception)."""
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        item = script[len(calls) - 1]
        if isinstance(item, Exception):
            raise item
        return item

    client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler), base_url="https://api.test"
    )
    return client, calls


class FakeSleep:
    def __init__(self):
        self.delays = []

    async def __call__(self, seconds):
        self.delays.append(seconds)


async def test_success_first_try_does_not_sleep():
    client, calls = make_client([httpx.Response(200, json={"ok": True})])
    fake = FakeSleep()
    async with client:
        assert await m.fetch_json(client, "/a", sleep=fake) == {"ok": True}
    assert calls == ["/a"]
    assert fake.delays == []


async def test_retries_server_errors_with_backoff():
    script = [httpx.Response(503), httpx.Response(500), httpx.Response(200, json=[1, 2])]
    client, calls = make_client(script)
    fake = FakeSleep()
    async with client:
        result = await m.fetch_json(client, "/a", base_delay=0.5, sleep=fake)
    assert result == [1, 2]
    assert len(calls) == 3
    assert fake.delays == [0.5, 1.0]


async def test_retries_transport_errors():
    script = [httpx.ConnectError("boom"), httpx.ReadTimeout("slow"), httpx.Response(200, json="hi")]
    client, calls = make_client(script)
    fake = FakeSleep()
    async with client:
        assert await m.fetch_json(client, "/a", sleep=fake) == "hi"
    assert len(calls) == 3


async def test_client_error_is_not_retried():
    client, calls = make_client([httpx.Response(404), httpx.Response(200, json={})])
    fake = FakeSleep()
    async with client:
        with pytest.raises(httpx.HTTPStatusError) as info:
            await m.fetch_json(client, "/a", sleep=fake)
    assert info.value.response.status_code == 404
    assert len(calls) == 1
    assert fake.delays == []


async def test_gives_up_and_raises_last_error():
    script = [httpx.Response(500), httpx.Response(502), httpx.Response(503)]
    client, calls = make_client(script)
    fake = FakeSleep()
    async with client:
        with pytest.raises(httpx.HTTPStatusError) as info:
            await m.fetch_json(client, "/a", retries=2, base_delay=1, sleep=fake)
    assert info.value.response.status_code == 503
    assert len(calls) == 3
    assert fake.delays == [1, 2]


async def test_retries_zero_means_single_attempt():
    client, calls = make_client([httpx.ConnectError("boom"), httpx.Response(200, json=1)])
    async with client:
        with pytest.raises(httpx.ConnectError):
            await m.fetch_json(client, "/a", retries=0, sleep=FakeSleep())
    assert len(calls) == 1
