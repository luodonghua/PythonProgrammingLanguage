---
layout: module
module: 04-input-and-arguments
kind: learn
title: Input and command-line arguments
permalink: /modules/04-input-and-arguments/
---

<div class="box key" markdown="1">

## Key learning points

- `input()` shows a prompt, waits for a line and **always returns a `str`**. Convert it yourself with `int()` or `float()`.
- Check user input. Catch `ValueError` and **ask again** in a loop.
- `sys.argv` is the raw list of command-line words. `sys.argv[0]` is the script name.
- `argparse` parses arguments for you: positional arguments, `--options`, flags, defaults, types and a free `--help`.
- Normal output goes to **stdout**. Errors go to **stderr**. The **exit code** tells other programs whether you succeeded (`0`) or failed (non-zero).
- Write functions that take parameters, and a `main(argv)` function. Then you can test them without a keyboard.

</div>

## 1. input() returns text

```python
age = input("Age: ")
print(type(age), age + "1")
print(int(age) + 1)
```

If the user types `41`, the output is:

```text
Age: <class 'str'> 411
42
```

`age + "1"` joins two strings, so you get `"411"`. Convert first with `int(age)` to do arithmetic.

## 2. Validate and retry

`int("abc")` raises `ValueError`. Catch it and ask again:

```python
def read_int(prompt: str) -> int:
    while True:
        text = input(prompt)
        try:
            return int(text)
        except ValueError:
            print("Please type a whole number.")
```

`return` leaves the loop as soon as the conversion works. Also decide what a valid value is. A number can parse and still be wrong (an age of `-5`), so add a range check inside the loop.

## 3. Make input replaceable

A function that calls `input()` directly is hard to test. Pass the input function as a **parameter** with `input` as the default:

```python
def read_int(prompt: str, input_fn=input) -> int:
    while True:
        try:
            return int(input_fn(prompt))
        except ValueError:
            print("Please type a whole number.")


answers = iter(["x", "", "7"])
print(read_int("n: ", lambda prompt: next(answers)))
```

```text
Please type a whole number.
Please type a whole number.
7
```

The fake `input_fn` returns the scripted answers `"x"`, `""` and `"7"`, so no one has to type. Tests do the same.

If a function calls `input()` directly, a test can instead replace it with `monkeypatch.setattr("builtins.input", fake)`. That does not work for a default like `input_fn=input`, because Python evaluates the default once, when the function is defined. Pass the fake in as an argument.

## 4. sys.argv

Everything after `python script.py` becomes a string in `sys.argv`:

```python
import sys
print(sys.argv)
```

Running `python argv.py a "b c" 3` prints:

```text
['argv.py', 'a', 'b c', '3']
```

Quotes keep `b c` together as one argument. `sys.argv` works for tiny scripts. For anything else, use `argparse`.

## 5. argparse

```python
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Greet someone.")
    parser.add_argument("name", help="who to greet")
    parser.add_argument("--times", type=int, default=1, help="repeat count")
    parser.add_argument("--shout", action="store_true", help="use capitals")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = f"Hello, {args.name}!"
    if args.shout:
        text = text.upper()
    for _ in range(args.times):
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- `name` is **positional** and required.
- `--times` is an **option** with a value. `type=int` converts the text and `default=1` is used when it is missing.
- `--shout` is a **flag**. `action="store_true"` makes it `True` when present and `False` otherwise.
- `parse_args(None)` reads `sys.argv`. `parse_args(["Ada"])` reads the list you give it, which is ideal for tests.

```text
$ python greet.py Ada --times 2 --shout
HELLO, ADA!
HELLO, ADA!
```

`argparse` also builds `--help` and checks the input. A missing argument or a bad number prints a usage message to stderr and exits with code 2:

```text
$ python greet.py Ada --times x
usage: greet.py [-h] [--times TIMES] [--shout] name
greet.py: error: argument --times: invalid int value: 'x'
```

## 6. stdout, stderr and exit codes

```python
import sys

print("result")                       # stdout: the program's output
print("problem", file=sys.stderr)     # stderr: messages about errors
sys.exit(2)                           # exit code 2 = failure
```

With `python err.py 2>/dev/null` only `result` appears, because `2>` redirects stderr. By convention, exit code `0` means success and anything else means failure. Shells and CI systems read this code.

## 7. Design for testability

Keep the parts separate:

1. **Pure functions** that take values and return values (`parse_amount(text)`).
2. **`main(argv)`** that parses arguments, calls the functions, prints, and returns an exit code.
3. `raise SystemExit(main())` under `if __name__ == "__main__":`.

A test then calls `main(["Ada", "--shout"])` and checks the return value and the captured output. It never needs a real terminal.

<div class="box warn" markdown="1">

## Common mistakes

- **Forgetting that `input()` returns text.** `input() + 1` is a `TypeError`, and `"5" > "10"` is `True` because strings compare character by character.
- **Using `sys.argv[1]` without a check.** With no arguments it raises `IndexError`.
- **`type=bool` in argparse.** `bool("False")` is `True`. Use `action="store_true"` for flags.
- **Calling `input()` deep inside logic.** The code can no longer be tested without a keyboard. Pass values in.
- **Printing errors to stdout.** Use `file=sys.stderr` so users can separate output from errors.

</div>

## Try it yourself

1. Write `read_float(prompt)` that asks again until the user types a number.
2. Write a script `add.py` that uses `argparse` to take two numbers and print their sum. Add a `--round` option with `type=int`.
3. Make your script from exercise 2 print an error to stderr and exit with code 1 when a number is negative.

## Further reading

- [argparse tutorial](https://docs.python.org/3/howto/argparse.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="04-input-and-arguments:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/04-input-and-arguments/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/04-input-and-arguments/assignments/' | relative_url }}).
