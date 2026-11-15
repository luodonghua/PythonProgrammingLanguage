---
layout: module
module: 03-strings
kind: assignments
title: Strings and formatting - assignments
permalink: /modules/03-strings/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/03-strings
```

---

<div class="assignment" markdown="1">

## Assignment 1: Palindromes and word tools

**Goal:** Check palindromes while ignoring punctuation, fix the capitalisation of a title, and count words. Practises slicing, `split`, `join` and string methods.

**Files:** [`starter.py`]({{ 'modules/03-strings/assignments/a1-palindrome/starter.py' | relative_url }}), test file `test_a1_palindrome.py` in the same folder.

```python
{% include_relative assignments/a1-palindrome/starter.py %}
```

Run: `uv run pytest modules/03-strings/assignments/a1-palindrome`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-palindrome/solution.py %}
```

`text[::-1]` reverses a string. Keeping only `isalnum()` characters in lower case makes the comparison ignore spaces and punctuation. `str.split()` with no argument splits on any run of whitespace, which is why `title_case` needs no extra clean-up.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Slugify

**Goal:** Turn titles into URL-friendly slugs, make them unique, and shorten long text. Practises loops over characters, `strip`, `while` and slicing.

**Files:** [`starter.py`]({{ 'modules/03-strings/assignments/a2-slugify/starter.py' | relative_url }}), test file `test_a2_slugify.py` in the same folder.

```python
{% include_relative assignments/a2-slugify/starter.py %}
```

Run: `uv run pytest modules/03-strings/assignments/a2-slugify`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-slugify/solution.py %}
```

Each character is either kept or replaced by a single hyphen, and a hyphen is added only if the last piece is not already one. `strip("-")` removes hyphens at both ends. `truncate` cuts to `width - len(suffix)` so the result including the suffix fits in `width`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Caesar cipher

**Goal:** Shift letters by a fixed amount, undo the shift, and crack a message with a known word. Practises `ord`, `chr`, `%` and string joining.

**Files:** [`starter.py`]({{ 'modules/03-strings/assignments/a3-caesar/starter.py' | relative_url }}), test file `test_a3_caesar.py` in the same folder.

```python
{% include_relative assignments/a3-caesar/starter.py %}
```

Run: `uv run pytest modules/03-strings/assignments/a3-caesar`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-caesar/solution.py %}
```

`(ord(char) - base + shift) % 26` maps a letter to a position from 0 to 25, wraps around the alphabet (also for negative shifts, because `%` returns a non-negative number here) and `+ base` turns it back into a character. Decrypting is encrypting with the negative shift.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Receipt formatter

**Goal:** Print a receipt where every column lines up. Practises f-string width, alignment, precision and thousands separators.

**Files:** [`starter.py`]({{ 'modules/03-strings/assignments/a4-receipt/starter.py' | relative_url }}), test file `test_a4_receipt.py` in the same folder.

```python
{% include_relative assignments/a4-receipt/starter.py %}
```

Run: `uv run pytest modules/03-strings/assignments/a4-receipt`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-receipt/solution.py %}
```

The spec `<14`, `>3` and `>13,.2f` fixes each column width, so every line has the same length. A nested field such as `{title:^{WIDTH}}` takes the width from a variable.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="03-strings:assignments"> I have finished the assignments</label></li>
</ul>
