---
layout: module
module: 17-debugging
kind: learn
title: Debugging
permalink: /modules/17-debugging/
---

<div class="box key" markdown="1">

## Key learning points

- Read a **traceback from the bottom**: the last line names the error, and the frame just above it shows where it happened.
- **Reproduce** the bug first. Then shrink the input until the smallest failing case remains.
- `print` is a fine first tool. For more, `breakpoint()` opens **pdb**, where you step through the code and inspect variables.
- Use the **`logging`** module instead of `print` for messages that should stay in the program, with levels such as `DEBUG`, `INFO` and `ERROR`.
- `assert` states something that must be true, so a wrong assumption fails loudly and early.
- Most bugs belong to a small number of families: off-by-one, mutable default, shadowed names and integer versus float division.

</div>

## 1. Reading a traceback

```python
def average(numbers):
    return sum(numbers) / len(numbers)

def report(groups):
    for name, nums in groups.items():
        print(name, average(nums))

report({"a": [1, 2, 3], "b": []})
```

```text
a 2.0
Traceback (most recent call last):
  File "/tmp/c/tb.py", line 8, in <module>
    report({"a": [1, 2, 3], "b": []})
  File "/tmp/c/tb.py", line 6, in report
    print(name, average(nums))
                ^^^^^^^^^^^^^
  File "/tmp/c/tb.py", line 2, in average
    return sum(numbers) / len(numbers)
           ~~~~~~~~~~~~~^~~~~~~~~~~~~~~~
ZeroDivisionError: division by zero
```

(The markers under the code differ slightly between Python versions.)

1. **Last line:** the exception type and message. It tells you *what* went wrong: division by zero.
2. **The frame above it:** `line 2, in average` is *where* it failed.
3. **The frames above that** are the chain of calls that led there, oldest first. `report` called `average` with `nums = []`.

The bug is not always in the last frame. Here `average` is correct for non-empty lists. The real question is what to do with an empty group. Start from the last frame and move up until you find the code that made the wrong decision.

## 2. Reproduce, then minimise

1. Make the bug happen every time. Note the exact input.
2. Remove everything that is not needed. If the failing call is `report(big_dict)`, try one key. Then try `average([])` alone.
3. Write that smallest case as a test. Then fix the code and watch the test pass.

If you cannot shrink it by hand, **bisect**: cut the input (or the list of recent code changes) in half, check which half still fails, and repeat. After a few rounds you have the culprit. `git bisect` does this for commits.

## 3. Print debugging

```python
def total(prices):
    result = 0
    for p in prices:
        print("p =", p, "result =", result)   # temporary
        result += p
    return result
```

Print the values you are unsure about, and print them with a label. `print(f"{p=}")` writes `p=3` for you. Remove the prints when you are done. For anything that should stay, use logging (section 5).

## 4. The debugger: breakpoint() and pdb

`breakpoint()` stops the program and opens `pdb`, Python's built-in debugger:

```python
def total(prices):
    result = 0
    for p in prices:
        result += p
    return result

breakpoint()
print(total([3, 4, 5]))
```

A short session (you type what comes after `(Pdb)`):

```text
> /tmp/c/pd.py(8)<module>()
-> print(total([3, 4, 5]))
(Pdb) s
--Call--
> /tmp/c/pd.py(1)total()
-> def total(prices):
(Pdb) n
> /tmp/c/pd.py(2)total()
-> result = 0
(Pdb) p prices
[3, 4, 5]
(Pdb) n
> /tmp/c/pd.py(3)total()
-> for p in prices:
(Pdb) n
> /tmp/c/pd.py(4)total()
-> result += p
(Pdb) n
> /tmp/c/pd.py(3)total()
-> for p in prices:
(Pdb) p result
3
(Pdb) c
```

| Command | Meaning |
|---|---|
| `n` (next) | run the current line, stay in this function |
| `s` (step) | step *into* a function call |
| `c` (continue) | run until the next breakpoint or the end |
| `p expr` | print the value of an expression |
| `l` (list) | show the source around the current line |
| `w` (where) | show the call stack |
| `q` (quit) | stop the program |

You can also run a whole script under the debugger with `python -m pdb script.py`. To stop when a crash happens, use `python -m pdb -c continue script.py`: pdb opens at the failing line. Editors such as VS Code offer the same tools with a click (breakpoints, step buttons, a variables panel).

The environment variable `PYTHONBREAKPOINT=0` turns every `breakpoint()` call off. Remove the calls before you commit.

## 5. Logging basics

`logging` gives you levels, timestamps and a single place to switch output on or off:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("shop")

def checkout(items):
    log.debug("items=%s", items)             # hidden at INFO level
    log.info("checking out %d items", len(items))
    try:
        1 / 0
    except ZeroDivisionError:
        log.exception("failed")              # ERROR plus the traceback

checkout(["a", "b"])
```

```text
18:37:41 INFO shop: checking out 2 items
18:37:41 ERROR shop: failed
Traceback (most recent call last):
  File "/tmp/c/lg.py", line 16, in checkout
    1 / 0
    ~~^~~
ZeroDivisionError: division by zero
```

(Your time and file path will differ.) The levels, from least to most serious, are `DEBUG`, `INFO`, `WARNING`, `ERROR` and `CRITICAL`. A logger only shows messages at or above its level. Pass values as arguments (`log.info("got %d", n)`) rather than building the string first. Call `basicConfig` once, in your main program, not in library code. Use `log.exception` inside an `except` block to record the traceback.

## 6. assert and the traceback module

`assert` documents an assumption and fails at once if it is false:

```python
x = 1
assert x == 2, "x should be 2"
```

```text
AssertionError: x should be 2
```

Use `assert` for conditions that can only be false because of a bug. Do not use it to validate user input. Python can run with assertions switched off (`python -O`).

The `traceback` module lets your program inspect an error:

```python
import traceback

def f():
    return 1 / 0

try:
    f()
except ZeroDivisionError as exc:
    last = traceback.extract_tb(exc.__traceback__)[-1]
    print(last.name, last.lineno, last.line)
    print(traceback.format_exception_only(exc)[0].strip())
```

```text
f 4 return 1 / 0
ZeroDivisionError: division by zero
```

## 7. Common bug families

```python
def add_item(item, items=[]):          # mutable default: one list for all calls
    items.append(item)
    return items

print(add_item(1), add_item(2))        # [1, 2] [1, 2]

rows = [[0] * 2] * 2                   # the same inner list twice
rows[0][0] = 9
print(rows)                            # [[9, 0], [9, 0]]

list = [1, 2]                          # shadows the built-in name
# list(range(3))  -> TypeError: 'list' object is not callable

print(7 / 2, 7 // 2)                   # 3.5 3  (true vs floor division)
```

```text
[1, 2] [1, 2]
[[9, 0], [9, 0]]
3.5 3
```

Another family is the **off-by-one** error. `range(1, len(nums))` skips the first item, and `nums[len(nums)]` is past the end. Print the first and last index you expect to see.

## 8. A routine for stubborn bugs

1. State what you **expected** and what **happened**.
2. Reproduce and shrink the case.
3. Form one **hypothesis**, then test it with a print, a log line or the debugger. Do not change code at random.
4. Change **one thing** at a time.
5. Explain the problem aloud, to a colleague or a rubber duck. Putting it in words often reveals the wrong assumption.
6. Add a test so the bug cannot return.

<div class="box warn" markdown="1">

## Common mistakes

- **Reading the first traceback line only.** The useful facts are the error on the last line and the frames just above it.
- **Changing code before understanding the bug.** Guesses hide the problem or add new ones.
- **Leaving `print` or `breakpoint()` in finished code.** Use logging for permanent messages.
- **Catching an exception just to silence it.** `except Exception: pass` hides the very traceback you need.
- **Naming a variable `list`, `str`, `max` or `id`.** The built-in disappears in that scope.

</div>

## Try it yourself

1. Write `def average(numbers)`, call it with `[]`, and read the traceback aloud. Then decide what it should do for an empty list.
2. Put `breakpoint()` inside a loop and use `n`, `p` and `c` to follow a counter.
3. Configure `logging` so a function writes an INFO line at start and an ERROR with traceback when it fails.

## Further reading

- [`pdb`](https://docs.python.org/3/library/pdb.html)
- [`logging`](https://docs.python.org/3/library/logging.html)
- [`traceback`](https://docs.python.org/3/library/traceback.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="17-debugging:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/17-debugging/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/17-debugging/assignments/' | relative_url }}).
