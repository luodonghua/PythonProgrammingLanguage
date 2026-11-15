---
layout: module
module: 05-conditions-and-match
kind: learn
title: Conditions and match
permalink: /modules/05-conditions-and-match/
---

<div class="box key" markdown="1">

## Key learning points

- `if` / `elif` / `else` runs **the first branch whose condition is true**, and skips the rest.
- Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) give a `bool`. They can be **chained**: `0 <= x < 10`.
- Every value is **truthy or falsy**. Falsy: `False`, `None`, zero, and empty strings and containers.
- `and` / `or` return one of their **operands**, not always `True` or `False`. Use `is None` to test for `None`.
- `match` / `case` (structural pattern matching) compares a value with **shapes**: literals, alternatives with `|`, sequences, mappings, class instances, and guards with `if`.

</div>

## 1. if, elif, else

```python
score = 72

if score >= 90:
    grade = "A"
elif score >= 70:
    grade = "B"
else:
    grade = "C"

print(grade)   # B
```

- The condition ends with a colon and the body is **indented** (four spaces).
- Order matters. `72 >= 70` is true, so `elif score >= 70` runs. Putting `score >= 70` first would also catch every 90.

## 2. Comparisons and boolean logic

```python
age = 25
print(age == 25)          # True
print(age != 25)          # False
print(18 <= age < 65)     # True  (chained comparison)
print(age > 30 or age < 20)   # False
print(not age > 30)       # True
```

| Operator | Meaning |
|---|---|
| `and` | true if both sides are true (stops early if the left side is falsy) |
| `or` | true if either side is true (stops early if the left side is truthy) |
| `not` | flips true and false |

`==` compares values. A single `=` assigns, so `if x = 5:` is a `SyntaxError`.

## 3. Truthiness

```python
for value in [0, 1, "", "0", [], [0], None]:
    print(repr(value), "->", bool(value))
```

```text
0 -> False
1 -> True
'' -> False
'0' -> True
[] -> False
[0] -> True
None -> False
```

This lets you write `if items:` instead of `if len(items) > 0:`.

`and` and `or` return an operand:

```python
name = "" or "guest"      # "guest"
print("a" and "b")        # b
```

Test for `None` with identity, not equality:

```python
if result is None:
    print("no result yet")
```

## 4. Conditional expressions

```python
label = "adult" if age >= 18 else "minor"
```

Use this for one short choice between two values. For anything longer, use a normal `if`.

## 5. match and case

`match` (Python 3.10+) selects a branch by the **shape** of a value.

```python
def describe(status: int) -> str:
    match status:
        case 200:
            return "ok"
        case 301 | 302:
            return "redirect"
        case 404:
            return "not found"
        case _:
            return "other"
```

- `|` joins alternatives (an *or-pattern*).
- `_` is the wildcard. Put it last as the default.
- Cases are tried top to bottom. The first match wins, and there is no fall-through.

### Sequence patterns

```python
def handle(command: list[str]) -> str:
    match command:
        case []:
            return "nothing"
        case ["quit"]:
            return "bye"
        case ["go", direction]:
            return f"going {direction}"
        case ["take", first, *rest]:
            return f"taking {first} and {len(rest)} more words"
        case _:
            return "unknown"
```

Names in a pattern (`direction`, `first`, `rest`) are **bound** to the matching parts.

### Guards

Add `if` after a pattern to require an extra condition:

```python
match point:
    case (x, y) if x == y:
        print("on the diagonal")
    case (x, y):
        print("somewhere else")
```

### Mappings and classes

```python
match event:
    case {"type": "click", "x": x, "y": y}:
        print("click at", x, y)
    case {"type": "key", "key": k}:
        print("key", k)
```

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

match Point(0, 5):
    case Point(x=0, y=y):
        print("on the y axis at", y)
```

A mapping pattern ignores extra keys. A class pattern checks the type first, then the attributes.

<div class="box warn" markdown="1">

## Common mistakes

- **Using a bare name as a constant.** `case ok:` does not compare with a variable called `ok`. It *captures* anything into a new name `ok`. To compare with a constant, use a dotted name such as `case Status.OK:` or a literal.
- **Ordering `elif` badly.** Put the most specific condition first.
- **`if x == True:`.** Write `if x:`. Likewise, write `is None`, not `== None`.
- **Using `match` for simple tests.** A plain `if` is clearer for one or two conditions. `match` pays off with many shapes.

</div>

## Try it yourself

1. Write `if` / `elif` / `else` to print "even", "odd" or "zero" for a number.
2. Rewrite your answer as a `match` statement. Which one reads better?
3. Predict the output of `print(bool([0]), bool(""), "x" or "y")`, then run it.

## Further reading

- [Python tutorial: if statements and match](https://docs.python.org/3/tutorial/controlflow.html#if-statements)
- [Structural pattern matching tutorial (PEP 636)](https://peps.python.org/pep-0636/)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="05-conditions-and-match:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/05-conditions-and-match/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/05-conditions-and-match/assignments/' | relative_url }}).
