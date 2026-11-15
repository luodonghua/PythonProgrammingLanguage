---
layout: module
module: 04-input-and-arguments
kind: assignments
title: Input and command-line arguments - assignments
permalink: /modules/04-input-and-arguments/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/04-input-and-arguments
```

---

<div class="assignment" markdown="1">

## Assignment 1: Read numbers safely

**Goal:** Write `read_int` and `read_yes_no`, which keep asking until the answer is valid. Practises `input()`, `int()`, `try`/`except ValueError`, loops and passing `input_fn` as a parameter.

**Files:** [`starter.py`]({{ 'modules/04-input-and-arguments/assignments/a1-read-number/starter.py' | relative_url }}), test file `test_a1_read_number.py` in the same folder.

```python
{% include_relative assignments/a1-read-number/starter.py %}
```

Run: `uv run pytest modules/04-input-and-arguments/assignments/a1-read-number`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-read-number/solution.py %}
```

`input_fn=input` is a default parameter, so real programs get the keyboard and tests pass a scripted function. The `tries` counter stops the loop when `max_tries` is reached, and `return None` tells the caller that the user gave up.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: A greeter with argparse

**Goal:** Build a command-line greeter with a positional name, `--times`, `--shout` and `--greeting`. Practises `argparse`, `main(argv)`, stdout, stderr and exit codes.

**Files:** [`starter.py`]({{ 'modules/04-input-and-arguments/assignments/a2-greeter/starter.py' | relative_url }}), test file `test_a2_greeter.py` in the same folder.

```python
{% include_relative assignments/a2-greeter/starter.py %}
```

Run: `uv run pytest modules/04-input-and-arguments/assignments/a2-greeter`

Try it in a terminal too: `uv run python modules/04-input-and-arguments/assignments/a2-greeter/starter.py Ada --shout`. Add `--help` to see the generated help.

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-greeter/solution.py %}
```

`nargs="+"` collects one or more words into a list. `main` takes `argv` so tests call `main(["Ada", "--shout"])` without a terminal, and returns an exit code instead of calling `sys.exit` itself. Errors that argparse detects (a missing name, `--times x`) exit with code 2.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Mortgage calculator CLI

**Goal:** Compute a loan's monthly payment and wrap it in a command-line tool with validation. Practises `float` and `int` arguments, error handling, f-string formatting and exit codes.

**Files:** [`starter.py`]({{ 'modules/04-input-and-arguments/assignments/a3-mortgage/starter.py' | relative_url }}), test file `test_a3_mortgage.py` in the same folder.

```python
{% include_relative assignments/a3-mortgage/starter.py %}
```

Run: `uv run pytest modules/04-input-and-arguments/assignments/a3-mortgage`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-mortgage/solution.py %}
```

`monthly_payment` is a pure function that is easy to test. `main` catches its `ValueError`, prints the message to stderr and returns 1. The zero-rate case needs its own branch because the formula would divide by zero.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: A to-do menu loop

**Goal:** Write an interactive command loop that reads commands from `input_fn` and writes to `output_fn`. Practises `while True`, `match`, string splitting and testable I/O.

**Files:** [`starter.py`]({{ 'modules/04-input-and-arguments/assignments/a4-menu/starter.py' | relative_url }}), test file `test_a4_menu.py` in the same folder.

```python
{% include_relative assignments/a4-menu/starter.py %}
```

Run: `uv run pytest modules/04-input-and-arguments/assignments/a4-menu`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-menu/solution.py %}
```

Both `input_fn` and `output_fn` are parameters, so a test feeds a list of commands and collects the output in a list. `EOFError` is what `input()` raises when no more input exists, which makes piped input end the program cleanly.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="04-input-and-arguments:assignments"> I have finished the assignments</label></li>
</ul>
