---
layout: module
module: 13-classes-and-objects
kind: assignments
title: Classes and objects - assignments
permalink: /modules/13-classes-and-objects/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/13-classes-and-objects
```

---

<div class="assignment" markdown="1">

## Assignment 1: Bank account

**Goal:** Build a class that validates its input and protects its balance with a read-only property. Practises `__init__`, properties, `ValueError` and `__repr__`.

**Files:** [`starter.py`]({{ 'modules/13-classes-and-objects/assignments/a1-bank-account/starter.py' | relative_url }}), test file `test_a1_bank_account.py` in the same folder.

```python
{% include_relative assignments/a1-bank-account/starter.py %}
```

Run: `uv run pytest modules/13-classes-and-objects/assignments/a1-bank-account`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-bank-account/solution.py %}
```

The balance lives in `self._balance`. Only `deposit` and `withdraw` change it, and they check the amount **before** touching the balance, so a failed call leaves the account unchanged.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Vector2D with operators

**Goal:** Make your own type work with `+`, `-`, `*`, `==`, `abs()`, unpacking and `bool()` by writing special methods.

**Files:** [`starter.py`]({{ 'modules/13-classes-and-objects/assignments/a2-vector2d/starter.py' | relative_url }}), test file `test_a2_vector2d.py` in the same folder.

```python
{% include_relative assignments/a2-vector2d/starter.py %}
```

Run: `uv run pytest modules/13-classes-and-objects/assignments/a2-vector2d`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-vector2d/solution.py %}
```

Each operator method returns `NotImplemented` for types it does not support, so Python raises a clear `TypeError`. `__rmul__ = __mul__` makes `3 * v` work as well as `v * 3`. `__iter__` enables `x, y = v`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Stack and Queue

**Goal:** Write two small container classes. Practises `__len__`, `__iter__`, `__repr__`, truthiness and choosing the right data structure.

**Files:** [`starter.py`]({{ 'modules/13-classes-and-objects/assignments/a3-stack-queue/starter.py' | relative_url }}), test file `test_a3_stack_queue.py` in the same folder.

```python
{% include_relative assignments/a3-stack-queue/starter.py %}
```

Run: `uv run pytest modules/13-classes-and-objects/assignments/a3-stack-queue`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-stack-queue/solution.py %}
```

Both classes only define `__len__`, so `bool()` works through the length. The stack wraps a list (fast at the end). The queue wraps `collections.deque`, because `list.pop(0)` is slow for long lists while `deque.popleft()` is fast.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Inventory with an alternative constructor

**Goal:** Combine a property, container methods and a `@classmethod` that builds an object from text.

**Files:** [`starter.py`]({{ 'modules/13-classes-and-objects/assignments/a4-inventory/starter.py' | relative_url }}), test file `test_a4_inventory.py` in the same folder.

```python
{% include_relative assignments/a4-inventory/starter.py %}
```

Run: `uv run pytest modules/13-classes-and-objects/assignments/a4-inventory`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-inventory/solution.py %}
```

`from_text` calls `cls()`, not `Inventory()`, so subclasses get an instance of their own type. Items whose count reaches 0 are deleted, which keeps `len()` and `in` honest.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="13-classes-and-objects:assignments"> I have finished the assignments</label></li>
</ul>
