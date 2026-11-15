---
layout: module
module: 26-lambda-closures-partial
kind: learn
title: Lambda, closures and partial
permalink: /modules/26-lambda-closures-partial/
---

<div class="box key" markdown="1">

## Key learning points

- A `lambda` is a small anonymous function with **one expression** and no statements. Use it for short throw-away functions, mostly as a `key=` argument.
- `sorted`, `min` and `max` accept `key=function`. The function maps each item to the value used for comparison. A tuple key sorts by several fields.
- A **closure** is an inner function that remembers variables of the enclosing function. Use `nonlocal` to rebind such a variable.
- Closures look up variables **when called**, not when created. In a loop this causes the *late-binding* bug. Fix it with a default argument or `functools.partial`.
- `functools.partial` makes a new function with some arguments already filled in.
- `operator.itemgetter`, `attrgetter` and `methodcaller` replace many simple lambdas. Functions are values, so a `dict` of functions can replace a chain of `if` statements.

</div>

## 1. lambda

```python
square = lambda x: x * x
print(square(5))   # 25
```

A lambda has the form `lambda parameters: expression`. The expression is the return value. It cannot contain statements such as `return`, `if` blocks, loops or assignments. PEP 8 advises against assigning a lambda to a name: use `def` when the function needs a name. Lambdas earn their place when you pass them straight into another call.

## 2. key= functions

```python
words = ["pear", "Fig", "banana", "kiwi"]
print(sorted(words))                              # ['Fig', 'banana', 'kiwi', 'pear']
print(sorted(words, key=str.lower))               # ['banana', 'Fig', 'kiwi', 'pear']
print(sorted(words, key=lambda w: (len(w), w)))   # ['Fig', 'kiwi', 'pear', 'banana']
print(max(words, key=len), min(words, key=len))   # banana Fig
```

The default sort puts `"Fig"` first because capital letters sort before lower-case ones. `key=str.lower` compares the lower-cased text but keeps the original items. The tuple key `(len(w), w)` sorts by length first and uses the word to break ties. Add `reverse=True` for descending order.

## 3. map and filter versus comprehensions

```python
nums = [1, 2, 3, 4, 5, 6]
print(list(map(lambda n: n * 2, nums)))          # [2, 4, 6, 8, 10, 12]
print([n * 2 for n in nums])                     # same result
print(list(filter(lambda n: n % 2 == 0, nums)))  # [2, 4, 6]
print([n for n in nums if n % 2 == 0])           # same result
```

`map` and `filter` return lazy iterators, so `list(...)` is needed to see the values. Most Python code prefers the comprehension, which is shorter and needs no lambda. `map` reads well when you already have a named function: `list(map(str.strip, lines))`.

## 4. Closures and nonlocal

```python
def make_counter(start=0):
    count = start
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
print(c(), c(), c())    # 1 2 3
d = make_counter(10)
print(d(), c())         # 11 4
```

`counter` uses `count`, which belongs to `make_counter`. Python keeps `count` alive after `make_counter` returns. That pair (function plus captured variables) is a **closure**. Each call to `make_counter` creates a separate `count`, so `c` and `d` do not affect each other.

Without `nonlocal`, `count += 1` would make `count` a local variable of `counter`, and the first call would raise `UnboundLocalError`. Reading a captured variable needs no `nonlocal`. Rebinding it does. The captured values are stored in `c.__closure__`:

```python
print(c.__closure__[0].cell_contents)   # 4
```

## 5. The late-binding trap

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])    # [2, 2, 2]
```

All three lambdas share one variable `i`. They read it when called, after the loop has ended, so they all see the last value. Two fixes:

```python
funcs = [lambda i=i: i for i in range(3)]       # default argument is evaluated now
print([f() for f in funcs])                      # [0, 1, 2]

from functools import partial
funcs = [partial(lambda i: i, i) for i in range(3)]   # partial stores the value now
print([f() for f in funcs])                      # [0, 1, 2]
```

A default argument is evaluated once, when the `lambda` is created, so each function keeps its own copy.

## 6. functools.partial

```python
from functools import partial

binary = partial(int, base=2)
print(binary("1010"))             # 10

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
print(square(7))                  # 49
print(square.func.__name__, square.args, square.keywords)   # power () {'exponent': 2}
```

`partial(f, *args, **kwargs)` returns a callable that calls `f` with those arguments plus the ones you give later. Use it to configure a general function once (a logger with a prefix, a request function with a base URL) and pass the result around. The attributes `func`, `args` and `keywords` show what is stored.

## 7. operator helpers and function tables

```python
from operator import itemgetter, attrgetter, methodcaller

rows = [{"name": "Ana", "age": 31}, {"name": "Ben", "age": 25}]
print(sorted(rows, key=itemgetter("age")))
print(itemgetter("name", "age")(rows[0]))              # ('Ana', 31)
print(list(map(methodcaller("strip"), ["  a ", "b  "])))   # ['a', 'b']
```

```text
[{'name': 'Ben', 'age': 25}, {'name': 'Ana', 'age': 31}]
```

`itemgetter("age")` is the same as `lambda r: r["age"]`, and `attrgetter("score")` does the same for attributes (`obj.score`). Giving several names returns a tuple, which is a ready-made multi-field sort key. `methodcaller("strip")` calls `.strip()` on each item.

Functions are ordinary values, so you can keep them in a dictionary and look them up. This is a **function table**:

```python
import operator

ops = {"+": operator.add, "-": operator.sub, "*": operator.mul}
print(ops["*"](6, 7))    # 42
```

A closure can also build a pipeline from smaller steps:

```python
def compose(*funcs):
    def run(x):
        for f in funcs:
            x = f(x)
        return x
    return run

clean = compose(str.strip, str.lower, str.title)
print(clean("  hELLO wORLD "))    # Hello World
```

<div class="box" markdown="1">

## Where this appears in AI agents

An agent picks a function by name and calls it with arguments produced by a model. A function table is the simplest way to do that. `partial` fixes settings such as an API key or a base URL, so the model only supplies the remaining arguments.

```python
import operator

tools = {"add": operator.add, "mul": operator.mul}
call = {"name": "add", "args": [2, 3]}     # what a model might ask for
print(tools[call["name"]](*call["args"]))  # 5
```

Callbacks that report progress or log events are usually closures over a list or a logger.

</div>

<div class="box warn" markdown="1">

## Common mistakes

- **Lambdas in a loop that use the loop variable.** They all see the final value. Bind it with `lambda i=i: ...` or `partial`.
- **Forgetting `nonlocal`.** `count += 1` inside the inner function then raises `UnboundLocalError`.
- **Long or clever lambdas.** If it does not fit on one short line, write a `def` with a name and a docstring.
- **Expecting `map` or `filter` to return a list.** They return iterators that can be read once.
- **Mutable captured state shared by accident.** Two closures that capture the same list change each other's data.

</div>

## Try it yourself

1. Sort `["Banana", "apple", "cherry"]` case-insensitively with `key=`. Then sort it by length, longest first, using one `sorted` call.
2. Write `make_multiplier(n)` that returns a function multiplying its argument by `n`. Create `double` and `triple` and check that they stay independent.
3. Use `partial(round, ndigits=2)` to make a function `round2`. Check `round2(3.14159)`, then look at `round2.func`, `round2.args` and `round2.keywords`.

## Where this comes from

*Introducing Python*, chapter 10 (Functions), which covers lambdas, closures and functions as arguments. *Learn Python the Hard Way*, exercises 18 to 21 (functions). Closures, `partial` and `operator` go beyond the two books, so see the Python docs for [`functools.partial`](https://docs.python.org/3/library/functools.html#functools.partial) and the [`operator` module](https://docs.python.org/3/library/operator.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="26-lambda-closures-partial:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/26-lambda-closures-partial/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/26-lambda-closures-partial/assignments/' | relative_url }}).
