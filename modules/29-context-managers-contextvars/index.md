---
layout: module
module: 29-context-managers-contextvars
kind: learn
title: Context managers and contextvars
permalink: /modules/29-context-managers-contextvars/
---

<div class="box key" markdown="1">

## Key learning points

- A `with` block guarantees **setup and cleanup**: the cleanup runs even when the body raises an error.
- A context manager is any object with `__enter__` and `__exit__`. The value after `as` is what `__enter__` returns.
- `@contextlib.contextmanager` turns a generator with one `yield` into a context manager. Put cleanup in `finally`.
- `contextlib` has ready-made tools: `suppress`, `closing`, `redirect_stdout`, `ExitStack`.
- A `ContextVar` holds a value that is **separate for each task or context**, such as a request id. Use `set()` (which returns a `Token`), `get()` and `reset(token)`.
- Thread-locals do not work for async code, because many tasks share one thread. `ContextVar` does.

</div>

## 1. What `with` does

```python
with open("data.txt", encoding="utf-8") as file:
    text = file.read()
# the file is closed here, even if read() raised an error
```

This is the same as a `try` / `finally` that always calls `file.close()`, but shorter and harder to get wrong.

## 2. A class-based context manager

```python
class Tag:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"<{self.name}>")
        return self

    def __exit__(self, exc_type, exc, tb):
        print(f"</{self.name}>")
        return False

with Tag("b") as t:
    print("text")
```

```text
<b>
text
</b>
```

`__exit__` receives the exception type, value and traceback (all `None` if there was no error). If it returns a **true** value, the exception is swallowed. If it returns `False` or `None`, the exception continues:

```python
try:
    with Tag("i"):
        raise ValueError("boom")
except ValueError as e:
    print("caught", e)
```

```text
<i>
</i>
caught boom
```

The closing tag still printed. Return `True` from `__exit__` only when you mean to hide an error.

## 3. contextmanager: the short way

```python
import os
from contextlib import contextmanager

@contextmanager
def chdir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)
```

Code before `yield` is the setup. Code after it is the cleanup. The `try` / `finally` is what makes the cleanup run when the body raises. The value you `yield` becomes the `as` target. This is how you build a timer, a temporary setting, or a transaction:

```python
@contextmanager
def transaction(items):
    snapshot = list(items)
    try:
        yield items
    except Exception:
        items[:] = snapshot   # roll back
        raise                 # and let the error continue

data = [1]
try:
    with transaction(data) as d:
        d.append(2)
        raise RuntimeError
except RuntimeError:
    pass
print(data)   # [1]
```

## 4. Tools in contextlib

```python
import io
from contextlib import suppress, redirect_stdout, closing, ExitStack

with suppress(FileNotFoundError):
    os.remove("old-cache.tmp")        # no error if the file is missing

buf = io.StringIO()
with redirect_stdout(buf):
    print("hidden")
print(repr(buf.getvalue()))           # 'hidden\n'
```

- `suppress(*errors)` ignores the listed exceptions.
- `redirect_stdout(target)` sends `print` output to a file-like object. It is handy in tests.
- `closing(obj)` calls `obj.close()` at the end, for objects that have `close()` but no `__exit__`.
- `ExitStack` collects any number of cleanups and runs them in reverse order. It suits "open all these files" when the count is only known at run time:

```python
with ExitStack() as stack:
    for n in range(3):
        stack.callback(print, "cleanup", n)
    print("working")
```

```text
working
cleanup 2
cleanup 1
cleanup 0
```

## 5. ContextVar: values that follow the task

A global variable is shared by everything. You often need a value that belongs to **one request or one task**, such as a request id used in log lines. `contextvars.ContextVar` provides that.

```python
import contextvars

request_id = contextvars.ContextVar("request_id", default="-")

print(request_id.get())        # -
token = request_id.set("abc")
print(request_id.get())        # abc
request_id.reset(token)        # go back to the previous value
print(request_id.get())        # -
```

`set()` returns a **Token**. Passing it to `reset()` restores exactly the old value. Create `ContextVar` objects at module level, not inside functions.

## 6. Context and asyncio

Each asyncio task runs in its own **copy** of the current context, taken when the task is created. A `set()` inside one task does not leak into the others:

```python
import asyncio

async def handle(rid):
    request_id.set(rid)
    await asyncio.sleep(0)               # let other tasks run
    return f"{rid} sees {request_id.get()}"

async def main():
    return await asyncio.gather(handle("r1"), handle("r2"), handle("r3"))

print(asyncio.run(main()))
print(request_id.get())
```

```text
['r1 sees r1', 'r2 sees r2', 'r3 sees r3']
-
```

Each task kept its own value, and the outer value is untouched. (`gather` wraps each coroutine in a task. Async code is covered fully in topic 32.)

A `threading.local()` fails here, because all three tasks run on the same thread and share it:

```python
import threading

local = threading.local()

async def bad(n):
    local.value = n
    await asyncio.sleep(0)
    return local.value

async def main2():
    return await asyncio.gather(bad(1), bad(2))

print(asyncio.run(main2()))   # [2, 2]
```

Task 1 expected 1 but read the value task 2 wrote.

You can also run code in a copy of the context by hand:

```python
ctx = contextvars.copy_context()

def work():
    request_id.set("inside")
    return request_id.get()

print(ctx.run(work), request_id.get())   # inside -
```

## 7. A context manager around a ContextVar

Combine both ideas to set a value for the length of a block and restore it afterwards:

```python
@contextmanager
def bind_request_id(value):
    token = request_id.set(value)
    try:
        yield
    finally:
        request_id.reset(token)
```

<div class="box warn" markdown="1">

## Common mistakes

- **Cleanup outside `finally`.** In a `@contextmanager` function, code after `yield` that is not in `finally` is skipped when the body raises.
- **Yielding twice.** A `@contextmanager` generator must `yield` exactly once.
- **Returning `True` from `__exit__` by accident.** It hides every exception in the block.
- **Using `threading.local` in async code.** Use `ContextVar`.
- **Creating a `ContextVar` inside a function.** Contexts keep a reference to each variable, so create them once at module level.
- **Forgetting `reset`.** A `set()` without a matching `reset` leaves the value in place for the rest of that context.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

An agent often runs many tool calls at once. A **trace id** stored in a `ContextVar` lets every log line say which run it belongs to, without passing the id through each function. A context manager can also wrap each tool call: start a timer, open a span, and close it even when the tool fails.

```python
trace_id = contextvars.ContextVar("trace_id", default="-")

with bind_trace_id("run-42"):
    run_agent()      # every log line in here can read trace_id.get()
```

</div>

## Try it yourself

1. Write a `@contextmanager` called `timer(clock)` that prints how long the block took, using the `clock` function you pass in.
2. Use `suppress(KeyError)` to delete a key from a dict that may not have it.
3. Create a `ContextVar` named `user`. Write an async function that sets it, awaits `asyncio.sleep(0)`, and returns `user.get()`. Run three of them with `gather`.

## Further reading

- [contextlib](https://docs.python.org/3/library/contextlib.html)
- [contextvars](https://docs.python.org/3/library/contextvars.html)
- [The with statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="29-context-managers-contextvars:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/29-context-managers-contextvars/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/29-context-managers-contextvars/assignments/' | relative_url }}).
