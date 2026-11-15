---
layout: module
module: 10-files-and-paths
kind: learn
title: Files and paths
permalink: /modules/10-files-and-paths/
---

<div class="box key" markdown="1">

## Key learning points

- Open a file with `with open(path, mode, encoding="utf-8") as f:`. The `with` block closes the file for you, even if an error happens.
- Modes: `"r"` read (default), `"w"` write (**erases** the old content), `"a"` append, and `"b"` added for bytes.
- A text file is an iterator of lines: `for line in f:` reads one line at a time and works for huge files.
- `pathlib.Path` represents a file or folder path. Build paths with `/`, and use `.read_text()`, `.write_text()`, `.exists()`, `.glob()` and `.mkdir()`.
- Always pass `encoding="utf-8"` for text. The default depends on the operating system.

</div>

## 1. Writing and appending

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("first line\n")
    f.write("second line\n")
    print("third line", file=f)     # print can write to a file too

with open("notes.txt", "a", encoding="utf-8") as f:
    f.write("fourth\n")
```

- `write` does not add a newline. You add `"\n"` yourself. `print(..., file=f)` does.
- Mode `"w"` creates the file or **empties** an existing one. Mode `"a"` adds to the end.

## 2. Reading

```python
with open("notes.txt", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip("\n"))
```

```text
first line
second line
third line
fourth
```

Each line still ends with `"\n"`, so `rstrip("\n")` removes it. The other read methods:

```python
with open("notes.txt", encoding="utf-8") as f:
    text = f.read()            # the whole file as one str

with open("notes.txt", encoding="utf-8") as f:
    first = f.readline()       # one line, 'first line\n'
    rest = f.readlines()       # the remaining lines as a list
```

Use the `for` loop for big files, because `read()` and `readlines()` load everything into memory.

Opening a missing file raises `FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'`. The next topic shows how to handle that.

## 3. Encodings and newlines

A file stores bytes. The **encoding** says how characters map to bytes. UTF-8 is the standard. The letter `é` takes 2 bytes in UTF-8, so `len("é".encode("utf-8"))` is `2`, while `len("é")` is `1`.

If you leave out `encoding`, Python uses a platform default, and a file that reads fine on Linux can fail on another system. Write `encoding="utf-8"` every time.

In text mode Python converts line endings: `"\r\n"` (Windows) is read as `"\n"`. Open with `newline=""` if you need the raw endings. Use mode `"rb"` or `"wb"` for binary files such as images. These give you `bytes` and take no `encoding`.

## 4. pathlib

`Path` objects are better than strings for paths. The `/` operator joins parts with the right separator for your system.

```python
from pathlib import Path

p = Path("data") / "reports" / "2025.csv"
print(p)            # data/reports/2025.csv   (backslashes on Windows)
print(p.name)       # 2025.csv
print(p.stem)       # 2025
print(p.suffix)     # .csv
print(p.parent)     # data/reports
print(p.exists())   # False
```

Create folders and write a file in one go:

```python
p.parent.mkdir(parents=True, exist_ok=True)   # make data/reports, no error if it exists
p.write_text("a,b\n1,2\n", encoding="utf-8")
print(p.read_text(encoding="utf-8"))
print(p.is_file(), p.parent.is_dir(), p.stat().st_size)   # True True 8
print(p.with_suffix(".json"))                 # data/reports/2025.json
```

`write_text` and `read_text` open and close the file for you. They suit small files. `read_bytes` and `write_bytes` do the same for bytes.

List and search folders:

```python
for q in sorted(Path("data").glob("*.txt")):    # files directly in data/
    print(q)
for q in sorted(Path("data").rglob("*.csv")):   # data/ and all subfolders
    print(q)
```

`iterdir()` lists everything in one folder. `glob` results come in no fixed order, so wrap them in `sorted`.

## 5. shutil and tempfile

```python
import shutil
import tempfile

shutil.copy("notes.txt", "copy.txt")    # copy a file
shutil.rmtree("data")                   # delete a folder and everything inside. No undo!

with tempfile.TemporaryDirectory() as tmp:
    scratch = Path(tmp) / "scratch.txt"
    scratch.write_text("hi", encoding="utf-8")
# the folder and the file are gone here
```

`tempfile.TemporaryDirectory()` is the safe place for scratch files and for tests. The `tmp_path` fixture in pytest works the same way.

<div class="box warn" markdown="1">

## Common mistakes

- **Using mode `"w"` when you meant `"a"`.** `"w"` deletes the existing content the moment you open the file.
- **Forgetting `with`.** Without it, the file may stay open and the last data may not be written.
- **Missing `encoding="utf-8"`.** Non-ASCII text such as `é` or `€` can break on another system.
- **Joining paths with `+` or an f-string.** Use `Path("a") / "b"` so the separator is right.
- **Relying on the current folder.** A relative path like `"data.txt"` depends on where you start the program. Use `Path(__file__).parent / "data.txt"` to find a file next to your script.

</div>

## Try it yourself

1. Write a script that saves the numbers 1 to 10, one per line, to `numbers.txt`, then reads them back and prints the sum.
2. Use `Path.rglob("*.py")` to count the `.py` files below the current folder.
3. Write a function that appends a line with the text of a message to `log.txt`. Call it three times and check the file.

## Further reading

- [Python docs](https://docs.python.org/3/library/pathlib.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="10-files-and-paths:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/10-files-and-paths/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/10-files-and-paths/assignments/' | relative_url }}).
