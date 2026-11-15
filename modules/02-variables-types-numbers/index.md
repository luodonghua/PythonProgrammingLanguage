---
layout: module
module: 02-variables-types-numbers
kind: learn
title: Variables, types and numbers
permalink: /modules/02-variables-types-numbers/
---

<div class="box key" markdown="1">

## Key learning points

- A **variable** is a name that points to a value. `x = 5` binds the name `x` to the object `5`. The name has no type. The value does.
- The basic types are `int`, `float`, `bool`, `str`, `None` and (rarely) `complex`. Check them with `type()` and `isinstance()`.
- `/` always gives a `float`. `//` is floor division, `%` is the remainder, `**` is power, and `divmod(a, b)` gives both `//` and `%` at once.
- Floats are binary approximations: `0.1 + 0.2` is not exactly `0.3`. Use `decimal.Decimal` for money.
- `int()`, `float()` and `str()` convert between types. They raise `ValueError` when the text does not fit.
- `==` compares values. `is` compares identity (the same object). Lists can change in place (mutable). Numbers and strings cannot (immutable).

</div>

## 1. Names and assignment

```python
price = 4
price = "four"      # the same name can point to a different type
print(type(price))
```

```text
<class 'str'>
```

Naming rules:

- Use letters, digits and `_`. The name cannot start with a digit.
- Names are case sensitive: `Total` and `total` are different.
- You cannot use keywords such as `if`, `for` or `None`.
- Style (PEP 8): `snake_case` for variables, `UPPER_CASE` for constants.

You can assign several names at once, update in place, and swap without a temporary variable:

```python
count = 0
count += 1          # same as count = count + 1
count *= 5
print(count)        # 5

w, h = 1, 2
w, h = h, w
print(w, h)         # 2 1
```

## 2. The basic types

```python
for value in (42, 3.14, True, None, 2 + 3j, "hi"):
    print(repr(value), type(value).__name__)
```

```text
42 int
3.14 float
True bool
None NoneType
(2+3j) complex
'hi' str
```

- `int` has no size limit: `2 ** 100` is `1267650600228229401496703205376`.
- `bool` has two values, `True` and `False`. It is a subtype of `int`, so `True + True` is `2`.
- `None` means "no value". There is only one `None` object.
- `complex` numbers (`2 + 3j`) are used in science and engineering. This course does not need them.

`isinstance(value, type)` is the usual way to test a type. It accepts a tuple of types:

```python
print(isinstance(True, int))          # True
print(isinstance(3, (int, float)))    # True
```

## 3. Arithmetic

```python
print(7 / 2)       # 3.5   true division, always a float
print(7 // 2)      # 3     floor division
print(7 % 2)       # 1     remainder
print(2 ** 10)     # 1024  power
print(-7 // 2)     # -4    floor division rounds down, not toward zero
print(-7 % 2)      # 1
print(divmod(7, 2))        # (3, 1)
```

`divmod` is handy for splitting a total into units. 3725 seconds is:

```python
hours, rest = divmod(3725, 3600)
minutes, seconds = divmod(rest, 60)
print(hours, minutes, seconds)   # 1 2 5
```

An `int` mixed with a `float` gives a `float`: `type(3 + 4.0)` is `float`.

## 4. Float precision, Decimal and round

```python
print(0.1 + 0.2)           # 0.30000000000000004
print(0.1 + 0.2 == 0.3)    # False
```

A `float` stores a binary fraction, and `0.1` has no exact binary form. Compare floats with a tolerance:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))   # True
```

For money, use `Decimal` and build it from a **string**, not from a float:

```python
from decimal import Decimal, ROUND_HALF_UP

print(Decimal("0.1") + Decimal("0.2"))    # 0.3
cents = Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(cents)                              # 2.68
```

`round()` uses "round half to even" and the float error shows up:

```python
print(round(2.5), round(3.5))   # 2 4
print(round(2.675, 2))          # 2.67
```

Use `f"{value:.2f}"` to *display* a number with two decimals. It does not change the value.

## 5. Underscores and other literals

```python
print(1_000_000)            # 1000000
print(0xFF, 0b101, 1e3)     # 255 5 1000.0
```

Underscores only make long numbers readable. Python ignores them.

## 6. Converting between types

```python
print(int("42"), int(3.9), float("2.5"), str(7) + "!")   # 42 3 2.5 7!
print(int(True), bool(""))                                # 1 False
```

`int(3.9)` cuts off the decimals (it gives `3`, it does not round). Bad text raises `ValueError`:

```python
try:
    int("3.5")
except ValueError as error:
    print(error)
```

```text
invalid literal for int() with base 10: '3.5'
```

To read `"3.5"` as a whole number, convert to `float` first. Whitespace around the text is allowed: `int("  42  ")` is `42`.

## 7. Mutable and immutable, `is` and `==`

```python
a = [1]
b = a              # b is another name for the SAME list
b.append(2)
print(a)           # [1, 2]

c = [1, 2]
print(a == c)      # True   equal values
print(a is c)      # False  different objects
```

Strings and numbers are **immutable**. You cannot change them in place:

```python
s = "hi"
s[0] = "H"         # TypeError: 'str' object does not support item assignment
```

Use `is` only for `None` (`if x is None:`). For everything else use `==`.

<div class="box warn" markdown="1">

## Common mistakes

- **Using `input()` or text as a number.** `"5" + 1` is a `TypeError`. Convert first with `int("5")`.
- **Comparing floats with `==`.** Use `math.isclose`, or use `Decimal` for money.
- **`Decimal(0.1)`.** It copies the float error. Write `Decimal("0.1")`.
- **Expecting `//` to round toward zero.** `-7 // 2` is `-4`.
- **Thinking `b = a` copies a list.** It adds a second name for the same list.

</div>

## Try it yourself

1. Convert 100 minutes to hours and minutes with `divmod`.
2. Predict `type(10 / 2)`, then check. Why is it not `int`?
3. Add `Decimal("19.99")` three times and compare with `19.99 + 19.99 + 19.99`.

## Further reading

- [Python tutorial: numbers](https://docs.python.org/3/tutorial/introduction.html#numbers)
- [Floating-point arithmetic: issues and limitations](https://docs.python.org/3/tutorial/floatingpoint.html)
- [decimal](https://docs.python.org/3/library/decimal.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="02-variables-types-numbers:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/02-variables-types-numbers/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/02-variables-types-numbers/assignments/' | relative_url }}).
