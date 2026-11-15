---
layout: module
module: 18-text-data
kind: learn
title: "Text data: CSV, JSON and regex"
permalink: /modules/18-text-data/
---

<div class="box key" markdown="1">

## Key learning points

- **CSV** files hold rows of text fields. `csv.reader` gives lists, `csv.DictReader` gives dicts keyed by the header. Every value is a `str`, so you convert numbers yourself.
- Open CSV files with `newline=""` and `encoding="utf-8"` so the `csv` module controls line endings and quoting.
- **JSON** maps to Python types: object to `dict`, array to `list`, `null` to `None`. Use `json.loads` / `json.dumps` for strings and `json.load` / `json.dump` for files.
- A **regular expression** (regex) describes a text pattern. `re.search` finds it anywhere, `re.match` only at the start, `re.fullmatch` needs the whole string, `re.findall` returns every match.
- Write patterns as **raw strings** (`r"\d+"`) and use groups, including named groups, to pull out the parts you need.
- Real data has bad rows. Catch the error per row, record it, and keep going.

</div>

## 1. CSV with csv.reader and DictReader

CSV (comma-separated values) is plain text, one record per line. The `csv` module handles quoting, so a field like `"Smith, Ann"` stays one field.

```python
import csv
import io

text = "name,qty,price\npen,3,1.50\nbook,1,12.00\n"

for row in csv.reader(io.StringIO(text)):
    print(row)
```

```text
['name', 'qty', 'price']
['pen', '3', '1.50']
['book', '1', '12.00']
```

`csv.DictReader` uses the first line as keys:

```python
for row in csv.DictReader(io.StringIO(text)):
    print(row)
```

```text
{'name': 'pen', 'qty': '3', 'price': '1.50'}
{'name': 'book', 'qty': '1', 'price': '12.00'}
```

To read a real file, open it like this:

```python
with open("sales.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        total = int(row["qty"]) * float(row["price"])
```

`io.StringIO` is a file-like object made from a string. It is handy for examples and tests.

## 2. Writing CSV

```python
out = io.StringIO()
writer = csv.writer(out)
writer.writerow(["name", "note"])
writer.writerow(["pen", 'blue, "fine"'])
print(repr(out.getvalue()))
```

```text
'name,note\r\npen,"blue, ""fine"""\r\n'
```

The writer quotes the field that contains a comma and doubles the inner quotes. It ends lines with `\r\n` by default, which is why you open real files with `newline=""`. `csv.DictWriter(f, fieldnames=[...])` writes dicts, and `writeheader()` writes the header row.

## 3. Bad rows

CSV gives you only strings, and real files have gaps. A short row leaves `None` in `DictReader`. A long row puts the extras under the key `None`.

```python
for row in csv.DictReader(io.StringIO("a,b\n1,2,3\n4\n")):
    print(row)
```

```text
{'a': '1', 'b': '2', None: ['3']}
{'a': '4', 'b': None}
```

Convert inside `try` and collect the problems:

```python
good, errors = [], []
for line_no, row in enumerate(csv.DictReader(f), start=2):
    try:
        good.append(int(row["qty"]))
    except (TypeError, ValueError) as exc:
        errors.append((line_no, str(exc)))
```

Line 1 is the header, so the first data row is line 2.

## 4. JSON

JSON is the common text format for data exchange. Its types map onto Python like this:

| JSON | Python |
|---|---|
| object | `dict` |
| array | `list` |
| string, number | `str`, `int` or `float` |
| `true`, `false`, `null` | `True`, `False`, `None` |

```python
import json

data = {"name": "Ada", "langs": ["py", "c"], "age": None, "ok": True}
s = json.dumps(data)
print(s)
print(json.loads(s) == data)
```

```text
{"name": "Ada", "langs": ["py", "c"], "age": null, "ok": true}
True
```

`indent=2` and `sort_keys=True` make output readable and stable:

```python
print(json.dumps(data, indent=2, sort_keys=True))
```

```text
{
  "age": null,
  "langs": [
    "py",
    "c"
  ],
  "name": "Ada",
  "ok": true
}
```

For files use `json.dump(obj, f)` and `json.load(f)`. Types JSON does not know raise `TypeError`. Give `dumps` a `default=` function to convert them:

```python
from datetime import date

print(json.dumps({"d": date(2025, 1, 2)}, default=str))
```

```text
{"d": "2025-01-02"}
```

Round trips are not perfect. Tuples come back as lists, and object keys are always strings. Invalid text raises `json.JSONDecodeError` (a subclass of `ValueError`):

```python
try:
    json.loads("{bad json}")
except json.JSONDecodeError as exc:
    print(exc)
```

```text
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

## 5. Regular expressions

```python
import re

log = "2025-03-01 ERROR disk full on /dev/sda1"
m = re.search(r"(\d{4})-(\d{2})-(\d{2})", log)
print(m.group(), m.groups(), m.start())
```

```text
2025-03-01 ('2025', '03', '01') 0
```

| Piece | Meaning |
|---|---|
| `\d` `\w` `\s` | digit, word character, whitespace |
| `.` | any character except newline |
| `*` `+` `?` | 0 or more, 1 or more, 0 or 1 |
| `{3}` `{2,4}` | exact count, range |
| `[a-z]` `[^,]` | a set, anything not in the set |
| `^` `$` | start, end of string |
| `( )` | a group |

**Raw strings.** Write `r"\d+"`. Without the `r`, Python reads `\d` as a string escape first.

**Functions.**

```python
print(re.findall(r"\d+", "a1 b22 c333"))
print(re.match(r"\d+", "abc123"), re.search(r"\d+", "abc123"))
print(re.fullmatch(r"\d{3}-\d{4}", "555-1234") is not None)
```

```text
['1', '22', '333']
None <re.Match object; span=(3, 6), match='123'>
True
```

`match` returns `None` here because it only tries the start of the string. Always check for `None` before calling `.group()`.

**Named groups** make results readable:

```python
m = re.match(r"(?P<date>\S+) (?P<level>[A-Z]+) (?P<msg>.*)", log)
print(m.groupdict())
```

```text
{'date': '2025-03-01', 'level': 'ERROR', 'msg': 'disk full on /dev/sda1'}
```

**Substitution** with `re.sub`, which also accepts a function:

```python
print(re.sub(r"\s+", " ", "a   b \n c"))
print(re.sub(r"(\d+)", lambda m: str(int(m.group()) * 2), "3 apples 10 pears"))
```

```text
a b c
6 apples 20 pears
```

**Flags** change matching: `re.IGNORECASE`, `re.MULTILINE` (`^` and `$` match at each line) and `re.VERBOSE`. Use `re.compile(pattern)` to reuse a pattern.

**Greedy or lazy.** `+` takes as much as it can. Add `?` to take as little as possible:

```python
print(re.findall(r"<.+>", "<a><b>"), re.findall(r"<.+?>", "<a><b>"))
```

```text
['<a><b>'] ['<a>', '<b>']
```

## 6. TOML configuration

`tomllib` (standard library since Python 3.11) reads TOML, the format of `pyproject.toml`. It reads only; it cannot write.

```python
import tomllib

cfg = tomllib.loads("""
title = "demo"
[server]
port = 8080
tags = ["a", "b"]
""")
print(cfg)
```

```text
{'title': 'demo', 'server': {'port': 8080, 'tags': ['a', 'b']}}
```

For a file, open it in binary mode: `tomllib.load(open("x.toml", "rb"))`.

<div class="box warn" markdown="1">

## Common mistakes

- **Treating CSV values as numbers.** `"3" + "4"` is `"34"`. Convert with `int()` or `float()` and handle the `ValueError`.
- **Forgetting `newline=""`** when opening a CSV file. Quoted fields that contain line breaks can then break, and Windows may add blank lines when writing.
- **Splitting CSV lines with `line.split(",")`.** It fails on quoted commas. Use the `csv` module.
- **Using `re.match` when you mean `re.search`.** `match` only checks the start of the string.
- **Calling `.group()` on `None`.** When nothing matches, the result is `None`. Test it first.
- **Writing a regex for everything.** For fixed text, `str.startswith` or `str.split` is simpler. Do not parse HTML with a regex.

</div>

## Try it yourself

1. Use `csv.DictReader` on a string you write yourself and print the sum of one numeric column.
2. Turn a list of dicts into a JSON string with `indent=2`, then load it back and compare it with the original.
3. Write a regex that finds every word starting with `#` in a sentence. Print the result of `re.findall`.

## Where this comes from

*Introducing Python*, chapter 17 (Text Data). *Learn Python the Hard Way* exercises 15 to 17 (reading and writing files) cover the file-handling side. Regex, `csv`, `json` and `tomllib` go beyond the two books in detail; see the [re](https://docs.python.org/3/library/re.html), [csv](https://docs.python.org/3/library/csv.html), [json](https://docs.python.org/3/library/json.html) and [tomllib](https://docs.python.org/3/library/tomllib.html) docs.

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="18-text-data:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/18-text-data/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/18-text-data/assignments/' | relative_url }}).
