"""Assignment 4: Build and inspect a Python package.

A package is a folder with an `__init__.py` file that contains modules
(`.py` files). These helpers create and check such folders. Tests use
temporary folders, and one test imports the package you generate.
"""

import keyword
from pathlib import Path


def is_valid_module_name(name: str) -> bool:
    """Return True if `name` can be used in an import statement as a module name.

    It must be a valid identifier, not a Python keyword, and lower case
    (PEP 8 style for module names).

    is_valid_module_name("utils")      -> True
    is_valid_module_name("my_tools2")  -> True
    is_valid_module_name("2fast")      -> False
    is_valid_module_name("my-tools")   -> False
    is_valid_module_name("class")      -> False
    is_valid_module_name("Utils")      -> False
    is_valid_module_name("")           -> False
    """
    # TODO: str.isidentifier(), keyword.iskeyword(), str.islower() ...
    ...


def create_package(base: Path, name: str, modules: list[str]) -> list[str]:
    """Create the package folder `base/name` with an `__init__.py` and one
    file `<module>.py` for each name in `modules`.

    - `__init__.py` contains the single line:  "\"\"\"Package <name>.\"\"\"\\n"
      (that is a one-line docstring)
    - each module file contains:  "\"\"\"Module <module>.\"\"\"\\n"  and then a
      function  def hello():  returning the string "<name>.<module>"
    - Raise ValueError(f"invalid module name: {x!r}") if `name` or any module
      name fails is_valid_module_name (check everything before creating files).
    - Return the sorted list of created paths relative to `base`, with forward
      slashes, for example ["pkg/__init__.py", "pkg/util.py"].
    """
    # TODO: validate, mkdir(parents=True, exist_ok=True), write files, return the list.
    ...


def list_modules(package_dir: Path) -> list[str]:
    """Return the sorted module names (file names without ".py") in a package
    folder. `__init__` is not a module name for this purpose. Subfolders and
    other files are ignored.

    list_modules(base / "pkg")  -> ["helpers", "util"]
    """
    # TODO: glob("*.py"), p.stem, skip "__init__".
    ...


def find_missing_init(root: Path) -> list[str]:
    """Find folders below `root` (not `root` itself) that contain `.py` files
    but have no `__init__.py`. Return their paths relative to `root` with
    forward slashes, sorted.

    Folders that contain no `.py` file directly are fine.
    """
    # TODO: root.rglob("*") for folders, check .glob("*.py") and (folder / "__init__.py").exists().
    ...


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        print(create_package(Path(tmp), "toolbox", ["text", "maths"]))
