---
layout: module
module: 10-files-and-paths
kind: assignments
title: "Files and paths - assignments"
permalink: /modules/10-files-and-paths/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Assignments 1 and 4 use data files that sit in their assignment folders (`sample.txt` and the `notes/` folder). The other tests create their files in temporary folders, so nothing outside the repository is touched.

Run all tests for this topic:

```bash
uv run pytest modules/10-files-and-paths
```

---

<div class="assignment" markdown="1">

## Assignment 1: Text file statistics

**Goal:** Count the lines, words and characters of a file and find its longest line. Practises `with open(...)`, iterating over lines, `read_text` and UTF-8.

**Files:** [`starter.py`]({{ 'modules/10-files-and-paths/assignments/a1-text-stats/starter.py' | relative_url }}), test file `test_a1_text_stats.py` in the same folder. The data file `sample.txt` is in the same folder.

```python
{% include_relative assignments/a1-text-stats/starter.py %}
```

Run: `uv run pytest modules/10-files-and-paths/assignments/a1-text-stats`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-text-stats/solution.py %}
```

Iterating over the file reads one line at a time, so `count_lines` works for huge files. `count_chars` counts **characters** of the decoded text, so `Café` is 4 even though it uses 5 bytes. `max(lines, key=len, default="")` returns the first longest line and handles an empty file.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Read and write text files

**Goal:** Read non-blank lines, write a formatted report, append to a log, copy a file in upper case and read the last lines. Practises the modes `"r"`, `"w"` and `"a"`.

**Files:** [`starter.py`]({{ 'modules/10-files-and-paths/assignments/a2-read-and-write/starter.py' | relative_url }}), test file `test_a2_read_and_write.py` in the same folder.

```python
{% include_relative assignments/a2-read-and-write/starter.py %}
```

Run: `uv run pytest modules/10-files-and-paths/assignments/a2-read-and-write`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-read-and-write/solution.py %}
```

`"w"` replaces the file and `"a"` keeps the old content and adds to the end. `copy_uppercase` opens both files in a single `with` statement and processes one line at a time. `tail` slices the list of lines with `lines[-n:]`, after handling `n <= 0`, because `lines[-0:]` would return everything.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Folder tools with pathlib

**Goal:** Find files by suffix, count them, find the largest file, create a folder tree and rename suffixes. Practises `Path`, `rglob`, `iterdir`, `mkdir(parents=True, exist_ok=True)` and `stat().st_size`.

**Files:** [`starter.py`]({{ 'modules/10-files-and-paths/assignments/a3-folder-tools/starter.py' | relative_url }}), test file `test_a3_folder_tools.py` in the same folder.

```python
{% include_relative assignments/a3-folder-tools/starter.py %}
```

Run: `uv run pytest modules/10-files-and-paths/assignments/a3-folder-tools`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-folder-tools/solution.py %}
```

`rglob("*")` walks all subfolders, and `is_file()` skips directories. `relative_to(folder).as_posix()` gives portable relative names. `mkdir(parents=True, exist_ok=True)` creates all missing parents without an error if the folder exists. `max` with a key on a name-sorted list picks the first name on ties.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Merge and search notes

**Goal:** Merge several note files into one, search them for a word with line numbers, number the lines of a file and read a file safely. Practises `glob`, `enumerate(f, start=1)` and catching `FileNotFoundError`.

**Files:** [`starter.py`]({{ 'modules/10-files-and-paths/assignments/a4-merge-and-search/starter.py' | relative_url }}), test file `test_a4_merge_and_search.py` in the same folder. The `notes/` folder with small text files is in the same folder.

```python
{% include_relative assignments/a4-merge-and-search/starter.py %}
```

Run: `uv run pytest modules/10-files-and-paths/assignments/a4-merge-and-search`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-merge-and-search/solution.py %}
```

`Path.glob("*.txt")` finds the notes and `sorted` gives a fixed order. `merge_notes` writes a header per note and makes sure each line ends with a newline. `search` uses `enumerate(f, start=1)` for line numbers. `safe_read` catches only `FileNotFoundError`, so other problems still show up.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="10-files-and-paths:assignments"> I have finished the assignments</label></li>
</ul>
