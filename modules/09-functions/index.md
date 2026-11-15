---
layout: module
module: 09-functions
kind: learn
title: Functions
permalink: /modules/09-functions/
---

<div class="box key" markdown="1">

## Key learning points

- `def name(parameters):` defines a function. `return` sends a value back. Without `return`, a function gives back `None`.
- **Parameters** are the names in the `def` line. **Arguments** are the values you pass in a call.
- Defaults, `*args` and `**kwargs`, keyword-only (`*`) and positional-only (`/`) parameters control how callers pass values.
- Names are looked up in the order **L**ocal, **E**nclosing, **G**lobal, **B**uilt-in (LEGB). Assigning inside a function makes the name local.
- Never use a mutable value such as `[]` as a default. Use `None` and create the list inside.
- Functions are values. You can store them in variables and dicts, pass them in and return them.

</div>

## 1. Defining and calling

```python
def area(width, height=1):
    """Return the area of a rectangle."""
    return width * height

print(area(3, 4))                  # 12
print(area(3))                     # 3
print(area(height=2, width=5))     # 10
```

The string right after the `def` line is the **docstring**. Tools and `help(area)` show it.

A function without `return` gives back `None`:

```python
def say(x):
    print(x)

print(say("hi"))     # prints hi, then None
```

Return several values by returning a tuple, and unpack them at the call:

```python
def min_max(nums):
    return min(nums), max(nums)

low, high = min_max([3, 1, 4])
print(low, high)     # 1 4
```

Keep functions small and let each do one job. Prefer `return` over `print` inside a function, so the caller decides what to do with the result.

## 2. Parameter kinds

```python
def total(*nums):          # *nums collects extra positional arguments in a tuple
    return sum(nums)

def show(**opts):          # **opts collects extra keyword arguments in a dict
    print(opts)

print(total(1, 2, 3))      # 6
show(a=1, b=2)             # {'a': 1, 'b': 2}
```

Two special markers in the parameter list:

```python
def f(a, /, b, *, c):
    return (a, b, c)

print(f(1, 2, c=3))        # (1, 2, 3)
print(f(1, b=2, c=3))      # (1, 2, 3)
```

- Parameters **before `/`** must be passed by position.
- Parameters **after `*`** must be passed by keyword.
- Between them, either way works.

`f(a=1, b=2, c=3)` raises `TypeError: f() got some positional-only arguments passed as keyword arguments: 'a'`, and `f(1, 2, 3)` raises `TypeError: f() takes 2 positional arguments but 3 were given`.

At a call, `*` and `**` unpack a sequence or dict into arguments:

```python
args = (1, 2)
kwargs = {"c": 3}
print(f(*args, **kwargs))  # (1, 2, 3)
```

## 3. The mutable default pitfall

Python evaluates a default value **once**, when `def` runs. A list default is then shared by every call:

```python
def bad(item, items=[]):
    items.append(item)
    return items

print(bad(1))    # [1]
print(bad(2))    # [1, 2]   surprise: the same list again
```

The fix is to use `None` and create the list inside:

```python
def good(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items

print(good(1))   # [1]
print(good(2))   # [2]
```

## 4. Scope: LEGB

```python
x = "global"

def show_x():
    x = "local"      # a new local name, the global x is untouched
    return x

print(show_x(), x)   # local global
```

Assigning to a name inside a function creates a **local** variable. To rebind a module-level name, declare it with `global`:

```python
count = 0

def inc():
    global count
    count += 1

inc()
inc()
print(count)         # 2
```

Use `global` rarely. Passing values in and returning results is easier to test.

A function defined inside another function can read the outer function's variables. Use `nonlocal` to rebind them:

```python
def make_counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step

c = make_counter()
print(c(), c())      # 1 2
```

`step` is a **closure**: it keeps the variable `n` alive after `make_counter` returns.

## 5. Recursion

A function may call itself. It needs a **base case** that stops the calls.

```python
def fact(n):
    return 1 if n == 0 else n * fact(n - 1)

print(fact(5))       # 120
```

Python limits the call depth (`sys.getrecursionlimit()` is 1000 by default). A function that never reaches its base case ends with `RecursionError`. For long inputs a loop is safer. To avoid repeated work, for example in Fibonacci numbers, store results in a dict.

## 6. Functions are values

```python
def apply(func, value):
    return func(value)

print(apply(str.upper, "abc"))   # ABC
print(apply(len, "abc"))         # 3

ops = {"double": lambda v: v * 2}
print(ops["double"](4))          # 8
```

Note that `apply(len, ...)` passes the function itself. `len(...)` would call it first. This idea powers callbacks, dispatch tables and decorators, which later topics build on.

<div class="box warn" markdown="1">

## Common mistakes

- **Mutable default values.** `def f(x, items=[])` shares one list between calls. Use `None`.
- **Printing instead of returning.** A function that only prints cannot be reused in a calculation, and its result is `None`.
- **Forgetting the parentheses.** `area` is the function. `area(3)` calls it.
- **Assigning to a global without `global`.** `count += 1` inside a function fails with `UnboundLocalError` because `count` is local there.
- **Recursion without a base case.** The calls never stop and Python raises `RecursionError`.

</div>

## Try it yourself

1. Write `is_even(n)` that returns `True` or `False`, and use it in a list comprehension.
2. Write `describe(name, *hobbies, **details)` and call it with several hobbies and a few keyword details. Print what each parameter contains.
3. Write a recursive `countdown(n)` that returns `[n, n-1, ..., 1]`. What happens with `countdown(5000)`?

## Further reading

- [Python tutorial: defining functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="09-functions:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/09-functions/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/09-functions/assignments/' | relative_url }}).
