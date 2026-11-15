---
layout: module
module: 09-functions
kind: assignments
title: Functions - assignments
permalink: /modules/09-functions/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/09-functions
```

---

<div class="assignment" markdown="1">

## Assignment 1: Statistics helpers

**Goal:** Write `min_max`, `mean`, `median`, `stats` and `split_name`. Practises `return`, returning several values, empty-input edge cases and reusing your own functions.

**Files:** [`starter.py`]({{ 'modules/09-functions/assignments/a1-stats/starter.py' | relative_url }}), test file `test_a1_stats.py` in the same folder.

```python
{% include_relative assignments/a1-stats/starter.py %}
```

Run: `uv run pytest modules/09-functions/assignments/a1-stats`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-stats/solution.py %}
```

Each function returns a value and prints nothing. `min_max` returns a tuple. `median` sorts a **copy** with `sorted`, so the caller's list stays unchanged, and averages the two middle items for even lengths. `stats` calls the other helpers instead of repeating their code.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Flexible arguments

**Goal:** Build helpers that use keyword-only (`*`), positional-only (`/`), `*args` and `**kwargs` parameters, for example `join_path(*parts, sep="/")` and `make_tag`. Practises reading and writing function signatures.

**Files:** [`starter.py`]({{ 'modules/09-functions/assignments/a2-flexible-arguments/starter.py' | relative_url }}), test file `test_a2_flexible_arguments.py` in the same folder.

```python
{% include_relative assignments/a2-flexible-arguments/starter.py %}
```

Run: `uv run pytest modules/09-functions/assignments/a2-flexible-arguments`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-flexible-arguments/solution.py %}
```

`*parts` collects the positional arguments in a tuple, and `sep` after it is keyword-only. `make_tag` receives the attributes as a dict in `**attributes` and builds the text with a generator expression. `call_with` forwards everything with `func(*args, **kwargs)`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Recursion

**Goal:** Write `factorial`, `sum_digits`, a cached `fib`, a deep `flatten` and `power_set_size` recursively. Practises base cases, shrinking the problem and caching results in a dict.

**Files:** [`starter.py`]({{ 'modules/09-functions/assignments/a3-recursion/starter.py' | relative_url }}), test file `test_a3_recursion.py` in the same folder.

```python
{% include_relative assignments/a3-recursion/starter.py %}
```

Run: `uv run pytest modules/09-functions/assignments/a3-recursion`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-recursion/solution.py %}
```

Every recursive function has a base case (`n == 0`, `n < 10`, an empty list) and a call on a smaller input. `fib` passes one `cache` dict down through the calls, so each value is computed once and `fib(80)` is instant. The default is `None`, not `{}`, to avoid the shared mutable default.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Defaults, closures and functions as values

**Goal:** Fix the mutable default bug, apply a function n times, compose functions, build a counter with a closure and run a dict of functions. Practises `nonlocal`, inner functions and passing functions around.

**Files:** [`starter.py`]({{ 'modules/09-functions/assignments/a4-defaults-and-functions/starter.py' | relative_url }}), test file `test_a4_defaults_and_functions.py` in the same folder.

```python
{% include_relative assignments/a4-defaults-and-functions/starter.py %}
```

Run: `uv run pytest modules/09-functions/assignments/a4-defaults-and-functions`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-defaults-and-functions/solution.py %}
```

`add_item` uses `None` as the default and creates a fresh list inside. `compose` returns an inner function that remembers `funcs`. `make_counter` keeps `current` in the enclosing scope and rebinds it with `nonlocal`, so every counter has its own state.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="09-functions:assignments"> I have finished the assignments</label></li>
</ul>
