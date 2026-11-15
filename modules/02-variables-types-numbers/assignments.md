---
layout: module
module: 02-variables-types-numbers
kind: assignments
title: "Variables, types and numbers - assignments"
permalink: /modules/02-variables-types-numbers/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/02-variables-types-numbers
```

---

<div class="assignment" markdown="1">

## Assignment 1: Seconds to a clock

**Goal:** Split a number of seconds into days, hours, minutes and seconds, and format it as H:MM:SS. Practises `divmod` and f-string padding.

**Files:** [`starter.py`]({{ 'modules/02-variables-types-numbers/assignments/a1-seconds-to-clock/starter.py' | relative_url }}), test file `test_a1_seconds_to_clock.py` in the same folder.

```python
{% include_relative assignments/a1-seconds-to-clock/starter.py %}
```

Run: `uv run pytest modules/02-variables-types-numbers/assignments/a1-seconds-to-clock`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-seconds-to-clock/solution.py %}
```

`divmod(total, 3600)` returns the whole hours and the rest in one step. Repeat with 60 for minutes and seconds. `:02d` pads a number to two digits.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Unit converter

**Goal:** Convert temperatures and distances, then parse text like "100 C". Practises float arithmetic, `round`, `float()` and `ValueError`.

**Files:** [`starter.py`]({{ 'modules/02-variables-types-numbers/assignments/a2-unit-converter/starter.py' | relative_url }}), test file `test_a2_unit_converter.py` in the same folder.

```python
{% include_relative assignments/a2-unit-converter/starter.py %}
```

Run: `uv run pytest modules/02-variables-types-numbers/assignments/a2-unit-converter`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-unit-converter/solution.py %}
```

The text version splits the input, converts the number with `float()` (which raises `ValueError` for bad numbers) and picks a function by unit. `:.1f` formats the result with one decimal.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Bill splitter

**Goal:** Add a tip and split a bill so the shares add up to the total to the cent. Practises `Decimal`, rounding and `divmod`.

**Files:** [`starter.py`]({{ 'modules/02-variables-types-numbers/assignments/a3-bill-splitter/starter.py' | relative_url }}), test file `test_a3_bill_splitter.py` in the same folder.

```python
{% include_relative assignments/a3-bill-splitter/starter.py %}
```

Run: `uv run pytest modules/02-variables-types-numbers/assignments/a3-bill-splitter`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-bill-splitter/solution.py %}
```

`Decimal` built from strings avoids float errors, and `quantize` with `ROUND_HALF_UP` rounds to cents. To split fairly, work in whole cents: `divmod(cents, people)` gives the base share and the number of people who get one extra cent.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Safe numbers and BMI

**Goal:** Turn messy text into numbers without crashing, then compute and classify a BMI. Practises `int()`, `float()`, `try`/`except ValueError`, `None` and `if`/`elif`.

**Files:** [`starter.py`]({{ 'modules/02-variables-types-numbers/assignments/a4-parse-number/starter.py' | relative_url }}), test file `test_a4_parse_number.py` in the same folder.

```python
{% include_relative assignments/a4-parse-number/starter.py %}
```

Run: `uv run pytest modules/02-variables-types-numbers/assignments/a4-parse-number`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-parse-number/solution.py %}
```

`parse_number` tries `int` first so whole numbers stay `int`, then `float`. `math.isfinite` rejects `nan` and `inf`, which `float()` accepts. Returning `None` lets the caller decide what an invalid value means.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="02-variables-types-numbers:assignments"> I have finished the assignments</label></li>
</ul>
