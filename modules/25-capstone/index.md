---
layout: module
module: 25-capstone
kind: learn
title: "Basic capstone: expense tracker"
permalink: /modules/25-capstone/
---

<div class="box key" markdown="1">

## Key learning points

- A project is easier when it is split into **layers**: parsing, storage, reporting and the command-line interface. Each layer does one job and can be tested alone.
- **Dataclasses** give the layers one shared, typed record: `Expense`.
- Money uses `Decimal` (or whole cents), never `float`.
- Functions take parameters and return values. Only the outer layer calls `print` or reads `sys.argv`. This is what makes tests easy.
- `main(argv)` returns an **exit code**, so a test can call it like any other function.
- Build in **stages**. After each stage the tests pass, and you have a working program.

</div>

## 1. The project

You will build `expenses`, a small command-line tracker:

```text
$ expenses add 2024-03-01 food 45.50 -d "Groceries"
Added #1: 2024-03-01 food 45.50
$ expenses list --month 2024-03
2024-03-01  food            45.50  Groceries
$ expenses report 2024-03
Expenses for 2024-03
Category     Count       Total
------------------------------
food             1       45.50
------------------------------
TOTAL            1       45.50
```

The assignments for this topic build the program one stage at a time. Each stage is a separate folder with its own tests, and it repeats the small pieces it needs (such as the `Expense` class). That way you can do any stage without having finished the earlier one. In your own project you would keep one copy of each piece and import it.

| Stage | Layer | What you write |
|---|---|---|
| 1 | Parsing | Read `expenses.csv` into `Expense` objects and collect errors |
| 2 | Storage | An SQLite repository: add, list, totals by category |
| 3 | Reporting | A text table for one month |
| 4 | Interface | `argparse` commands that connect the layers |
| 5 | Stretch | Export to JSON and import it back |

## 2. Design: layers and data flow

```text
CSV file --parse--> Expense objects --store--> SQLite
                                                  |
 terminal <--print-- text report <--format-- Expense objects
```

The rules that keep the layers apart:

- The **parsing** layer knows about CSV and validation. It does not know about SQLite.
- The **storage** layer knows SQL. It receives and returns `Expense` objects, never raw rows.
- The **reporting** layer takes a list of `Expense` objects and returns a `str`. It does no input or output.
- The **CLI** layer reads arguments, calls the other layers and prints.

A suggested layout for your own copy of the project:

```text
expenses/
  pyproject.toml
  src/expenses/
    __init__.py
    models.py      # Expense dataclass
    parsing.py     # CSV -> Expense
    storage.py     # ExpenseRepository (SQLite)
    report.py      # format_report
    cli.py         # build_parser, main
  tests/
    test_parsing.py
    test_storage.py
    test_report.py
    test_cli.py
```

## 3. The record: a frozen dataclass

```python
from dataclasses import dataclass
from datetime import date
from decimal import Decimal


@dataclass(frozen=True)
class Expense:
    date: date
    category: str
    description: str
    amount: Decimal
```

`frozen=True` makes instances read-only, and the dataclass writes `__init__`, `__repr__` and `__eq__` for you. Equal fields mean equal objects, which makes test assertions short.

Why `Decimal`? Floats cannot store most decimal fractions exactly:

```python
print(0.1 + 0.1 + 0.1)          # 0.30000000000000004
print(Decimal("0.10") * 3)      # 0.30
```

Always build a `Decimal` from a **string** (`Decimal("0.10")`), not from a float.

## 4. Parsing with error collection

A real file has bad rows. Stop on the first one and the user must fix the file again and again. Instead, record each error with its line number and continue.

```python
import csv
import io

text = "date,category,description,amount\n2024-03-01,food,Lunch,12.25\n2024-03-02,food,Tea,abc\n"
reader = csv.DictReader(io.StringIO(text))
for row in reader:
    print(reader.line_num, row)
```

```text
2 {'date': '2024-03-01', 'category': 'food', 'description': 'Lunch', 'amount': '12.25'}
3 {'date': '2024-03-02', 'category': 'food', 'description': 'Tea', 'amount': 'abc'}
```

`reader.line_num` is the line of the file, which is what a user needs in an error message. The pattern is: validate one row in a function that raises `ValueError`, then catch it in the loop and append `f"line {n}: {message}"` to a list of errors. Beware that `Decimal("abc")` raises `decimal.InvalidOperation`, which is not a `ValueError`.

## 5. Storing money in SQLite

SQLite has no decimal type. Store whole **cents** as an `INTEGER`, and convert at the edges. Always pass values as `?` parameters, never by building SQL text with f-strings.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE expenses (id INTEGER PRIMARY KEY, day TEXT, cents INTEGER)")
with conn:   # commits on success, rolls back on error
    conn.execute(
        "INSERT INTO expenses (day, cents) VALUES (?, ?)",
        ("2024-03-01", int(Decimal("45.50") * 100)),
    )
print(conn.execute("SELECT SUM(cents) FROM expenses").fetchone()[0])   # 4550
```

Dates go in as ISO text (`"2024-03-01"`). That text sorts correctly, and `substr(day, 1, 7)` gives the month.

## 6. A command-line interface that can be tested

```python
import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="expenses")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("amount")
    args = parser.parse_args(argv)
    print("would add", args.amount)
    return 0


print(main(["add", "5.00"]))   # prints "would add 5.00", then 0
```

Pass `argv` as a list and return the exit code. At the bottom of the file, `sys.exit(main())` turns the code into the process status. Errors go to `sys.stderr`, normal output to `sys.stdout`. By convention `0` means success, `1` means a failure the program reports, and `2` means a usage error (`argparse` exits with `2` itself).

## 7. Testing as you go

Write a test for each function as soon as it works. Use `tmp_path` for database files and `capsys` to check printed output. The test files in this topic show the patterns. Run them with:

```bash
uv run pytest modules/25-capstone
```

<div class="box warn" markdown="1">

## Common mistakes

- **Using `float` for money.** Totals drift by fractions of a cent. Use `Decimal` or integer cents.
- **Building SQL with f-strings.** A description such as `x'); DROP TABLE expenses; --` then becomes SQL. Use `?` parameters.
- **Stopping at the first bad row.** Collect the errors, keep the good rows and report both.
- **Printing inside the logic layers.** A function that prints cannot be reused or tested easily. Return values and print only in `main`.
- **Calling `sys.exit` inside `main`.** Return the code instead. Only the `if __name__ == "__main__":` block exits.

</div>

## Try it yourself

1. Sketch on paper the functions each layer needs for a new command, `delete ID`. Which layers change?
2. Add a `--category` filter to `list`. Which layer does the filtering?
3. Write a test that adds the same expense twice and checks that `report` shows a count of 2.

## Where this comes from

This project combines ideas from earlier topics. *Introducing Python*, chapter 20 (Files), chapter 23 (Data in a Box: Persistent Storage), chapter 11 (Objects) and chapter 15 (Testing). *Learn Python the Hard Way*, exercise 46 (project skeleton), exercise 47 (automated testing) and exercises 40 to 44 (classes). For `dataclasses` see the [Python docs](https://docs.python.org/3/library/dataclasses.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="25-capstone:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/25-capstone/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/25-capstone/assignments/' | relative_url }}).
