---
layout: module
module: 03-strings
kind: learn
title: Strings and formatting
permalink: /modules/03-strings/
---

<div class="box key" markdown="1">

## Key learning points

- A `str` is an **immutable** sequence of Unicode characters. Methods such as `upper()` return a **new** string.
- **Indexing and slicing** work like lists: `s[0]`, `s[-1]`, `s[1:4]`, `s[::-1]`. A slice never raises `IndexError`. A single index can.
- Learn a core set of methods: `strip`, `split`, `join`, `replace`, `find`, `startswith`, `endswith`, `lower`, `upper`.
- **f-strings** (`f"{value:>8.2f}"`) are the normal way to build text. The part after `:` is a **format spec** for width, alignment, precision and separators.
- `\n` and `\t` are **escapes**. A raw string `r"..."` keeps backslashes as they are.
- `len()` counts characters. `encode("utf-8")` turns text into `bytes`, and the byte count can be larger.

</div>

## 1. Indexing and slicing

```python
s = "Python"
print(s[0], s[-1])        # P n
print(s[1:4])             # yth
print(s[:2], s[2:])       # Py thon
print(s[::-1])            # nohtyP   (step -1 reverses)
print(s[::2])             # Pto      (every second character)
print(len(s), "th" in s)  # 6 True
```

A slice `s[start:stop:step]` includes `start` and excludes `stop`. Out-of-range slices are cut quietly (`"Hello"[1:99]` is `"ello"`). A single bad index is an error:

```python
"abc"[5]    # IndexError: string index out of range
```

## 2. Strings are immutable

```python
word = "hello"
print(word.replace("h", "j"))   # jello
print(word)                     # hello   (unchanged)
```

`word[0] = "j"` raises `TypeError`. To "change" a string, build a new one and assign it to a name.

## 3. Useful methods

```python
raw = "  Hello, World  "
print(repr(raw.strip()))          # 'Hello, World'
print(raw.lower(), raw.upper())
print(raw.strip().title())        # Hello, World
```

Splitting and joining are opposites:

```python
print("a,b,,c".split(","))          # ['a', 'b', '', 'c']
print("one  two three".split())     # ['one', 'two', 'three']   (any whitespace)
print("a b c".split(" ", 1))        # ['a', 'b c']              (at most one split)
print("-".join(["a", "b", "c"]))    # a-b-c
```

Searching and testing:

```python
print("hello".find("l"), "hello".find("z"))   # 2 -1
print("hello".count("l"))                     # 2
print("data.csv".startswith("data"))          # True
print("data.csv".endswith((".csv", ".txt")))  # True
print("hello".replace("l", "L", 1))           # heLlo
print("abc".isalpha(), "123".isdigit())       # True True
```

`find` returns `-1` when the text is missing. `index` does the same search but raises `ValueError`. Use `in` when you only need yes or no.

## 4. f-strings and format specs

```python
name, price, qty = "tea", 3.5, 12
print(f"{name} costs {price}")        # tea costs 3.5
print(f"{price:.2f}")                 # 3.50
print(f"{qty:04d}")                   # 0012
print(f"{1234567:,}")                 # 1,234,567
print(f"{1234567.891:,.2f}")          # 1,234,567.89
print(f"{0.256:.1%}")                 # 25.6%
print(f"{name:>8}|{name:<8}|{name:^8}|")
```

```text
     tea|tea     |  tea   |
```

The spec is `[fill][align][width][,][.precision][type]`. Alignment is `<` left, `>` right, `^` centre. Strings align left by default and numbers align right. A fill character goes before the alignment: `f"{'x' * 3:-^11}"` gives `----xxx----`.

Two more tricks. `!r` shows the `repr`, and `=` prints the expression and its value (handy for debugging):

```python
print(f"{name!r} {price=}")    # 'tea' price=3.5
```

The older `str.format` does the same job and you will see it in existing code:

```python
print("{} costs {:.2f}".format(name, price))   # tea costs 3.50
print("{0} {0}".format("hi"))                  # hi hi
```

## 5. Escapes, raw and multi-line strings

```python
print("a\tb\nc")          # a, a tab, b, then a new line, then c
print("quote\"s", 'it\'s')
print(r"C:\new\table")    # C:\new\table   (raw: backslashes stay)
print(len(r"\n"), len("\n"))   # 2 1
```

Triple quotes make a multi-line string:

```python
text = """line one
line two"""
print(text.splitlines())    # ['line one', 'line two']
```

## 6. Unicode: characters and bytes

```python
print(len("café"))                    # 4 characters
print("café".encode("utf-8"))         # b'caf\xc3\xa9'
print(len("é".encode("utf-8")))       # 2 bytes
print(b"caf\xc3\xa9".decode("utf-8")) # café
print(ord("A"), chr(97))              # 65 a
```

A `str` holds characters. A `bytes` object holds numbers from 0 to 255. UTF-8 stores `é` in two bytes and `😀` in four. Always name the encoding when you convert (`"utf-8"`).

## 7. t-strings (Python 3.14+)

Python 3.14 adds **template strings**, written like an f-string with a `t` prefix:

```python
# Python 3.14 or later only
name = "Wenslydale"
template = t"Mister {name}"
```

A t-string does not produce a `str`. It produces a `Template` object (from `string.templatelib`) that keeps the fixed text and the inserted values **separate**. A function can then process the values safely, for example to escape HTML or to build a parameterised SQL query. This course uses ordinary f-strings. See [What's new in Python 3.14](https://docs.python.org/3/whatsnew/3.14.html) for the details.

<div class="box warn" markdown="1">

## Common mistakes

- **Ignoring the return value.** `name.strip()` alone does nothing useful. Write `name = name.strip()`.
- **Joining non-strings.** `",".join([1, 2])` is a `TypeError`. Convert first: `",".join(str(n) for n in numbers)`.
- **Off-by-one slices.** `s[1:4]` has three characters, not four.
- **Backslashes in Windows paths.** `"C:\new"` contains a new line. Use a raw string or forward slashes.
- **Mixing text and bytes.** `"a" + b"a"` is a `TypeError`. Encode or decode explicitly.

</div>

## Try it yourself

1. Print the last three characters of any word, and the word reversed.
2. Format the number `1234.5` as `$1,234.50`, right-aligned in a field 12 characters wide.
3. Split `"2025-06-30"` on `"-"` and join the parts back with `"/"`.

## Further reading

- [Python 3.14 release notes](https://docs.python.org/3/whatsnew/3.14.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="03-strings:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/03-strings/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/03-strings/assignments/' | relative_url }}).
