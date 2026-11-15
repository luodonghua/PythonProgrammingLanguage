---
layout: module
module: 30-dataclasses-pydantic
kind: assignments
title: Dataclasses and Pydantic - assignments
permalink: /modules/30-dataclasses-pydantic/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Assignments 2 to 4 use **Pydantic**, which the project already lists as a dependency. Assignment 3 reads a small data file, `products.json`, from its folder.

Run all tests for this topic:

```bash
uv run pytest modules/30-dataclasses-pydantic
```

---

<div class="assignment" markdown="1">

## Assignment 1: Order dataclasses

**Goal:** Model an order with a frozen `LineItem` and an `Order` dataclass that validates itself in `__post_init__`, computes totals in integer cents, and returns changed copies. Practises `frozen`, `field(default_factory=...)`, `replace` and `asdict`.

**Files:** [`starter.py`]({{ 'modules/30-dataclasses-pydantic/assignments/a1-order/starter.py' | relative_url }}), test file `test_a1_order.py` in the same folder.

```python
{% include_relative assignments/a1-order/starter.py %}
```

Run: `uv run pytest modules/30-dataclasses-pydantic/assignments/a1-order`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-order/solution.py %}
```

`LineItem` is frozen, so nothing can change it after creation. `Order.items` uses `default_factory=list` so each order gets its own list. `with_item` builds a new list and calls `replace`, which copies the order without touching the original. Integer cents avoid float rounding errors.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: A validated user model

**Goal:** Write a Pydantic `User` model with constraints and a custom email validator, then parse a batch of rows and report which fields failed. Practises `Field`, `field_validator`, coercion and `ValidationError.errors()`.

**Files:** [`starter.py`]({{ 'modules/30-dataclasses-pydantic/assignments/a2-user-model/starter.py' | relative_url }}), test file `test_a2_user_model.py` in the same folder.

```python
{% include_relative assignments/a2-user-model/starter.py %}
```

Run: `uv run pytest modules/30-dataclasses-pydantic/assignments/a2-user-model`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-user-model/solution.py %}
```

`str_strip_whitespace` cleans strings before the length checks. The email validator runs after the type check and can return a changed value (lower-case). `exc.errors()` is a list of dicts, and the first item of `loc` is the field name.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Messy JSON into models

**Goal:** Parse a JSON file with strings for numbers, comma-separated tags and invalid rows into `Product` models, collecting errors instead of stopping. Practises coercion, a `mode="before"` validator and error reporting.

**Files:** [`starter.py`]({{ 'modules/30-dataclasses-pydantic/assignments/a3-messy-json/starter.py' | relative_url }}), test file `test_a3_messy_json.py` in the same folder. The data file `products.json` is in the same folder.

```python
{% include_relative assignments/a3-messy-json/starter.py %}
```

Run: `uv run pytest modules/30-dataclasses-pydantic/assignments/a3-messy-json`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-messy-json/solution.py %}
```

A `mode="before"` validator sees the raw input, so it can turn `"a, b"` into a list before Pydantic checks the type. `load_products` catches `ValidationError` per row, so one bad row does not stop the rest. The `type` of an error (such as `float_parsing`) is stable and machine-readable.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Parse until valid

**Goal:** Write a loop that asks a producer for JSON, validates it, and on failure asks again with the validation errors in the prompt. The tests use a scripted fake producer, so nothing is random. Practises `model_validate_json`, error formatting and custom exceptions.

**Files:** [`starter.py`]({{ 'modules/30-dataclasses-pydantic/assignments/a4-parse-until-valid/starter.py' | relative_url }}), test file `test_a4_parse_until_valid.py` in the same folder.

```python
{% include_relative assignments/a4-parse-until-valid/starter.py %}
```

Run: `uv run pytest modules/30-dataclasses-pydantic/assignments/a4-parse-until-valid`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-parse-until-valid/solution.py %}
```

`model_validate_json` also reports invalid JSON as a `ValidationError` (with an empty `loc`), so one `except` handles both problems. Each new prompt starts from the original task, so feedback does not pile up. Attributes on `GaveUp` let the caller see what went wrong.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="30-dataclasses-pydantic:assignments"> I have finished the assignments</label></li>
</ul>
