---
layout: module
module: 01-getting-started
kind: learn
title: Getting started
permalink: /modules/01-getting-started/
---

<div class="box key" markdown="1">

## Key learning points

- Python is an **interpreter**: it reads your file from top to bottom and runs each line.
- Use **uv** to install Python and run your code. Check the version with `uv run python --version`.
- There are three ways to run code: the **REPL** (`python`), a **script** (`uv run hello.py`) and a **one-liner** (`python -c "..."`).
- `print()` shows values. `#` starts a comment.
- A **traceback** is read from the bottom: the last line says what went wrong.
- Four terminal commands cover most needs: `pwd`, `ls`, `cd`, `mkdir`.

</div>

## 1. Install Python with uv

`uv` is a fast tool that installs Python versions, creates project environments and runs your code.

macOS and Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Open a new terminal, then install a current Python and check it:

```bash
uv python install 3.14
uv run --python 3.14 python --version
```

You should see `Python 3.14.x` (or newer).

## 2. Terminal in five minutes

You will type commands into a terminal (Terminal on macOS, a shell on Linux, PowerShell on Windows). These four work in all of them.

| Command | What it does |
|---|---|
| `pwd` | Print the folder you are in |
| `ls` | List what is in this folder |
| `cd name` | Move into folder `name` (`cd ..` goes up) |
| `mkdir name` | Make a new folder |

```bash
mkdir python-practice
cd python-practice
pwd
```

Use the Up arrow to repeat a command and Tab to complete a name.

## 3. Your first project

```bash
uv init hello-python
cd hello-python
ls
```

`uv init` creates `main.py`, `pyproject.toml` (project settings) and `.python-version` (the Python version to use). Run the sample script:

```bash
uv run main.py
```

Now replace the contents of `main.py` with:

```python
# My first program
name = "Ada"
print("Hello,", name)
print(2 + 3, "is two plus three")
```

Run it again. Python executes the lines in order, so `name` must be defined before `print` uses it.

## 4. The REPL and one-liners

Type `python` (or `uv run python`) with no file name to open the **REPL**. Each line runs as soon as you press Enter, which makes it good for experiments.

```python
>>> 6 * 7
42
>>> "py" * 3
'pypypy'
>>> exit()
```

To leave the REPL, type `exit()`, press Ctrl-D (macOS, Linux) or press Ctrl-Z then Enter (Windows). Since Python 3.13 the REPL supports multi-line editing and colour, and Python 3.14 adds syntax highlighting.

For a quick check without a file:

```bash
python -c "print(1 + 1)"
```

## 5. Reading an error

```python
print("Total:", totl)
```

```text
Traceback (most recent call last):
  File "main.py", line 1, in <module>
    print("Total:", totl)
NameError: name 'totl' is not defined
```

1. Read the **last line** first: the type (`NameError`) and the message.
2. Read the line above it: the file, line number and code that failed.
3. Fix, save, run again. Typos in names are the most common cause at the start.

A `SyntaxError` means the code is not valid Python (for example a missing `)`). A `NameError` means the code is valid, but a name does not exist when that line runs.

<div class="box warn" markdown="1">

## Common mistakes

- **Naming your file after a module.** A script called `random.py` or `json.py` hides the standard library module of the same name.
- **Running the wrong folder.** If `uv run main.py` says the file is not found, run `pwd` and `ls` to see where you are.
- **Mixing tabs and spaces, or curly quotes.** Type code in a code editor, not a word processor.
- **Forgetting that Python runs top to bottom.** Define a name before you use it.

</div>

## Try it yourself

1. Change `name` in `main.py` and run it again.
2. Add a line `print("Python version check")` and a comment above it that explains why.
3. Break the program on purpose (misspell `print`) and read the traceback.

## Where this comes from

*Introducing Python*, chapter 1 (Introduction) and chapter 13 (Development environment). *Learn Python the Hard Way*, exercises 0 to 8 (setup, first program, comments, terminal).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="01-getting-started:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/01-getting-started/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/01-getting-started/assignments/' | relative_url }}).
