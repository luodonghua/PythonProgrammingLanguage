---
layout: module
module: 20-concurrency
kind: learn
title: "Concurrency: threads and processes"
permalink: /modules/20-concurrency/
---

<div class="box key" markdown="1">

## Key learning points

- **I/O-bound** work waits for disks, networks or databases. **CPU-bound** work keeps the processor busy. The kind of work decides which tool helps.
- **Threads** share memory and suit I/O-bound work. **Processes** have separate memory and suit CPU-bound work. **asyncio** runs many waiting tasks on one thread.
- In the standard (GIL) build of CPython, only one thread runs Python code at a time, so threads do not speed up CPU-bound code. A free-threaded build removes that limit.
- Threads that change shared data need a `threading.Lock`. Without it you get **race conditions**.
- `queue.Queue` passes work between threads safely.
- `concurrent.futures` (`ThreadPoolExecutor`, `ProcessPoolExecutor`) is the simplest way to run many jobs: `map` keeps the input order, `as_completed` gives results as they finish.

</div>

## 1. Which kind of work do you have?

| Work | Example | Good tool |
|---|---|---|
| I/O-bound | download 50 pages, read many files | threads, or asyncio |
| CPU-bound | resize images, compute primes | processes |

Concurrency means several jobs are in progress at the same time. Parallelism means they run at the same instant on several CPU cores. Threads in the standard build give concurrency for I/O. Processes give true parallelism.

## 2. The GIL and the free-threaded build

The **Global Interpreter Lock** (GIL) is a lock inside the standard CPython interpreter. It lets one thread run Python bytecode at a time. A thread that waits for I/O releases it, so threads still help with I/O. Two threads doing pure calculation take turns, so they gain nothing.

Python 3.13 added an optional *free-threaded* build, which runs without the GIL. In Python 3.14 this build is officially supported (PEP 779). It is a separate build of the interpreter and not the default, and single-threaded code runs a little slower in it (roughly 5-10% in 3.14, per the Python 3.14 release notes). Many extension packages still need updates for it. This course assumes the standard build. Your code should be correct either way, so protect shared data with locks.

In Python 3.13 and later, `sys._is_gil_enabled()` tells you which mode is running.

## 3. Threads

```python
import threading

def work(name, results):
    results.append(f"hello from {name}")

results = []
t = threading.Thread(target=work, args=("worker", results))
t.start()      # begin running
t.join()       # wait until it finishes
print(results)
```

```text
['hello from worker']
```

Always `join()` threads you need to wait for. A thread that raises an exception prints a traceback but does not stop the main thread.

### Race conditions and Lock

`counter += 1` is really three steps: read, add, write. Two threads can read the same old value, and one update is lost. The result then changes from run to run. A lock lets one thread at a time into a section:

```python
counter = 0
lock = threading.Lock()

def add(n):
    global counter
    for _ in range(n):
        with lock:
            counter += 1

threads = [threading.Thread(target=add, args=(10_000,)) for _ in range(4)]
for th in threads:
    th.start()
for th in threads:
    th.join()
print(counter)
```

```text
40000
```

Use `with lock:` so the lock is always released. Keep the locked section short. Taking two locks in different orders in different threads can cause a **deadlock**, where both wait forever.

## 4. queue.Queue

A `Queue` is a thread-safe line of items. It needs no extra lock. A common pattern is one producer and one consumer, with `None` as a "stop" signal:

```python
import queue

q = queue.Queue()

def producer():
    for i in range(3):
        q.put(i)
    q.put(None)

def consumer(out):
    while (item := q.get()) is not None:
        out.append(item * 10)

out = []
p = threading.Thread(target=producer)
c = threading.Thread(target=consumer, args=(out,))
p.start(); c.start()
p.join(); c.join()
print(out)
```

```text
[0, 10, 20]
```

`q.get()` waits until an item is available. `Queue(maxsize=n)` makes `put` wait when the queue is full, which limits memory use.

## 5. concurrent.futures

An *executor* manages a pool of workers. You submit jobs and get results back.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def square(x):
    return x * x

with ThreadPoolExecutor(max_workers=4) as pool:
    print(list(pool.map(square, range(6))))

    futures = {pool.submit(square, n): n for n in (1, 2, 3)}
    results = {futures[f]: f.result() for f in as_completed(futures)}
    print(dict(sorted(results.items())))
```

```text
[0, 1, 4, 9, 16, 25]
{1: 1, 2: 4, 3: 9}
```

- `pool.map(fn, items)` returns results **in input order**.
- `pool.submit(fn, arg)` returns a `Future`. `future.result()` waits for the value.
- `as_completed(futures)` yields futures in the order they finish, which can differ from the order you submitted them.
- An exception inside a job is stored in the future and raised again by `result()`:

```python
with ThreadPoolExecutor() as pool:
    future = pool.submit(int, "x")
    try:
        future.result()
    except ValueError as exc:
        print("error:", exc)
```

```text
error: invalid literal for int() with base 10: 'x'
```

### Processes for CPU-bound work

`ProcessPoolExecutor` has the same interface but runs jobs in separate processes, each with its own interpreter and GIL. Arguments and results are copied between processes (pickled), so they must be picklable. Functions must be defined at module top level, and the starting code must sit under a main guard:

```python
from concurrent.futures import ProcessPoolExecutor

def square(x):
    return x * x

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as pool:
        print(list(pool.map(square, range(5))))
```

```text
[0, 1, 4, 9, 16]
```

Without the `if __name__ == "__main__":` guard, a new process may import your file and start more processes. Starting a process costs time, so use it only for jobs that take noticeably long.

## 6. A first look at asyncio

`asyncio` runs many tasks on one thread. A task gives control back at each `await`, so while one waits, another runs.

```python
import asyncio

async def job(n):
    await asyncio.sleep(0)     # a pause point where other tasks can run
    return n * 2

async def main():
    return await asyncio.gather(job(1), job(2), job(3))

print(asyncio.run(main()))
```

```text
[2, 4, 6]
```

`asyncio.gather` runs the coroutines together and returns their results in the order you passed them. Topic 32 covers asyncio in full.

<div class="box warn" markdown="1">

## Common mistakes

- **Using threads to speed up pure calculation** in the standard build. Use processes.
- **Changing shared data without a lock.** Bugs of this kind are rare and hard to reproduce.
- **Forgetting `join()`** or leaving the `with` block too early, then reading results before the work is done.
- **Missing `if __name__ == "__main__":`** around process-pool code. It can start processes recursively on Windows and macOS.
- **Sending unpicklable things to a process**, such as a lambda or an open file.
- **Testing with `time.sleep` and timing.** Tests become slow and flaky. Test the results, not the speed.

</div>

## Try it yourself

1. Write a function that returns the number of characters in a text. Use `ThreadPoolExecutor.map` to run it on five short strings and print the results.
2. Remove the lock from the counter example and run it with more threads and larger counts. Does the total change between runs on your Python version?
3. Write a consumer thread that reads numbers from a `Queue` and prints their running total. Stop it with `None`.

## Further reading

- [threading](https://docs.python.org/3/library/threading.html)
- [queue](https://docs.python.org/3/library/queue.html)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [free-threading HOWTO](https://docs.python.org/3/howto/free-threading-python.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="20-concurrency:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/20-concurrency/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/20-concurrency/assignments/' | relative_url }}).
