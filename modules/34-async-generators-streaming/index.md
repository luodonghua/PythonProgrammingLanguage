---
layout: module
module: 34-async-generators-streaming
kind: learn
title: Async generators and streaming
permalink: /modules/34-async-generators-streaming/
---

<div class="box key" markdown="1">

## Key learning points

- An **async generator** is an `async def` function with `yield`. You read it with `async for`. It can `await` between items.
- `async for` and **async comprehensions** (`[x async for x in stream]`) work on any async iterator.
- Streaming means you use each piece when it **arrives**, instead of waiting for the whole result.
- Close a generator that you stop reading early: `await gen.aclose()` or `contextlib.aclosing`. Otherwise its `finally` block runs late.
- `async with` runs `await` code on entry and exit. `@asynccontextmanager` builds one from a generator.
- A bounded `asyncio.Queue` gives **backpressure**: a fast producer waits when a slow consumer falls behind.

</div>

## 1. Your first async generator

```python
import asyncio

async def chunks(text, size):
    for start in range(0, len(text), size):
        await asyncio.sleep(0)             # pretend each piece takes time
        yield text[start:start + size]

async def main():
    async for piece in chunks("streaming!", 4):
        print(repr(piece))

asyncio.run(main())
```

```text
'stre'
'amin'
'g!'
```

- A function with both `async def` and `yield` is an **async generator function**. Calling it does not run the body. It returns an async generator object.
- `async for` can only be used inside `async def`. It awaits the next item each time.
- Inside an async generator you can `await`. In a normal generator (topic 28) you cannot.

An **async comprehension** builds a list from a stream:

```python
async def main():
    print([p async for p in chunks("abcdef", 3)])

asyncio.run(main())   # ['abc', 'def']
```

You can also filter: `[x * x async for x in numbers() if x % 2 == 0]`.

To take one item by hand, use `await anext(gen)`. When the generator is finished, `anext` raises `StopAsyncIteration`, the async version of `StopIteration`.

A class can be an async iterator too. It needs `__aiter__` (return `self`) and `async def __anext__`, which raises `StopAsyncIteration` at the end. Most of the time a generator function is shorter.

## 2. Closing generators

If you stop reading a generator early, its `finally` block does not run at once.

```python
async def gen():
    try:
        for i in range(10):
            yield i
    finally:
        print("gen cleanup")

async def main():
    async for i in gen():
        if i == 1:
            break
    print("after break")

asyncio.run(main())
```

```text
after break
gen cleanup
```

The cleanup ran later, when `asyncio.run` shut down. That can be too late if the generator holds a file, a connection or a lock. Close it yourself:

```python
from contextlib import aclosing

async def main():
    async with aclosing(gen()) as g:
        async for i in g:
            if i == 1:
                break
    print("after aclosing")

asyncio.run(main())
```

```text
gen cleanup
after aclosing
```

`await g.aclose()` does the same by hand. It raises `GeneratorExit` inside the generator at its `yield`, so the `finally` block runs.

## 3. async with and asynccontextmanager

`async with` calls `await __aenter__()` on entry and `await __aexit__()` on exit. Use it for resources that need `await` to open or close, such as a network connection. `@asynccontextmanager` builds one from a generator with a single `yield`:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def session(name):
    print("open", name)
    try:
        yield name
    finally:
        print("close", name)

async def main():
    async with session("db") as s:
        print("using", s)

asyncio.run(main())
```

```text
open db
using db
close db
```

## 4. Streaming with a Queue and backpressure

A producer and a consumer can run as separate tasks, joined by an `asyncio.Queue`. With `maxsize=1`, `await queue.put(...)` waits while the queue is full. A slow consumer therefore slows the producer, and memory use stays small.

```python
async def producer(q):
    for i in range(3):
        await q.put(i)
        print("put", i)
    await q.put(None)            # marker: the stream is over

async def consumer(q):
    while (item := await q.get()) is not None:
        print("got", item)
        await asyncio.sleep(0)

async def main():
    q = asyncio.Queue(maxsize=1)
    await asyncio.gather(producer(q), consumer(q))

asyncio.run(main())
```

```text
put 0
got 0
put 1
got 1
put 2
got 2
```

The consumer sets the pace. Without `maxsize`, the queue grows without limit when the producer is faster.

## 5. Incremental text

Network data arrives in arbitrary chunks. A chunk can end in the middle of a line. To stream lines, keep a buffer: add each chunk, then yield every complete line and keep the rest.

```python
async def lines(chunks):
    buffer = ""
    async for chunk in chunks:
        buffer += chunk
        while "\n" in buffer:
            line, buffer = buffer.split("\n", 1)
            yield line
    if buffer:
        yield buffer       # the last line had no newline
```

You implement and test this in the assignments. It is the core of reading a server's streamed response line by line.

## 6. Merging streams

To read two streams at once, run one task per stream. Each puts its items into one shared queue, and one generator reads the queue. Wait for the tasks in a `finally` block so none is left running. Assignment 4 builds this, plus a per-item timeout with `asyncio.timeout`.

<div class="box warn" markdown="1">

## Common mistakes

- **Using `for` instead of `async for`.** A plain `for` over an async generator raises `TypeError`.
- **Expecting `return value` in an async generator.** A bare `return` ends it. Returning a value is a `SyntaxError`.
- **Breaking out of `async for` and relying on `finally`.** Close with `aclose()` or `aclosing`.
- **Collecting the whole stream into a list first.** That removes the benefit of streaming. Process each item as it comes.
- **An unbounded queue between a fast producer and a slow consumer.** Set `maxsize`.

</div>

## Try it yourself

1. Write `async def countdown(n)` that yields `n, n-1, ..., 1` with `await asyncio.sleep(0)` between items. Read it with `async for` and with an async comprehension.
2. Add a `try/finally` that prints "closed". Stop reading after two items, once without closing and once with `aclosing`. Compare when "closed" prints.
3. Write `async def numbered(stream)` that yields `(index, item)` pairs, like `enumerate` for async streams.

<div class="box" markdown="1">

## Where this appears in AI agents

Language model services stream their answer: the text arrives as many small chunks, and a chat program shows each one at once. The client code is an async generator that yields chunks, and the caller reads it with `async for`. The same pattern streams progress events from an agent ("calling tool", "tool finished") to a user interface, with a bounded queue so a slow screen does not make the agent pile up events.

```python
async for chunk in model.stream(prompt):
    print(chunk, end="", flush=True)
```

</div>

## Further reading

- [asynchronous iterators and generators](https://docs.python.org/3/reference/expressions.html#asynchronous-generator-functions)
- [`async for`](https://docs.python.org/3/reference/compound_stmts.html#the-async-for-statement)
- [`contextlib.aclosing` and `asynccontextmanager`](https://docs.python.org/3/library/contextlib.html)
- [asyncio queues](https://docs.python.org/3/library/asyncio-queue.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="34-async-generators-streaming:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/34-async-generators-streaming/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/34-async-generators-streaming/assignments/' | relative_url }}).
