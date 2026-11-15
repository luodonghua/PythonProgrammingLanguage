---
layout: module
module: 06-loops
kind: assignments
title: Loops - assignments
permalink: /modules/06-loops/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/06-loops
```

---

<div class="assignment" markdown="1">

## Assignment 1: Sums, products and digits

**Goal:** Write three small accumulator functions, `sum_of_multiples`, `factorial` and `digit_sum`. Practises `for`, `range`, `break` and building a result in a loop.

**Files:** [`starter.py`]({{ 'modules/06-loops/assignments/a1-multiples/starter.py' | relative_url }}), test file `test_a1_multiples.py` in the same folder.

```python
{% include_relative assignments/a1-multiples/starter.py %}
```

Run: `uv run pytest modules/06-loops/assignments/a1-multiples`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-multiples/solution.py %}
```

Each function follows the same pattern: initialise (`total = 0` or `result = 1`), update inside the loop, return after it. In `sum_of_multiples`, `break` after the first matching divisor stops a number such as 15 from being counted twice.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Text patterns

**Goal:** Return multiplication tables, triangles, pyramids and checkerboards as lists of strings. Practises nested loops and string building.

**Files:** [`starter.py`]({{ 'modules/06-loops/assignments/a2-patterns/starter.py' | relative_url }}), test file `test_a2_patterns.py` in the same folder.

```python
{% include_relative assignments/a2-patterns/starter.py %}
```

Run: `uv run pytest modules/06-loops/assignments/a2-patterns`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-patterns/solution.py %}
```

Returning a list of lines (instead of printing) keeps the logic testable. The checkerboard uses `(row + col) % 2` to alternate, and the pyramid pads each row with `height - row` spaces.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Guessing game logic

**Goal:** Judge guesses, play a game from scripted guesses with a try limit, and count the guesses a binary-search player needs. Practises `for`, `while`, early `return` and slicing.

**Files:** [`starter.py`]({{ 'modules/06-loops/assignments/a3-guessing/starter.py' | relative_url }}), test file `test_a3_guessing.py` in the same folder.

```python
{% include_relative assignments/a3-guessing/starter.py %}
```

Run: `uv run pytest modules/06-loops/assignments/a3-guessing`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-guessing/solution.py %}
```

`guesses[:max_tries]` limits the loop without a counter, and `return` inside the loop stops at the first correct guess. The strategy function halves the range every round, which is why 100 numbers need at most 7 guesses.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Collatz chains and primes

**Goal:** Count Collatz steps, find the start below a limit with the longest chain, and build a sieve of Eratosthenes. Practises `while`, nested loops, lists of booleans and `enumerate`.

**Files:** [`starter.py`]({{ 'modules/06-loops/assignments/a4-collatz-primes/starter.py' | relative_url }}), test file `test_a4_collatz_primes.py` in the same folder.

```python
{% include_relative assignments/a4-collatz-primes/starter.py %}
```

Run: `uv run pytest modules/06-loops/assignments/a4-collatz-primes`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-collatz-primes/solution.py %}
```

The sieve marks multiples of each prime as not prime, starting at `p * p` because smaller multiples were already marked by smaller primes. `enumerate(is_prime)` pairs each number with its flag so a comprehension can collect the primes.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="06-loops:assignments"> I have finished the assignments</label></li>
</ul>
