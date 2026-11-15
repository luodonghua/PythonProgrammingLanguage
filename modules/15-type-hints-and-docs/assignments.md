---
layout: module
module: 15-type-hints-and-docs
kind: assignments
title: "Type hints and documentation - assignments"
permalink: /modules/15-type-hints-and-docs/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/15-type-hints-and-docs
```

---

<div class="assignment" markdown="1">

## Assignment 1: Add type hints

**Goal:** Annotate six working functions with the exact types listed in the task. Practises `list[...]`, `dict[...]`, `X | None`, `Callable`, `Literal` and `-> None`.

**Files:** [`starter.py`]({{ 'modules/15-type-hints-and-docs/assignments/a1-add-hints/starter.py' | relative_url }}), test file `test_a1_add_hints.py` in the same folder.

```python
{% include_relative assignments/a1-add-hints/starter.py %}
```

Run: `uv run pytest modules/15-type-hints-and-docs/assignments/a1-add-hints`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-add-hints/solution.py %}
```

The bodies do not change. The tests read the annotations with `typing.get_type_hints`, which is the same data a type checker or editor uses. Use `collections.abc.Callable` for functions.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Docstrings with doctest examples

**Goal:** Add working `>>>` examples to three docstrings, including one that shows an exception.

**Files:** [`starter.py`]({{ 'modules/15-type-hints-and-docs/assignments/a2-doctests/starter.py' | relative_url }}), test file `test_a2_doctests.py` in the same folder.

```python
{% include_relative assignments/a2-doctests/starter.py %}
```

Run: `uv run pytest modules/15-type-hints-and-docs/assignments/a2-doctests`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-doctests/solution.py %}
```

Each example is a real call with its real output. For an exception, doctest compares the `Traceback` header and the last line, so the middle may be written as `...`. Run `python -m doctest -v solution.py` to see each example run.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Generic functions and a generic class

**Goal:** Use the Python 3.12 type-parameter syntax to write `first`, `last`, `pairs` and a `Box[T]` class with a generic `map` method.

**Files:** [`starter.py`]({{ 'modules/15-type-hints-and-docs/assignments/a3-generics/starter.py' | relative_url }}), test file `test_a3_generics.py` in the same folder.

```python
{% include_relative assignments/a3-generics/starter.py %}
```

Run: `uv run pytest modules/15-type-hints-and-docs/assignments/a3-generics`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-generics/solution.py %}
```

`def first[T](...)` and `class Box[T]` create type parameters without importing `TypeVar`. The method `map[U]` has its own parameter `U`, so `Box[int].map(str)` is a `Box[str]` for a type checker. At run time nothing about `T` is checked.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: TypedDict record validator

**Goal:** Write a validator that checks a dict against the hints of a `TypedDict`, because Python does not do it for you.

**Files:** [`starter.py`]({{ 'modules/15-type-hints-and-docs/assignments/a4-typeddict-validator/starter.py' | relative_url }}), test file `test_a4_typeddict_validator.py` in the same folder.

```python
{% include_relative assignments/a4-typeddict-validator/starter.py %}
```

Run: `uv run pytest modules/15-type-hints-and-docs/assignments/a4-typeddict-validator`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-typeddict-validator/solution.py %}
```

`get_type_hints(schema)` returns the field names and types in order. `get_origin` and `get_args` take `list[str]` apart. A `bool` is a subclass of `int`, so the code excludes it with an explicit check.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="15-type-hints-and-docs:assignments"> I have finished the assignments</label></li>
</ul>
