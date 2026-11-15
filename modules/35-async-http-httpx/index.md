---
layout: module
module: 35-async-http-httpx
kind: learn
title: Async HTTP with httpx
permalink: /modules/35-async-http-httpx/
---

<div class="box key" markdown="1">

## Key learning points

- `httpx.AsyncClient` sends many HTTP requests at once from async code. Create **one client** and reuse it, with `async with`.
- Set **timeouts** on purpose. Call `response.raise_for_status()` so that 4xx and 5xx answers become exceptions.
- **Retry only temporary failures** (network errors and 5xx), with a growing delay (exponential backoff). Pass `sleep` in as a parameter so tests do not wait.
- Limit concurrency with `asyncio.Semaphore`, and obey `429 Too Many Requests` and `Retry-After`.
- Read big or slow responses as a **stream** with `client.stream(...)` and `aiter_lines()`.
- Test with `httpx.MockTransport`. The code under test is the real code, but no packet leaves your computer.

</div>

Topic 23 showed HTTP with the standard library. The standard `urllib` blocks while it waits for the network. `httpx` (a third-party package, `uv add httpx`) has the same simple API in a blocking form (`httpx.Client`) and in an async form (`httpx.AsyncClient`). This page uses the async form together with `asyncio` from topics 32 to 34.

## 1. A client, a request, a response

A real client talks to a real server. To keep every example here runnable offline, we plug in a **mock transport**. The transport is the part of the client that actually sends the request. `httpx.MockTransport(handler)` calls your function `handler(request)` and uses the `httpx.Response` it returns.

```python
import asyncio
import httpx


def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/user":
        return httpx.Response(200, json={"name": "Ada", "id": 7})
    return httpx.Response(404, text="nope")


async def main():
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://api.test") as client:
        r = await client.get("/user", params={"verbose": "1"})
        print(r.status_code, r.json(), r.url)


asyncio.run(main())
```

```text
200 {'name': 'Ada', 'id': 7} https://api.test/user?verbose=1
```

- `base_url` is put in front of relative paths. `params=` builds and escapes the query string.
- `r.json()` decodes the body. `r.text` is the body as text. `r.headers` is a case-insensitive mapping.
- To talk to a real server, leave out `transport=` and use a real URL. Nothing else changes.

## 2. Client lifetime, timeouts and errors

A client keeps a **pool** of open connections, so later requests are faster. Create it once (for example at program start) and share it. Do not create a new client for every request.

```python
timeout = httpx.Timeout(10.0, connect=2.0)
print(timeout)
```

```text
Timeout(connect=2.0, read=10.0, write=10.0, pool=10.0)
```

The default timeout in httpx is 5 seconds for each phase. Without any timeout, a stalled server can block your task forever, so always know what yours is.

Errors fall into two families:

| Problem | Exception | Typical cause |
|---|---|---|
| The request did not complete | `httpx.TransportError` and its subclasses (`ConnectError`, `ReadTimeout`, ...) | Network down, server too slow |
| The server answered with an error status | `httpx.HTTPStatusError`, only after `response.raise_for_status()` | 404, 429, 503 |

httpx does **not** raise for a 404 by itself. Call `response.raise_for_status()` to turn 4xx and 5xx into `HTTPStatusError`. The failed response is available as `exc.response`.

## 3. Retries with exponential backoff

Some failures go away if you try again: a dropped connection, a 503 from an overloaded server. Waiting longer after each failure (1x, 2x, 4x ...) is called **exponential backoff**. It stops many clients from hammering a struggling server in step. A 404 will not fix itself, so do not retry it.

```python
async def get_json(client, url, retries=3, base_delay=0.5, sleep=asyncio.sleep):
    for attempt in range(retries + 1):
        if attempt:
            await sleep(base_delay * 2 ** (attempt - 1))
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except (httpx.TransportError, httpx.HTTPStatusError):
            if attempt == retries:
                raise
```

The `sleep` parameter has the real `asyncio.sleep` as its default. A test passes a fake that only records the delay:

```python
attempts = 0


def handler(request):
    global attempts
    attempts += 1
    if attempts < 3:
        return httpx.Response(503)
    return httpx.Response(200, json={"ok": True})


async def main():
    slept = []

    async def fake_sleep(seconds):
        slept.append(seconds)

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="https://api.test") as c:
        print(await get_json(c, "/job", sleep=fake_sleep))
    print("requests:", attempts, "sleeps:", slept)
```

```text
{'ok': True}
requests: 3 sleeps: [0.5, 1.0]
```

The test is instant and checks the exact delays. (This simple version retries 4xx too. The assignment asks you to do better.)

Real systems also add **jitter**, a small random amount, to each delay. Keep randomness out of the function you test, or inject it too.

## 4. Many requests, bounded concurrency

`asyncio.gather` runs many requests at once and returns the results in input order. Without a limit, 10,000 URLs mean 10,000 simultaneous requests. A `Semaphore(n)` lets only `n` tasks into a block at the same time.

```python
async def demo():
    sem = asyncio.Semaphore(2)
    running = 0
    peak = 0

    async def work(i):
        nonlocal running, peak
        async with sem:
            running += 1
            peak = max(peak, running)
            await asyncio.sleep(0)
            running -= 1
        return i * i

    print(await asyncio.gather(*(work(i) for i in range(6))), "peak", peak)
```

```text
[0, 1, 4, 9, 16, 25] peak 2
```

The same shape works for requests: put `await client.get(url)` inside `async with sem:`.

## 5. Rate limits: 429 and Retry-After

A server protects itself by answering `429 Too Many Requests`. Often it adds the header `Retry-After: 3`, meaning "wait 3 seconds". Read that header, wait, and try again. Cap the wait so that a wrong header cannot freeze your program, and fall back to a default if the header is missing or not a number.

## 6. Streaming responses

A normal `await client.get(...)` reads the whole body first. For long or incremental responses, stream it:

```python
async with client.stream("GET", "/events") as response:
    response.raise_for_status()
    async for line in response.aiter_lines():
        print(line)
```

Memory stays small, and you can react to the first line before the last one arrives. `aiter_bytes()` and `aiter_text()` work the same way. If you stop reading early, leaving the `async with` closes the connection.

An async generator wraps this nicely: `async def iter_events(...)` that `yield`s parsed items (topic 34). The caller then writes `async for event in iter_events(...)`.

## 7. Testing without a network

`MockTransport` has three advantages: tests are fast, they are deterministic, and you can simulate failures that are hard to cause for real.

```python
def handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/flaky":
        raise httpx.ConnectError("connection refused")   # simulate a network failure
    return httpx.Response(429, headers={"Retry-After": "2"})
```

The handler may also be `async def`, and it may record every request it receives. Assert on that record: how many requests were sent, which headers, which JSON body (`json.loads(request.content)`). Topic 37 builds on this.

<div class="box warn" markdown="1">

## Common mistakes

- **Creating a client per request.** Every new client opens new connections. Share one client with `async with`.
- **Forgetting `raise_for_status()`.** A 500 response is a normal return value in httpx. Your code then decodes an error page as if it were data.
- **Retrying everything.** Retrying a 404, 401 or 422 only repeats the mistake. Retry network errors, 429 and 5xx.
- **Real `sleep` in tests.** A retry test with a 30-second backoff would take 30 seconds. Inject `sleep`.
- **No limit on concurrency.** `gather` over thousands of URLs without a `Semaphore` can exhaust sockets or trigger rate limits.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

Calls to a model API are slow HTTP requests, so agents use an async client, a timeout, retries with backoff, and a concurrency limit. Providers answer `429` when you go too fast and `5xx` when they are overloaded, so the code in section 3 and 5 is what a real agent needs. Model replies are often streamed line by line, as in section 6. Tests replace the provider with a `MockTransport` or a scripted fake, so no money is spent and no key is needed.

```python
async with httpx.AsyncClient(timeout=httpx.Timeout(60.0, connect=5.0)) as client:
    ...  # one shared client for every model and tool call
```

</div>

## Try it yourself

1. Write a `MockTransport` handler that returns 503 twice and then 200. Use `get_json` from section 3 and print the list of delays it asked for.
2. Change the handler so that it returns `httpx.Response(200, text="a\nb\nc")`, then print each line with `client.stream` and `aiter_lines()`.
3. Fetch ten URLs with `gather` and a `Semaphore(3)`. Count how many handlers run at the same moment and check that the peak is 3.

## Further reading

- [httpx documentation](https://www.python-httpx.org/async/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="35-async-http-httpx:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/35-async-http-httpx/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/35-async-http-httpx/assignments/' | relative_url }}).
