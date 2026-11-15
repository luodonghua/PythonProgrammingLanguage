---
layout: module
module: 27-decorators-functools
kind: learn
title: Decorators and functools
permalink: /modules/27-decorators-functools/
---

<div class="box key" markdown="1">

## Key learning points

- A **decorator** is a function that takes a function and returns a replacement. `@deco` above a `def` is shorthand for `f = deco(f)`.
- Inside a decorator, write a `wrapper(*args, **kwargs)` and add `@functools.wraps(func)` so the name and docstring survive.
- A decorator **with arguments** is a function that returns a decorator: three levels of `def`.
- A decorator can register a function (a plugin or command table) and return it unchanged.
- `functools` ships ready-made helpers: `cache`, `lru_cache`, `cached_property`, `singledispatch`, `total_ordering`.
- For code you want to test, **inject** the clock or the `sleep` function instead of calling `time` directly.

</div>

## 1. Functions are objects

You can pass a function to another function, return it, and store it in a dict. A decorator uses exactly that.

```python
def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@shout
def greet(name):
    """Return a greeting."""
    return f"hello {name}"

print(greet("ada"))
```

```text
HELLO ADA
```

The line `@shout` runs `greet = shout(greet)` right after the `def`. The name `greet` now points at `wrapper`.

## 2. Keep the metadata with functools.wraps

```python
print(greet.__name__, greet.__doc__)
```

```text
wrapper None
```

The wrapper hides the original name and docstring. That breaks help text, logs and debuggers. Fix it with `functools.wraps`:

```python
import functools

def shout(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper
```

Now `greet.__name__` is `greet` and `greet.__doc__` is `Return a greeting.` Always use `wraps`.

## 3. Decorators with arguments

`@repeat(times=3)` first **calls** `repeat(times=3)`. That call must return the real decorator.

```python
def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def ping():
    print("ping")

ping()
```

```text
ping
ping
ping
```

## 4. Class-based decorators

An object with a `__call__` method can act as the wrapper. This is handy when the decorator keeps state.

```python
class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def hello():
    return "hi"

hello()
hello()
print(hello.calls)   # 2
```

A function can hold state too: set `wrapper.calls = 0` and update it inside the wrapper.

## 5. Registries

A decorator does not have to wrap anything. It can record the function and hand it back.

```python
COMMANDS = {}

def command(func):
    COMMANDS[func.__name__] = func
    return func

@command
def start():
    return "started"

@command
def stop():
    return "stopped"

print(sorted(COMMANDS), COMMANDS["stop"]())
```

```text
['start', 'stop'] stopped
```

Job runners, web frameworks and plugin systems use this pattern: `@app.route("/")`, `@pytest.fixture`, `@command`.

## 6. Timing and retry, with injected helpers

A decorator that calls `time.sleep` is slow to test. Take the function as a parameter with a default:

```python
import time

def timed(clock=time.perf_counter):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = clock()
            try:
                return func(*args, **kwargs)
            finally:
                print(f"{func.__name__} took {clock() - start:.1f}s")
        return wrapper
    return decorator

ticks = iter([10.0, 12.5])

@timed(clock=lambda: next(ticks))
def work():
    return "done"

print(work())
```

```text
work took 2.5s
done
```

The test supplies a fake clock, so the output is always the same. A `retry(times, sleep=time.sleep)` decorator works the same way: tests pass `sleep=fake_sleep` and nothing waits.

## 7. Caching: cache and lru_cache

`functools.cache` remembers results by arguments. The arguments must be hashable.

```python
@functools.cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(80))
print(fib.cache_info())
```

```text
23416728348467685
CacheInfo(hits=78, misses=81, maxsize=None, currsize=81)
```

Without the cache, `fib(80)` would take longer than you want to wait. `lru_cache(maxsize=N)` keeps only the N most recently used results:

```python
@functools.lru_cache(maxsize=2)
def square(n):
    return n * n

for n in (1, 2, 1, 3, 2):
    square(n)
print(square.cache_info())
```

```text
CacheInfo(hits=1, misses=4, maxsize=2, currsize=2)
```

Only cache **pure** functions (same input, same output, no side effects).

## 8. singledispatch, cached_property, total_ordering

`singledispatch` picks an implementation by the type of the first argument:

```python
from functools import singledispatch

@singledispatch
def describe(value):
    return f"object {value!r}"

@describe.register
def _(value: int):
    return f"int {value}"

@describe.register
def _(value: list):
    return f"list of {len(value)}"

print(describe(5))
print(describe([1, 2]))
print(describe(2.5))
```

```text
int 5
list of 2
object 2.5
```

`cached_property` computes an attribute once per instance:

```python
class Report:
    def __init__(self, rows):
        self.rows = rows

    @functools.cached_property
    def total(self):
        print("computing")
        return sum(self.rows)

r = Report([1, 2, 3])
print(r.total)
print(r.total)
```

```text
computing
6
6
```

`total_ordering` fills in `<=`, `>` and `>=` when you define `==` and one of `<`, `<=`, `>`, `>=`:

```python
@functools.total_ordering
class Version:
    def __init__(self, text):
        self.parts = tuple(int(p) for p in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

print(Version("1.2") < Version("1.10"), Version("2.0") >= Version("1.9"))
```

```text
True True
```

<div class="box warn" markdown="1">

## Common mistakes

- **Forgetting `functools.wraps`.** Every decorated function then shows up as `wrapper` in logs and tracebacks.
- **Forgetting to return the result** from the wrapper, so the decorated function always returns `None`.
- **Writing `@repeat` instead of `@repeat(3)`** for a decorator with arguments. Python passes the function in as `times`.
- **Caching a function with side effects, or with mutable results.** A cached list is shared by every caller. A cached function that must read fresh data returns stale data.
- **Passing unhashable arguments** (a list or dict) to a cached function. It raises `TypeError`.

</div>

<div class="box" markdown="1">

## Where this appears in AI agents

Agent code uses decorators to turn plain Python functions into **tools**. A `@tool` decorator records the function in a registry, so the agent can list the available tools and call one by name. The same code often wraps tools with a retry decorator for flaky network calls, and with `cache` for repeated lookups.

```python
TOOLS = {}

def tool(func):
    TOOLS[func.__name__] = func
    return func
```

Topic 38 builds a full tool registry on this idea.

</div>

## Try it yourself

1. Write a decorator `announce` that prints `calling <name>` before each call of the decorated function. Check that `__name__` is kept.
2. Write `retry(times)` that calls the function again when it raises `ValueError`, and raises the last error after `times` attempts.
3. Decorate a slow function with `functools.cache`. Call it twice and look at `cache_info()`.

## Where this comes from

*Introducing Python*, chapter 10 (Functions), the section on decorators. *Learn Python the Hard Way* has no decorator exercise, so this topic goes beyond that book. See the Python docs: [functools](https://docs.python.org/3/library/functools.html) and [glossary: decorator](https://docs.python.org/3/glossary.html#term-decorator).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="27-decorators-functools:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/27-decorators-functools/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/27-decorators-functools/assignments/' | relative_url }}).
