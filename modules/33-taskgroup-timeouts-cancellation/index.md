---
layout: module
module: 33-taskgroup-timeouts-cancellation
kind: learn
title: TaskGroup, timeouts and cancellation
permalink: /modules/33-taskgroup-timeouts-cancellation/
---

<div class="box key" markdown="1">

## Key learning points

- `asyncio.TaskGroup` runs tasks as a unit. The `async with` block ends only when **every task has finished**. This is **structured concurrency**: no task outlives its block.
- If a task fails, the group **cancels the others** and raises an `ExceptionGroup` that holds every error.
- `except*` handles the errors inside an `ExceptionGroup` by type. A plain `except` does not match a group.
- `asyncio.timeout(seconds)` cancels the code in its block when time runs out, and the block raises `TimeoutError`.
- Cancellation arrives as `asyncio.CancelledError` at an `await`. Clean up in `finally` and let the error continue.
- `asyncio.Queue` with a fixed number of worker tasks gives you a worker pool.

</div>

## 1. TaskGroup

`gather` (topic 32) leaves tasks running when one of them fails. `TaskGroup` is stricter and safer.

```python
import asyncio

async def fetch(name):
    await asyncio.sleep(0)
    if name == "bad":
        raise ValueError("bad item")
    return name.upper()

async def main():
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(n)) for n in ["a", "b", "c"]]
    # Here every task is finished.
    print([t.result() for t in tasks])

asyncio.run(main())
```

```text
['A', 'B', 'C']
```

- `tg.create_task(coro)` starts a task that belongs to the group.
- Leaving the `async with` block waits for all tasks.
- Read results with `task.result()` after the block. Reading before is an error if the task is not done.

### When a task fails

```python
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch("a"))
            tg.create_task(fetch("bad"))
    except* ValueError as eg:
        print("caught", type(eg).__name__, eg.exceptions)

asyncio.run(main())
```

```text
caught ExceptionGroup (ValueError('bad item'),)
```

The group cancels every task that is still running. It then raises an **`ExceptionGroup`**, because more than one task could have failed. The group is also why no half-finished background task is left behind.

## 2. ExceptionGroup and except*

An `ExceptionGroup` is an exception that holds a list of other exceptions (`eg.exceptions`). `except*` picks out the members of a given type:

```python
async def boom(exc):
    raise exc

async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(boom(ValueError("v1")))
            tg.create_task(boom(TypeError("t1")))
            tg.create_task(boom(ValueError("v2")))
    except* ValueError as eg:
        print("values:", [str(e) for e in eg.exceptions])
    except* TypeError as eg:
        print("types:", [str(e) for e in eg.exceptions])

asyncio.run(main())
```

```text
values: ['v1', 'v2']
types: ['t1']
```

- More than one `except*` clause can run for the same group, each taking its own part.
- Members that no clause matches are raised again as a smaller group.
- A plain `except ValueError:` does **not** catch a group that contains a `ValueError`. The group itself is not a `ValueError`, so the clause does not match.
- `return`, `break` and `continue` are not allowed inside an `except*` block. Save values in variables and act after the `try`.

`except*` and `ExceptionGroup` came in Python 3.11, together with `TaskGroup`.

## 3. Timeouts

```python
async def main():
    try:
        async with asyncio.timeout(0.05):
            await asyncio.sleep(10)
    except TimeoutError:
        print("timed out")

asyncio.run(main())
```

```text
timed out
```

- `asyncio.timeout(seconds)` is an async context manager (3.11+). When time is up it cancels the current task, and the `async with` block raises `TimeoutError`.
- `asyncio.wait_for(awaitable, timeout=seconds)` does the same for a single awaitable and also raises `TimeoutError`.
- A timeout only works at an `await`. Code that never awaits cannot be interrupted.
- Use a short timeout in an example only when the job can never finish. Real timing makes tests flaky.

## 4. Cancellation

`task.cancel()` asks a task to stop. At its next `await`, the task receives `asyncio.CancelledError`.

```python
async def work():
    try:
        print("working")
        await asyncio.sleep(10)
    finally:
        print("cleanup")        # runs on success, error and cancel

async def main():
    t = asyncio.create_task(work())
    await asyncio.sleep(0)      # let it start
    t.cancel()
    try:
        await t
    except asyncio.CancelledError:
        print("task cancelled:", t.cancelled())

asyncio.run(main())
```

```text
working
cleanup
task cancelled: True
```

Rules for `CancelledError`:

1. Put cleanup (closing files, releasing locks, logging) in `finally`.
2. If you catch `CancelledError`, **re-raise it** after cleanup. Swallowing it breaks timeouts and TaskGroups, which rely on it.
3. `CancelledError` is not an `Exception` subclass (it derives from `BaseException`), so `except Exception:` does not catch it.

### shield

`asyncio.shield(task)` lets the caller be cancelled or time out without cancelling the inner task:

```python
async def save():
    await asyncio.sleep(0.05)
    return "saved"

async def main():
    t = asyncio.create_task(save())
    try:
        async with asyncio.timeout(0.01):
            await asyncio.shield(t)
    except TimeoutError:
        print("timed out, task done?", t.done())
    print(await t)

asyncio.run(main())
```

```text
timed out, task done? False
saved
```

Use `shield` rarely, for work that must finish, such as writing a result to a database.

## 5. Worker pools with Queue

An `asyncio.Queue` hands items to a fixed number of workers.

```python
async def main():
    queue = asyncio.Queue()
    results = []

    async def worker():
        while True:
            item = await queue.get()
            try:
                results.append(item * 2)
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as tg:
        workers = [tg.create_task(worker()) for _ in range(2)]
        for i in range(5):
            queue.put_nowait(i)
        await queue.join()          # wait until every item has task_done()
        for w in workers:
            w.cancel()              # workers loop forever, so stop them
    print(sorted(results))

asyncio.run(main())
```

```text
[0, 2, 4, 6, 8]
```

- `queue.get()` waits for an item. `queue.task_done()` says one item is finished.
- `queue.join()` waits until every `put` item has had a `task_done()`.
- The number of workers is the concurrency limit. Cancelling a child task does not make the TaskGroup fail.

<div class="box warn" markdown="1">

## Common mistakes

- **Catching `CancelledError` and not re-raising it.** The task seems to ignore the timeout or cancel request.
- **Using `except ValueError` around a TaskGroup.** The error arrives wrapped in an `ExceptionGroup`. Use `except*`.
- **Forgetting `task_done()`.** `queue.join()` then never returns. Call it in a `finally` block.
- **Reading `task.result()` inside the TaskGroup block.** The task may not be finished. Read results after the block.
- **Long blocking code under `asyncio.timeout`.** Without an `await` the timeout cannot fire.

</div>

## Try it yourself

1. Start three tasks in a TaskGroup where the second raises. Print which of the others were cancelled.
2. Write `fetch_or_default(coro_factory, seconds, default)` using `asyncio.timeout`.
3. Build a worker pool with 3 workers and 10 items. Record the largest number of workers busy at once.

<div class="box" markdown="1">

## Where this appears in AI agents

An agent often calls several tools in parallel. A `TaskGroup` keeps those calls together: if the user cancels the run, every call stops, and no call keeps running in the background. A timeout around each model or tool call stops one slow service from hanging the whole run. When some calls fail and others work, `except*` or a wrapper that returns the error lets the agent report partial results.

```python
async with asyncio.timeout(30):
    async with asyncio.TaskGroup() as tg:
        calls = [tg.create_task(run_tool(c)) for c in tool_calls]
```

</div>

## Where this comes from

Beyond the two reference books. See the Python docs: [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html) (TaskGroup, timeout, shield), [Queues](https://docs.python.org/3/library/asyncio-queue.html) and [Exception groups](https://docs.python.org/3/tutorial/errors.html#raising-and-handling-multiple-unrelated-exceptions). *Introducing Python*, chapter 21 gives the background on concurrency.

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="33-taskgroup-timeouts-cancellation:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/33-taskgroup-timeouts-cancellation/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/33-taskgroup-timeouts-cancellation/assignments/' | relative_url }}).
