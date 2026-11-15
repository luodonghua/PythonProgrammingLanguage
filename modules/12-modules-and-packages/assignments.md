---
layout: module
module: 12-modules-and-packages
kind: assignments
title: Modules and packages - assignments
permalink: /modules/12-modules-and-packages/assignments/
---
Four tasks. Write the code yourself first, run the tests, and open the solution only after you have tried.

{% include practice-setup.md %}

Run all tests for this topic:

```bash
uv run pytest modules/12-modules-and-packages
```

---

<div class="assignment" markdown="1">

## Assignment 1: A module with a command-line entry point

**Goal:** Write a small module that parses numbers, summarises them with `statistics` and runs as a script through `main(argv)` and the `__main__` guard. Practises `import`, `sys.argv`, exit codes and `if __name__ == "__main__":`.

**Files:** [`starter.py`]({{ 'modules/12-modules-and-packages/assignments/a1-numstats-cli/starter.py' | relative_url }}), test file `test_a1_numstats_cli.py` in the same folder.

```python
{% include_relative assignments/a1-numstats-cli/starter.py %}
```

Run: `uv run pytest modules/12-modules-and-packages/assignments/a1-numstats-cli`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-numstats-cli/solution.py %}
```

The logic lives in functions, so other code can import and test it. `main(argv)` returns an exit code and the guard turns it into a process exit with `raise SystemExit(main())`. Errors go to `sys.stderr` and the result goes to stdout. One test also runs the file as a real script in a subprocess.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: Standard library tour

**Goal:** Solve seven small tasks by picking the right standard library function from `itertools`, `math`, `collections`, `random`, `json` and `statistics`. Practises reading module documentation instead of writing loops.

**Files:** [`starter.py`]({{ 'modules/12-modules-and-packages/assignments/a2-stdlib-tour/starter.py' | relative_url }}), test file `test_a2_stdlib_tour.py` in the same folder.

```python
{% include_relative assignments/a2-stdlib-tour/starter.py %}
```

Run: `uv run pytest modules/12-modules-and-packages/assignments/a2-stdlib-tour`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-stdlib-tour/solution.py %}
```

Each answer is one or two lines because the module already does the work: `itertools.batched`, `itertools.accumulate`, `math.comb`, `math.dist`, `Counter.most_common`, `json.dumps(sort_keys=True, indent=2)` and `statistics.stdev`. `rolls` uses its own `random.Random(seed)` object, so it is repeatable and does not disturb the global random state. `itertools.batched` needs Python 3.12 or later.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Installed packages and dynamic imports

**Goal:** Report installed package versions with `importlib.metadata`, check whether a module can be imported without importing it, and load a function from a dotted name. Practises `importlib` and the exceptions that imports raise.

**Files:** [`starter.py`]({{ 'modules/12-modules-and-packages/assignments/a3-installed-packages/starter.py' | relative_url }}), test file `test_a3_installed_packages.py` in the same folder.

```python
{% include_relative assignments/a3-installed-packages/starter.py %}
```

Run: `uv run pytest modules/12-modules-and-packages/assignments/a3-installed-packages`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-installed-packages/solution.py %}
```

`importlib.metadata.version` raises `PackageNotFoundError` for a missing package, which `installed_version` turns into `None`. `importlib.util.find_spec` looks for a module without running it, but for `a.b` it imports `a` first, so a missing parent raises `ModuleNotFoundError`. `load_function` splits the path with `rpartition(".")`, imports the module with `importlib.import_module` and fetches the attribute with `getattr`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: Package builder and checker

**Goal:** Generate a real package folder with `__init__.py` and modules, list its modules, and find folders that are missing `__init__.py`. A test imports the package you generated. Practises package layout, `pathlib` and valid module names.

**Files:** [`starter.py`]({{ 'modules/12-modules-and-packages/assignments/a4-package-builder/starter.py' | relative_url }}), test file `test_a4_package_builder.py` in the same folder.

```python
{% include_relative assignments/a4-package-builder/starter.py %}
```

Run: `uv run pytest modules/12-modules-and-packages/assignments/a4-package-builder`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-package-builder/solution.py %}
```

`create_package` checks every name before it writes anything, so a failure leaves no half-built package. A module name must be a lower-case identifier that is not a keyword. `find_missing_init` looks at each folder with `rglob("*")` and reports those with `.py` files but no `__init__.py`. The import test adds the temporary folder to `sys.path` with `monkeypatch.syspath_prepend`.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="12-modules-and-packages:assignments"> I have finished the assignments</label></li>
</ul>
