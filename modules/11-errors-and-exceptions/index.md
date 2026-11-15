---
layout: module
module: 11-errors-and-exceptions
kind: learn
title: Errors and exceptions
permalink: /modules/11-errors-and-exceptions/
---

<div class="box key" markdown="1">

## Key learning points

- An **exception** is an object that Python raises when something goes wrong. If nothing catches it, the program stops and prints a traceback.
- `try` / `except` catches **specific** exception types. `else` runs when no error happened. `finally` always runs.
- Use `raise` to signal a problem yourself, and `raise NewError(...) from original` to keep the cause.
- Define your own exception by subclassing `Exception` (or a more specific class such as `ValueError`).
- Never write a bare `except:`. It also hides `KeyboardInterrupt` and real bugs.
- Python style prefers **EAFP** ("easier to ask forgiveness than permission"): try the operation, and handle the failure.

</div>

## 1. Common exceptions

```python
int("abc")             # ValueError: invalid literal for int() with base 10: 'abc'
[1, 2][5]              # IndexError: list index out of range
{"a": 1}["b"]          # KeyError: 'b'
1 / 0                  # ZeroDivisionError: division by zero
"a" + 1                # TypeError: can only concatenate str (not "int") to str
open("nofile.txt")     # FileNotFoundError: [Errno 2] No such file or directory: 'nofile.txt'
None.upper()           # AttributeError: 'NoneType' object has no attribute 'upper'
```

A `NameError` means you used a name that does not exist, often from a typo. Exceptions form a family tree: `KeyError` and `IndexError` are both `LookupError`, `ZeroDivisionError` is an `ArithmeticError`, and `FileNotFoundError` is an `OSError`. Catching a parent class also catches its children.

## 2. try, except, else, finally

```python
def parse(text):
    try:
        n = int(text)
    except ValueError:
        print("not a number")
        return None
    else:
        print("parsed")
        return n
    finally:
        print("done")

print(parse("5"))
print(parse("x"))
```

```text
parsed
done
5
not a number
done
None
```

- `try`: the code that might fail. Keep it short.
- `except ValueError`: runs only for that exception type.
- `else`: runs when the `try` block raised nothing.
- `finally`: runs **always**, even after a `return`. Use it for cleanup.

Catch several types with a tuple, and name the error with `as`:

```python
try:
    int("x")
except (ValueError, TypeError) as e:
    print("caught", e)      # caught invalid literal for int() with base 10: 'x'
```

Only catch what you know how to handle. If you only want to log an error and let it go on, use a bare `raise` inside the `except` block to re-raise it.

## 3. Raising exceptions

```python
def set_age(age):
    if age < 0:
        raise ValueError(f"age must be >= 0, got {age}")
    return age
```

`ValueError` fits a right type with a wrong value. `TypeError` fits a wrong type. Put the facts in the message: what was wrong and which value.

`assert condition, "message"` raises `AssertionError` when the condition is false. Use it for checks of your own assumptions while developing, not to validate user input, because assertions can be switched off with `python -O`.

## 4. Custom exceptions and chaining

```python
class AppError(Exception):
    """Base class for errors of this program."""

class NotFound(AppError):
    def __init__(self, name):
        super().__init__(f"{name} not found")
        self.name = name

try:
    raise NotFound("bob")
except AppError as e:
    print(type(e).__name__, e, e.name)    # NotFound bob not found bob
```

A base class for your package lets callers catch all your errors with one `except AppError`.

When you translate a low-level error into your own, chain it with `from`:

```python
def load(text):
    try:
        return int(text)
    except ValueError as exc:
        raise AppError(f"bad value {text!r}") from exc
```

The new exception keeps the original in its `__cause__` attribute, and the traceback shows both.

## 5. EAFP and LBYL

```python
# LBYL: look before you leap
if key in data:
    value = data[key]
else:
    value = None

# EAFP: try it, and handle the failure
try:
    value = data[key]
except KeyError:
    value = None
```

(For this particular case, `data.get(key)` is shortest.) EAFP is usually safer when the situation can change between the check and the use, for example a file that is deleted after you checked that it exists.

Several errors at once, for example from many concurrent tasks, are grouped in an `ExceptionGroup` and caught with `except*`. That is covered in the topic on task groups.

<div class="box warn" markdown="1">

## Common mistakes

- **A bare `except:` or `except Exception: pass`.** It hides bugs and makes failures silent. Catch the specific type, and at least log what happened.
- **A huge `try` block.** If ten lines are inside, you cannot tell which one failed. Wrap only the risky line.
- **Losing the original error.** Use `raise NewError(...) from exc` when you replace an exception.
- **Using exceptions for normal flow when a simple test is clearer.** `if not items:` is better than catching `IndexError` for an empty list.
- **Catching an exception and returning a made-up value that hides the problem.** Return a clear default only when the caller expects it.

</div>

## Try it yourself

1. Ask for a number with `input()` in a loop until the user types a valid integer. Catch `ValueError`.
2. Write `read_first_line(path)` that returns `None` if the file does not exist, and lets other errors through.
3. Define `class TooYoung(ValueError)` and raise it from a function when `age < 18`. Catch it with `except ValueError`. Does that work? Why?

## Where this comes from

This topic goes beyond the chapter list of the two reference books, so see the Python docs: the [tutorial on errors and exceptions](https://docs.python.org/3/tutorial/errors.html) and the [built-in exceptions](https://docs.python.org/3/library/exceptions.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="11-errors-and-exceptions:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/11-errors-and-exceptions/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/11-errors-and-exceptions/assignments/' | relative_url }}).
