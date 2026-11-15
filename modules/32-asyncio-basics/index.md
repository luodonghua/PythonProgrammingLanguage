---
layout: module
module: 32-asyncio-basics
kind: learn
title: asyncio basics
permalink: /modules/32-asyncio-basics/
---

<div class="box key" markdown="1">

## Key learning points

- `async def` defines a **coroutine function**. Calling it returns a coroutine object and runs nothing yet. `await` runs it and gives you its result.
- `asyncio.run(main())` starts the **event loop**, a scheduler that runs many coroutines in one thread. A coroutine gives control back to the loop at each `await`.
- `asyncio.gather(...)` and `asyncio.create_task(...)` run work **concurrently**. The total time of waiting jobs is about the longest job, not the sum.
- asyncio helps with **waiting** (network, timers, files). It does not speed up CPU-heavy code.
- A blocking call such as `time.sleep` freezes every task. Use `await asyncio.sleep`, or `asyncio.to_thread` for blocking code.
- `asyncio.Semaphore` limits how many tasks work at the same moment.

</div>

## 1. Coroutines and await

```python
import asyncio

async def greet(name):
    await asyncio.sleep(0.1)     # pretend to wait for a server
    return f"hello {name}"

async def main():
    print(await greet("Ada"))

asyncio.run(main())
```

```text
hello Ada
```

- `async def greet` makes a coroutine function.
- `await asyncio.sleep(0.1)` pauses this coroutine for 0.1 s and lets other coroutines run.
- `await` is only allowed inside `async def`.
- `asyncio.run(main())` is the one entry point from normal code. Call it once, at the top of the program.

Calling a coroutine function without `await` does not run it:

```python
c = greet("x")
print(type(c))   # <class 'coroutine'>
```

Python warns `coroutine 'greet' was never awaited` when such an object is thrown away. That warning almost always means a missing `await`.

## 2. Running things at the same time

Three awaits one after another take the sum of their waits. `asyncio.gather` starts them together:

```python
import time

async def compare():
    t = time.perf_counter()
    await greet("a"); await greet("b"); await greet("c")
    print(f"sequential: {time.perf_counter() - t:.1f} s")

    t = time.perf_counter()
    results = await asyncio.gather(greet("a"), greet("b"), greet("c"))
    print(results)
    print(f"gather: {time.perf_counter() - t:.1f} s")

asyncio.run(compare())
```

```text
sequential: 0.3 s
['hello a', 'hello b', 'hello c']
gather: 0.1 s
```

`gather` returns the results **in the order you passed the coroutines**, not in the order they finish.

By default, if one coroutine raises, `gather` raises that exception to you and the other results are lost. With `return_exceptions=True` it returns the exception objects in the result list instead:

```python
async def ok():
    return 1

async def bad():
    raise ValueError("boom")

async def main():
    print(await asyncio.gather(ok(), bad(), return_exceptions=True))

asyncio.run(main())   # [1, ValueError('boom')]
```

## 3. Tasks

`asyncio.create_task(coro)` schedules a coroutine to run in the background and returns a `Task`. The task starts the next time the current coroutine awaits something.

```python
async def job(n):
    print("start", n)
    await asyncio.sleep(0)       # give control back to the loop
    print("end", n)
    return n * 10

async def main():
    t1 = asyncio.create_task(job(1))
    t2 = asyncio.create_task(job(2))
    print("created")
    print(await t1, await t2)

asyncio.run(main())
```

```text
created
start 1
start 2
end 1
end 2
10 20
```

Nothing in `job` ran until `main` reached its first `await`. `asyncio.sleep(0)` is the smallest possible pause: it only lets other tasks take a turn. Tests in this course use it instead of real waiting, so they are fast and do not depend on the clock.

Keep a reference to every task you create (in a variable or a list). The loop holds only a weak reference, and an unreferenced task can be garbage collected before it finishes.

## 4. Blocking code and threads

The loop runs one task at a time. If a task calls `time.sleep(5)` or does a long calculation without awaiting, **nothing else runs for 5 seconds**.

```python
# Bad inside a coroutine:
time.sleep(1)               # freezes all tasks
# Good:
await asyncio.sleep(1)      # other tasks run during the wait
```

Some code is blocking and has no async version, such as `Path.read_text` or a slow library call. Run it in a worker thread with `asyncio.to_thread`:

```python
def slow(x):
    time.sleep(0.1)
    return x * 2

async def main():
    print(await asyncio.to_thread(slow, 21))   # 42

asyncio.run(main())
```

The loop stays free while the thread works. Threads do not help CPU-heavy pure Python (see the GIL in topic 20). For that, use processes.

## 5. Limiting concurrency

Starting 1000 requests at once can overload a server. A `Semaphore` is a counter of free slots. `async with sem` takes a slot and gives it back when the block ends. At most N tasks are inside the block at the same time.

```python
async def main():
    sem = asyncio.Semaphore(2)
    active = peak = 0

    async def work():
        nonlocal active, peak
        async with sem:
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0)
            active -= 1

    await asyncio.gather(*(work() for _ in range(6)))
    print("peak", peak)   # peak 2

asyncio.run(main())
```

## 6. Other useful pieces

- `asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)` returns when the first task finishes (assignment 4).
- `asyncio.Event` lets one task wait until another calls `set()`.
- `asyncio.run` creates a new loop each time. Do not call it from inside a running coroutine.
- Python 3.14 added `python -m asyncio pstree`, a command-line tool that shows the call graph of the tasks in a running process. It is for debugging and not needed for this topic.

<div class="box warn" markdown="1">

## Common mistakes

- **Forgetting `await`.** `result = fetch()` gives you a coroutine object, not the result. Look for the "never awaited" warning.
- **Using `time.sleep` or a blocking library call in a coroutine.** It stops every task. Use `await asyncio.sleep` or `asyncio.to_thread`.
- **Awaiting in a loop and expecting concurrency.** `for x in xs: await f(x)` runs one at a time. Use `gather` or tasks.
- **Dropping the reference to a task.** Store the result of `create_task`.
- **Expecting a speed-up for CPU work.** One event loop uses one thread. Calculations still run one after another.

</div>

## Try it yourself

1. Write `async def fetch(n)` that sleeps 0.1 s and returns `n * n`. Time `await fetch(1); await fetch(2)` against `gather(fetch(1), fetch(2))`.
2. Run 10 jobs with a `Semaphore(3)` and print how many are active when each starts. The number should never go above 3.
3. Call `time.sleep(1)` inside one of two concurrent tasks and watch what happens to the other. Then replace it with `await asyncio.sleep(1)`.

<div class="box" markdown="1">

## Where this appears in AI agents

Calling a language model or a tool is a network request that takes seconds. An agent that asks three tools for data would wait three times as long if it did them one by one. With `gather` it waits as long as the slowest one. A `Semaphore` keeps the agent under a provider's rate limit, and `to_thread` lets it call a blocking library without freezing the rest of the program.

```python
answers = await asyncio.gather(*(call_tool(c) for c in tool_calls))
```

</div>

## Further reading

- [Coroutines and Tasks](https://docs.python.org/3/library/asyncio-task.html)
- [Synchronization primitives](https://docs.python.org/3/library/asyncio-sync.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="32-asyncio-basics:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/32-asyncio-basics/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/32-asyncio-basics/assignments/' | relative_url }}).
