---
layout: module
module: 12-modules-and-packages
kind: learn
title: Modules and packages
permalink: /modules/12-modules-and-packages/
---

<div class="box key" markdown="1">

## Key learning points

- A **module** is one `.py` file. A **package** is a folder of modules with an `__init__.py` file. `import` makes their names available.
- `import x`, `from x import y` and `import x as z` do the same loading. They differ in which names you get.
- Python finds modules by searching the folders in `sys.path`. The folder of your script comes first, then the standard library and installed packages.
- Code under `if __name__ == "__main__":` runs only when the file is run directly, not when it is imported.
- The standard library is large. Look there first (`itertools`, `collections`, `statistics`, `json`, `pathlib`, `math`, `random`) before you write your own code or install a package.
- Add third-party packages with `uv add name`. They are recorded in `pyproject.toml`.

</div>

## 1. Import forms

```python
import math
print(math.sqrt(16))              # 4.0

from math import pi, floor
print(round(pi, 3), floor(2.7))   # 3.142 2

import statistics as st
print(st.mean([1, 2, 3]))         # 2
```

- `import math` keeps the name `math.`. Readers see where `sqrt` comes from.
- `from math import pi` copies only the names you list into your file.
- `as` gives a shorter or clearer name.
- Avoid `from math import *`. It pulls in many names and hides where each one comes from.

A missing module raises `ModuleNotFoundError: No module named 'nonexistent_mod'`.

## 2. Your own module and `__name__`

Save this as `greet.py`:

```python
def hello(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(hello("script"))
```

From another file in the same folder:

```python
import greet
print(greet.hello("Ada"))     # Hello, Ada!
```

Python sets `__name__` to `"__main__"` in the file you run (`python greet.py`) and to the module name (`"greet"`) when the file is imported. The `if` block therefore holds the "run as a program" part. Importing the file only defines the functions and prints nothing.

Run a module by name with `python -m greet`. The `-m` option searches the module in `sys.path`, which also works for modules inside packages.

## 3. How Python finds modules

When you `import greet`, Python looks through `sys.path`, a list of folders:

1. The folder of the script you ran.
2. The standard library.
3. The `site-packages` folder of your environment, where installed packages live.

```python
import sys
print(sys.path[0])     # the folder of your script
```

If you name your own file `random.py` or `json.py`, you hide the standard module of the same name, because your folder comes first. Pick other names.

## 4. Packages

A folder with an `__init__.py` file is a package:

```text
shop/
    __init__.py
    pricing.py
    tools.py
    __main__.py
```

`shop/pricing.py`:

```python
TAX = 0.2


def total(prices):
    return round(sum(prices) * (1 + TAX), 2)
```

`shop/__init__.py` runs when the package is first imported. It often re-exports the main names:

```python
"""A tiny shop package."""

from .pricing import total

__all__ = ["total"]
```

```python
import shop
print(shop.total([10, 5]))     # 18.0
```

Inside a package, a module can import its neighbours in two ways:

```python
# shop/tools.py
from . import pricing            # relative: "from this package"
from shop.pricing import TAX     # absolute: the full path from the top
```

Absolute imports are clearer and work everywhere. Relative imports (with a leading dot) are useful inside bigger packages and only work in a package, not in a script you run directly.

A `__main__.py` file lets you run the whole package with `python -m shop`.

## 5. A short tour of the standard library

```python
import itertools, collections, statistics, json, random

print(list(itertools.batched("abcdefg", 3)))   # [('a', 'b', 'c'), ('d', 'e', 'f'), ('g',)]
print(list(itertools.accumulate([1, 2, 3, 4])))  # [1, 3, 6, 10]
print(list(itertools.combinations("abc", 2)))  # [('a', 'b'), ('a', 'c'), ('b', 'c')]
print(collections.Counter("hello").most_common(1))   # [('l', 2)]
print(statistics.median([3, 1, 2]))            # 2
print(json.dumps({"a": [1, 2]}))               # {"a": [1, 2]}
print(json.loads('{"x": 1}'))                  # {'x': 1}

rng = random.Random(42)                        # a generator with its own seed
print([rng.randint(1, 6) for _ in range(5)])   # [6, 1, 1, 6, 3]
```

`itertools.batched` needs Python 3.12 or later. A seeded `random.Random` gives the same numbers on every run, which makes code with randomness testable. `math`, `pathlib`, `datetime` and `argparse` are other modules you will use often. The [library index](https://docs.python.org/3/library/index.html) lists them all.

## 6. Third-party packages

Packages from PyPI (the Python Package Index) are installed into your project's environment. With `uv`:

```bash
uv add httpx          # install and record it in pyproject.toml
uv run python app.py  # run your script in the project environment
```

`pyproject.toml` describes the project and its dependencies:

```toml
[project]
name = "shop"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["httpx"]
```

Use `importlib.metadata.version("httpx")` to ask which version is installed. Use one environment per project, so that two projects can need different versions of the same package.

<div class="box warn" markdown="1">

## Common mistakes

- **Naming your file like a standard module** (`random.py`, `json.py`, `email.py`). Your file hides the real one and imports fail in strange ways.
- **Running code at the top level of a module.** Anything outside functions runs on every import. Put the "script" part under `if __name__ == "__main__":`.
- **`from x import *`.** It makes it unclear where names come from, and it can overwrite your own names.
- **Forgetting `__init__.py`.** Python can import a folder without one, but tools and tests often behave better with it, and it is the clear marker of a package.
- **Circular imports.** If `a` imports `b` and `b` imports `a`, one of them sees a half-loaded module. Move shared code into a third module.
- **Installing packages into the system Python.** Use a project environment (`uv add`) instead.

</div>

## Try it yourself

1. Write `mytools.py` with two small functions and a `__main__` block that demonstrates them. Import it from another file and check that the demo does not run.
2. Use `itertools.batched` to print a list of 10 names in groups of 3.
3. Create a folder `pets` with `__init__.py` and `dog.py`, then import `pets.dog` from a script next to the folder.

## Where this comes from

*Introducing Python*, chapter 12 (Modules and Packages). *Learn Python the Hard Way*, exercise 46 (a project skeleton). See also the Python tutorial on [modules](https://docs.python.org/3/tutorial/modules.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="12-modules-and-packages:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/12-modules-and-packages/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/12-modules-and-packages/assignments/' | relative_url }}).
