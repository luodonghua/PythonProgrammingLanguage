import httpx
import pytest

from practice import load

m = load(__file__)

BODY = (
    ": keep-alive\n"
    'data: {"text": "Hel"}\n'
    "\n"
    'data: {"text": "lo", "n": 2}\n'
    "event: ignored\n"
    'data: {"other": true}\n'
    "data: [DONE]\n"
    'data: {"text": "never seen"}\n'
)


def make_client(status=200, body=BODY):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=body)

    return httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="https://api.test")


async def test_iter_events_parses_data_lines_and_stops_at_done():
    async with make_client() as client:
        events = [event async for event in m.iter_events(client, "/s")]
    assert events == [{"text": "Hel"}, {"text": "lo", "n": 2}, {"other": True}]


async def test_iter_events_without_done_reads_to_the_end():
    async with make_client(body='data: {"a": 1}\ndata: {"a": 2}') as client:
        events = [event async for event in m.iter_events(client, "/s")]
    assert events == [{"a": 1}, {"a": 2}]


async def test_iter_events_is_an_async_generator_and_can_stop_early():
    async with make_client() as client:
        stream = m.iter_events(client, "/s")
        first = await anext(stream)
        await stream.aclose()
    assert first == {"text": "Hel"}


async def test_iter_events_raises_for_error_status():
    async with make_client(status=503, body="down") as client:
        with pytest.raises(httpx.HTTPStatusError):
            async for _ in m.iter_events(client, "/s"):
                pass


async def test_collect_text():
    async with make_client() as client:
        assert await m.collect_text(client, "/s") == "Hello"


async def test_collect_text_empty_stream():
    async with make_client(body="data: [DONE]\n") as client:
        assert await m.collect_text(client, "/s") == ""
