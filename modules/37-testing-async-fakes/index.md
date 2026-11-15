---
layout: module
module: 37-testing-async-fakes
kind: learn
title: Testing async code with fakes
permalink: /modules/37-testing-async-fakes/
---

<div class="box key" markdown="1">

## Key learning points

- A good test is **fast, repeatable and offline**. Slow, random or paid dependencies (network, clock, a model API) are replaced by **test doubles**.
- The common doubles: **stub** (returns fixed answers), **fake** (a simple working replacement), **spy** (records how it was called) and **mock** (checks the calls itself).
- With `pytest-asyncio` in **auto mode** you write `async def test_...` and `async` fixtures with no decorator.
- `unittest.mock.AsyncMock` is a mock whose calls can be awaited. It records `await_count` and the arguments.
- **Pass dependencies in** (client, `sleep`, clock) so tests can substitute them. Use `monkeypatch` for what you cannot pass in, such as environment variables.
- Test timeouts and cancellation with an `asyncio.Event` that is never set, not with long sleeps.

</div>

Topic 16 introduced pytest. Async code adds two problems: tests must run inside an event loop, and async code loves to wait (network, `sleep`, queues). A test that really waits is slow, and a test that depends on timing breaks on a busy computer. This page shows how to remove both problems.

## 1. Test doubles

| Double | What it does | Example |
|---|---|---|
| Stub | Returns a fixed answer | A client that always returns `{"ok": True}` |
| Fake | A small, working replacement | A `FakeClock` that moves time without waiting |
| Spy | A stub or fake that also records calls | A client that stores every URL it received |
| Mock | Verifies calls for you | `AsyncMock` with `assert_awaited_once_with` |

The names overlap in everyday speech. What matters is the idea: **the code under test is real, and its slow neighbours are fake.**

## 2. pytest-asyncio and auto mode

The package `pytest-asyncio` runs coroutine tests inside an event loop. In this repository `pyproject.toml` sets:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
```

In **auto mode** every `async def test_...` is run as a coroutine, and `async` fixtures work with the plain `@pytest.fixture` decorator. (In the default *strict* mode you must add `@pytest.mark.asyncio` to each test.) `function` scope means each test gets a fresh event loop, so tests cannot leak tasks into each other.

```python
@pytest.fixture
async def client():
    c = AsyncMock()
    c.get.side_effect = [ConnectionError("down"), ConnectionError("down"), "body"]
    yield c          # code after the yield is the cleanup; there is none here


async def test_retry(client):
    ...
```

## 3. AsyncMock as a spy and a stub

`AsyncMock()` creates an object whose attributes are async mocks too. Calling one returns a coroutine, and awaiting it gives the configured result.

```python
from unittest.mock import AsyncMock

m = AsyncMock(return_value=5)
coro = m()
print(type(coro).__name__)
print(await coro)
```

```text
coroutine
5
```

(Run this inside an `async def`, or paste it in the `python -m asyncio` console.)

- `return_value=...` gives one answer for every call.
- `side_effect=[a, b, c]` gives the items in order. An item that is an exception **instance** is raised, so `[ConnectionError("down"), "body"]` means "fail once, then work". When the list is empty the mock raises `StopAsyncIteration`, a hint that the code made more calls than you planned.
- After the call: `m.await_count`, `m.await_args_list`, and `m.assert_awaited_once_with("/a")` check what happened.
- `MagicMock` is the non-async version. `MagicMock().get("/a")` returns a plain value that you cannot `await`. Use `AsyncMock` for `async def` methods.

Mocks are quick to set up, but a test full of `assert_called_with` checks how the code works inside. A small hand-written **fake** (like the `FakeClient` in the assignments) often gives clearer tests, because it behaves like the real thing and you assert on **results**.

## 4. Dependency injection: fake `sleep` and clock

Code that sleeps or reads the time should receive them as arguments.

```python
async def fetch_with_retry(client, url, sleep):
    for n in range(3):
        try:
            return await client.get(url)
        except ConnectionError:
            if n == 2:
                raise
            await sleep(2 ** n)
```

```python
class FakeClock:
    def __init__(self):
        self.sleeps = []

    async def sleep(self, seconds):
        self.sleeps.append(seconds)


async def test_retry(client):          # client is the fixture above
    clock = FakeClock()
    assert await fetch_with_retry(client, "/a", clock.sleep) == "body"
    assert clock.sleeps == [1, 2]
    assert client.get.await_count == 3
    client.get.assert_awaited_with("/a")
```

This test passes in a few milliseconds. The real `asyncio.sleep` would take 3 seconds, and a longer backoff would take longer. A good `FakeClock.sleep` also does `await asyncio.sleep(0)`, which lets other tasks run, as a real sleep would.

A default value such as `sleep=asyncio.sleep` is read **once**, when the function is defined. Patching `asyncio.sleep` later does not change it. This is another reason to pass the function explicitly.

## 5. monkeypatch for the rest

Sometimes you cannot pass a dependency in: an environment variable, a module-level constant, a function imported from elsewhere. pytest's `monkeypatch` fixture changes it for one test and restores it afterwards.

```python
def test_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "fake")
    assert os.environ["API_KEY"] == "fake"
    monkeypatch.delenv("API_KEY")
    assert "API_KEY" not in os.environ
```

`monkeypatch.setattr(module, "name", value)` replaces an attribute. Patch the name **where it is looked up**: if `app.py` does `from time import monotonic`, patch `app.monotonic`, not `time.monotonic`.

## 6. Timeouts and cancellation without waiting

To test "gives up after the time limit", the code needs something that never finishes. An `asyncio.Event` that nobody sets is perfect:

```python
async def test_timeout_without_waiting():
    never = asyncio.Event()
    with pytest.raises(TimeoutError):
        async with asyncio.timeout(0.01):
            await never.wait()
```

The result does not depend on timing: the work can never finish, so only the time limit can end it. Keep the limit small (a hundredth of a second) so the test is quick. The same trick tests cancellation. Start the task, let it begin with `await asyncio.sleep(0)`, call `task.cancel()`, and check that its `finally` block ran.

To test concurrency, use events instead of sleeps. Task A waits for an event that task B sets and the other way round. If the code runs them one after the other, the test deadlocks (put an `asyncio.timeout(1)` around it so it fails instead of hanging). If it runs them together, the test passes.

<div class="box warn" markdown="1">

## Common mistakes

- **`MagicMock` for an async function.** The call returns a mock, not a coroutine, so `await` fails with a `TypeError`. Use `AsyncMock`.
- **Asserting on timing.** `assert elapsed < 0.1` fails on a slow computer. Assert on recorded calls and results.
- **Forgetting `await` on a call to an async function.** The coroutine never runs, and Python warns `coroutine ... was never awaited`. The test may still pass by accident, so treat that warning as an error.
- **Patching the wrong name.** `monkeypatch.setattr("time.sleep", ...)` has no effect on code that already did `from time import sleep`.
- **Testing the mock.** If the test only checks that the mock returned what you told it to return, no real code is tested.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

Real model calls cost money, take seconds and return different text each time. Agent tests therefore use a **scripted fake model**: a class with the same `complete(messages)` method that returns prepared replies in order, including a reply that asks for a tool and a reply that raises a timeout. The agent loop runs for real, and the test checks the final answer and the calls the fake recorded. Topics 38 and 39 are built this way.

```python
model = FakeModel([tool_call_reply("add", {"a": 1, "b": 2}), text_reply("The sum is 3")])
```

</div>

## Try it yourself

1. Write a `FakeClient` with an `async def get(self, url)` method that returns values from a list and records the URLs. Test a function that calls it twice.
2. Replace the `FakeClient` with `AsyncMock(side_effect=[...])` and write the same test. Which one reads better to you?
3. Write a test that proves a function cancels its work on timeout: the work sets a flag in `finally`, and the test checks the flag.

## Further reading

- [`unittest.mock`](https://docs.python.org/3/library/unittest.mock.html)
- [`asyncio` testing and timeouts](https://docs.python.org/3/library/asyncio-task.html#timeouts)
- [pytest monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="37-testing-async-fakes:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/37-testing-async-fakes/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/37-testing-async-fakes/assignments/' | relative_url }}).
