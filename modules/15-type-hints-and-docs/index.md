---
layout: module
module: 15-type-hints-and-docs
kind: learn
title: Type hints and documentation
permalink: /modules/15-type-hints-and-docs/
---

<div class="box key" markdown="1">

## Key learning points

- **Type hints** (annotations) say what types a variable, parameter or return value should have: `name: str`, `-> int`.
- Python **does not enforce** hints when the program runs. Tools such as mypy, pyright and your editor check them.
- Common forms: `list[int]`, `dict[str, int]`, `tuple[float, float]`, `X | None`, `Callable[[int], str]`, `Literal["r", "w"]`, `TypedDict`.
- Write generic functions with the Python 3.12 syntax `def first[T](items: list[T]) -> T`.
- A **docstring** is the first string in a function, class or module. Good ones state purpose, arguments, return value and errors.
- **doctest** runs the `>>>` examples in docstrings, so documentation cannot silently go out of date.

</div>

## 1. Annotating variables, parameters and returns

```python
age: int = 30
names: list[str] = ["ann", "bob"]
scores: dict[str, int] = {"ann": 90}
point: tuple[float, float] = (1.0, 2.0)

def greet(name: str, times: int = 1) -> str:
    return ("Hello, " + name + "! ") * times
```

The syntax is `name: type` for variables and parameters, and `-> type` for the return value. `-> None` means "returns nothing useful".

Hints are **not checked at run time**:

```python
def double(x: int) -> int:
    return x * 2

print(double("ab"))   # a type checker complains, Python does not
```

```text
abab
```

The code runs because `"ab" * 2` is valid. A checker would report that you passed a `str` where an `int` is expected.

Python keeps the hints in `__annotations__`, and `typing.get_type_hints` reads them:

```python
from typing import get_type_hints

print(greet.__annotations__)
```

```text
{'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}
```

## 2. Optional values, unions and Callable

`X | Y` means "X or Y". `X | None` marks a value that may be missing:

```python
def find(items: list[str], target: str) -> int | None:
    for i, x in enumerate(items):
        if x == target:
            return i
    return None

print(find(["a", "b"], "b"), find(["a"], "z"))
```

```text
1 None
```

A checker will make you handle the `None` before you use the result as a number.

Functions are values too. `Callable[[args], return]` types them:

```python
from collections.abc import Callable

def apply(f: Callable[[int, int], int], a: int, b: int) -> int:
    return f(a, b)

print(apply(lambda x, y: x + y, 2, 3))
```

```text
5
```

## 3. Literal and TypedDict

`Literal` limits a value to a few exact choices:

```python
from typing import Literal

Mode = Literal["r", "w"]

def open_it(mode: Mode) -> str:
    return mode
```

A `TypedDict` describes a dictionary with known keys, which is common for JSON data:

```python
from typing import TypedDict

class Movie(TypedDict):
    title: str
    year: int

m: Movie = {"title": "Alien", "year": 1979}
print(m["title"], type(m))
```

```text
Alien <class 'dict'>
```

At run time `m` is a plain `dict`. The checker knows `m["year"]` is an `int` and flags `m["yeer"]`.

## 4. Generics

A function that returns an item of the same type it received needs a **type variable**. Python 3.12 added a short syntax for it:

```python
def first[T](items: list[T]) -> T:
    return items[0]

print(first([1, 2]), first(["a"]))

class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item

print(Box(3).get())
```

```text
1 a
3
```

`first([1, 2])` has type `int` for the checker, and `first(["a"])` has type `str`. A `type` statement (also 3.12) names a type: `type Pair = tuple[int, int]`.

## 5. Protocol and Any

A `Protocol` states which methods an object needs (see topic 14). `Any` switches checking off for a value. Use it rarely, because it hides mistakes.

## 6. Running a type checker

Hints pay off when a tool reads them. Install a checker as a development tool and run it on your files:

```bash
uv add --dev mypy
uv run mypy src/
```

Another popular checker is pyright (`pyright src/`). Most editors run one while you type. Start by annotating function signatures. Those give the biggest benefit. Python 3.14 evaluates annotations lazily (PEP 649 and PEP 749), so you no longer need quotes around a class name used before it is defined.

## 7. Docstrings

A docstring is the first statement of a function, class or module. Google style is easy to read:

```python
def average(nums: list[float]) -> float:
    """Return the mean of nums.

    Args:
        nums: A non-empty list of numbers.

    Returns:
        The arithmetic mean.

    Raises:
        ValueError: If nums is empty.
    """
    if not nums:
        raise ValueError("nums must not be empty")
    return sum(nums) / len(nums)
```

The first line is a short summary in the imperative mood ("Return ..."). `help(average)` and editors show the docstring. With type hints in the signature, do not repeat types in the text.

## 8. doctest: examples that run

Put examples in the docstring with `>>>`. The text after the prompt line is the expected output:

```python
def average(nums: list[float]) -> float:
    """Return the mean of nums.

    >>> average([1, 2, 3])
    2.0
    >>> average([])
    Traceback (most recent call last):
        ...
    ValueError: nums must not be empty
    """
    if not nums:
        raise ValueError("nums must not be empty")
    return sum(nums) / len(nums)

import doctest
print(doctest.testmod())
```

```text
TestResults(failed=0, attempted=2)
```

From the shell, run `python -m doctest -v yourfile.py`. For an exception, doctest compares only the traceback header and the last line (`ValueError: ...`).

<div class="box warn" markdown="1">

## Common mistakes

- **Believing hints are enforced.** `double("ab")` runs. Run a checker or write tests.
- **Mutable defaults with hints.** `def f(x: list[int] = [])` still shares one list. Use `x: list[int] | None = None`.
- **Using `Any` everywhere.** It turns the checker off. Prefer a real type or a `Protocol`.
- **Old spellings.** In new code write `list[int]` and `int | None`, not `List[int]` and `Optional[int]`.
- **Docstrings that repeat the code.** "Adds a and b" for `add(a, b)` helps nobody. Explain behaviour, edge cases and errors.

</div>

## Try it yourself

1. Add hints to `def total(prices, tax_rate)` and `def shout(words)` (list of strings, returns a string).
2. Write `last[T](items: list[T]) -> T | None` that returns `None` for an empty list. Add two doctest examples and run `python -m doctest -v`.
3. Define a `TypedDict` for `{"name": str, "tags": list[str]}` and write a function that takes one.

## Where this comes from

*Introducing Python*, chapter 14 (Type Hints and Documentation). *Learn Python the Hard Way* has no matching exercise, but exercise 47 uses docstrings and tests. See also the Python docs for [`typing`](https://docs.python.org/3/library/typing.html), [`doctest`](https://docs.python.org/3/library/doctest.html) and the [type hints cheat sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="15-type-hints-and-docs:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/15-type-hints-and-docs/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/15-type-hints-and-docs/assignments/' | relative_url }}).
