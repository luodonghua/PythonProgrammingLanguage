---
layout: module
module: 31-inspect-and-json-schema
kind: assignments
title: inspect, runtime type hints and JSON Schema - assignments
permalink: /modules/31-inspect-and-json-schema/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

This topic uses `pydantic` in assignment 4. It is already included in the project's dev dependencies.

Run all tests for this topic:

```bash
uv run pytest modules/31-inspect-and-json-schema
```

---

<div class="assignment" markdown="1">

## Assignment 1: Describe a function

**Goal:** Read a function's signature with `inspect` and report each parameter. Also read its docstring and list an object's public methods.

**Files:** [`starter.py`]({{ 'modules/31-inspect-and-json-schema/assignments/a1-describe-function/starter.py' | relative_url }}), test file `test_a1_describe_function.py` in the same folder.

```python
{% include_relative assignments/a1-describe-function/starter.py %}
```

Run: `uv run pytest modules/31-inspect-and-json-schema/assignments/a1-describe-function`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-describe-function/solution.py %}
```

`inspect.signature(func).parameters.values()` gives `Parameter` objects. The default is the marker `Parameter.empty` when there is none, so compare with `is`. `inspect.getmembers(obj, callable)` finds methods, and the signature of a bound method has no `self`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Build a JSON Schema

**Goal:** Turn type hints and a function signature into a JSON Schema tool description. Practises `get_type_hints`, `get_origin`, `get_args` and recursion.

**Files:** [`starter.py`]({{ 'modules/31-inspect-and-json-schema/assignments/a2-build-schema/starter.py' | relative_url }}), test file `test_a2_build_schema.py` in the same folder.

```python
{% include_relative assignments/a2-build-schema/starter.py %}
```

Run: `uv run pytest modules/31-inspect-and-json-schema/assignments/a2-build-schema`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-build-schema/solution.py %}
```

`type_to_schema` calls itself for `list[T]` and for each member of a union. `build_schema` joins the per-parameter schemas and puts parameters without a default in `required`. Comparing the union origin with both `typing.Union` and `types.UnionType` makes the code work on every Python version.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Call with JSON arguments

**Goal:** Check a dict of arguments against a function's signature and hints, collect every problem, and call the function only when there are none.

**Files:** [`starter.py`]({{ 'modules/31-inspect-and-json-schema/assignments/a3-call-with-json-args/starter.py' | relative_url }}), test file `test_a3_call_with_json_args.py` in the same folder.

```python
{% include_relative assignments/a3-call-with-json-args/starter.py %}
```

Run: `uv run pytest modules/31-inspect-and-json-schema/assignments/a3-call-with-json-args`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-call-with-json-args/solution.py %}
```

Collect messages in a list instead of raising on the first problem, so the caller sees everything that is wrong at once. `matches` tests `bool` before `int`, because `True` is an instance of `int`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Schema and validation with pydantic

**Goal:** Build a pydantic model from a function signature with `create_model`. Use it to get a JSON Schema and to validate and coerce arguments.

**Files:** [`starter.py`]({{ 'modules/31-inspect-and-json-schema/assignments/a4-pydantic-schema/starter.py' | relative_url }}), test file `test_a4_pydantic_schema.py` in the same folder.

```python
{% include_relative assignments/a4-pydantic-schema/starter.py %}
```

Run: `uv run pytest modules/31-inspect-and-json-schema/assignments/a4-pydantic-schema`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-pydantic-schema/solution.py %}
```

Each parameter becomes a field `(type, default)`, with `...` meaning "required". `extra="forbid"` turns unknown keys into errors. `ValidationError.errors()` gives a list of dicts, which you reformat into short messages.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="31-inspect-and-json-schema:assignments"> I have finished the assignments</label></li>
</ul>
