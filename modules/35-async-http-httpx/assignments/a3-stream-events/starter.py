"""Assignment 3: read a streamed response line by line.

Some servers send a long response in pieces (for example, a text that grows
token by token). The format used here is a simplified "server-sent events"
stream. Each event is one line:

    : comment lines start with a colon and are ignored
    data: {"text": "Hel"}
    data: {"text": "lo"}
    data: [DONE]

Blank lines separate events and are ignored.
"""

import asyncio
import json
from collections.abc import AsyncIterator

import httpx


async def iter_events(client: httpx.AsyncClient, url: str) -> AsyncIterator[dict]:
    """Yield one dict per ``data:`` line of the streamed response at ``url``.

    * Open the response with ``client.stream("GET", url)`` and read it with
      ``response.aiter_lines()``, so the body is never held in memory in full.
    * Call ``response.raise_for_status()`` first: a 4xx/5xx status raises
      ``httpx.HTTPStatusError`` when the generator is first iterated.
    * Skip blank lines and lines that start with ``:``.
    * For a line ``data: <payload>``: stop (return) when the payload is
      ``[DONE]``, otherwise yield ``json.loads(payload)``. Ignore any line after
      ``[DONE]``.
    * Lines that do not start with ``data:`` are ignored.
    """
    # TODO: use "async with client.stream(...)" and "async for line in ...".
    # The "yield" keyword below makes this function an async generator.
    return
    yield  # noqa: unreachable, keep so the stub is an async generator


async def collect_text(client: httpx.AsyncClient, url: str) -> str:
    """Join the ``"text"`` field of every event from ``iter_events`` into one string.

    Events without a ``"text"`` key are skipped.
    """
    # TODO: use "async for" over iter_events.
    ...


if __name__ == "__main__":
    body = 'data: {"text": "Hel"}\n\n: ping\ndata: {"text": "lo"}\ndata: [DONE]\n'

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=body)

    async def demo() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x.test") as c:
            print(await collect_text(c, "/stream"))

    asyncio.run(demo())
