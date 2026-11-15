---
layout: module
module: 14-inheritance-vs-composition
kind: assignments
title: Inheritance vs composition - assignments
permalink: /modules/14-inheritance-vs-composition/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/14-inheritance-vs-composition
```

---

<div class="assignment" markdown="1">

## Assignment 1: Shape hierarchy

**Goal:** Build an abstract `Shape` with concrete subclasses and functions that work on any shape. Practises inheritance, `super()`, abstract methods and polymorphism.

**Files:** [`starter.py`]({{ 'modules/14-inheritance-vs-composition/assignments/a1-shapes/starter.py' | relative_url }}), test file `test_a1_shapes.py` in the same folder.

```python
{% include_relative assignments/a1-shapes/starter.py %}
```

Run: `uv run pytest modules/14-inheritance-vs-composition/assignments/a1-shapes`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-shapes/solution.py %}
```

`Shape.describe` is written once and calls `self.area()`, so every subclass gets it for free. `Square` really is a `Rectangle`, so it inherits and only calls `super().__init__(side, side)`. `total_area` and `largest` never ask which kind of shape they have.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Car has an Engine

**Goal:** Compose a `Car` from an `Engine` object and delegate to it. Practises has-a design and swapping a part.

**Files:** [`starter.py`]({{ 'modules/14-inheritance-vs-composition/assignments/a2-car-engine/starter.py' | relative_url }}), test file `test_a2_car_engine.py` in the same folder.

```python
{% include_relative assignments/a2-car-engine/starter.py %}
```

Run: `uv run pytest modules/14-inheritance-vs-composition/assignments/a2-car-engine`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-car-engine/solution.py %}
```

`Car` receives its engine instead of creating one, so the tests can pass in a fake. `start`, `stop` and `is_running` delegate to the engine. `replace_engine` shows the benefit of composition: you can change the part while the car stays the same.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Notifier with pluggable senders

**Goal:** Write a `Notifier` that sends a message through any number of sender objects, and survives a sender that fails.

**Files:** [`starter.py`]({{ 'modules/14-inheritance-vs-composition/assignments/a3-notifier/starter.py' | relative_url }}), test file `test_a3_notifier.py` in the same folder.

```python
{% include_relative assignments/a3-notifier/starter.py %}
```

Run: `uv run pytest modules/14-inheritance-vs-composition/assignments/a3-notifier`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-notifier/solution.py %}
```

The notifier only needs `.name` and `.send()` from a sender, so you can add new kinds without changing it. It catches only `DeliveryError`. A real bug (any other exception) still shows up.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Mixins and a Protocol

**Goal:** Write two small mixins, combine them in one class, and write a function that accepts any object with a `render()` method.

**Files:** [`starter.py`]({{ 'modules/14-inheritance-vs-composition/assignments/a4-mixin-protocol/starter.py' | relative_url }}), test file `test_a4_mixin_protocol.py` in the same folder.

```python
{% include_relative assignments/a4-mixin-protocol/starter.py %}
```

Run: `uv run pytest modules/14-inheritance-vs-composition/assignments/a4-mixin-protocol`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-mixin-protocol/solution.py %}
```

Mixins add one feature each and use `vars(self)`, so they work for any class. The `Renderable` protocol is never inherited from. `Heading` and `Paragraph` match it because they have `render()`, which is duck typing written down.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="14-inheritance-vs-composition:assignments"> I have finished the assignments</label></li>
</ul>
