import asyncio

import httpx

from practice import load

m = load(__file__)


def make_client(handler):
    return httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://api.test")


async def test_results_keep_input_order():
    async def handler(request: httpx.Request) -> httpx.Response:
        # Make earlier URLs finish later, so a wrong order would show up.
        delay = {"/a": 5, "/b": 3, "/c": 0}[request.url.path]
        for _ in range(delay):
            await asyncio.sleep(0)
        return httpx.Response(200, json=request.url.path)

    async with make_client(handler) as client:
        assert await m.fetch_all(client, ["/a", "/b", "/c"], limit=3) == ["/a", "/b", "/c"]


async def test_limit_is_respected_and_used():
    state = {"active": 0, "peak": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        for _ in range(5):
            await asyncio.sleep(0)
        state["active"] -= 1
        return httpx.Response(200, json=1)

    async with make_client(handler) as client:
        result = await m.fetch_all(client, [f"/{i}" for i in range(8)], limit=3)
    assert result == [1] * 8
    assert state["peak"] == 3


async def test_limit_one_runs_sequentially():
    state = {"active": 0, "peak": 0}

    async def handler(request: httpx.Request) -> httpx.Response:
        state["active"] += 1
        state["peak"] = max(state["peak"], state["active"])
        await asyncio.sleep(0)
        state["active"] -= 1
        return httpx.Response(200, json=1)

    async with make_client(handler) as client:
        await m.fetch_all(client, ["/a", "/b", "/c"], limit=1)
    assert state["peak"] == 1


async def test_failures_become_none():
    def handler(request: httpx.Request) -> httpx.Response:
        match request.url.path:
            case "/ok":
                return httpx.Response(200, json={"v": 1})
            case "/missing":
                return httpx.Response(404)
            case "/down":
                raise httpx.ConnectError("down")
            case _:
                return httpx.Response(500)

    async with make_client(handler) as client:
        result = await m.fetch_all(client, ["/ok", "/missing", "/down", "/boom", "/ok"])
    assert result == [{"v": 1}, None, None, None, {"v": 1}]


async def test_empty_list():
    async with make_client(lambda request: httpx.Response(200, json=1)) as client:
        assert await m.fetch_all(client, []) == []
