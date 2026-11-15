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
    async with client.stream("GET", url) as response:
        response.raise_for_status()
        async for line in response.aiter_lines():
            if not line.startswith("data:"):
                continue
            payload = line.removeprefix("data:").strip()
            if payload == "[DONE]":
                return
            yield json.loads(payload)


async def collect_text(client: httpx.AsyncClient, url: str) -> str:
    """Join the ``"text"`` field of every event from ``iter_events`` into one string.

    Events without a ``"text"`` key are skipped.
    """
    parts = []
    async for event in iter_events(client, url):
        if "text" in event:
            parts.append(event["text"])
    return "".join(parts)


if __name__ == "__main__":
    body = 'data: {"text": "Hel"}\n\n: ping\ndata: {"text": "lo"}\ndata: [DONE]\n'

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=body)

    async def demo() -> None:
        transport = httpx.MockTransport(handler)
        async with httpx.AsyncClient(transport=transport, base_url="https://x.test") as c:
            print(await collect_text(c, "/stream"))

    asyncio.run(demo())
