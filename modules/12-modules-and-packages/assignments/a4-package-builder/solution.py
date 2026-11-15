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
    return name.isidentifier() and not keyword.iskeyword(name) and name == name.lower()


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
    for candidate in [name, *modules]:
        if not is_valid_module_name(candidate):
            raise ValueError(f"invalid module name: {candidate!r}")
    package_dir = Path(base) / name
    package_dir.mkdir(parents=True, exist_ok=True)
    created = []
    init_file = package_dir / "__init__.py"
    init_file.write_text(f'"""Package {name}."""\n', encoding="utf-8")
    created.append(f"{name}/__init__.py")
    for module in modules:
        text = (
            f'"""Module {module}."""\n'
            "\n"
            "\n"
            "def hello():\n"
            f'    return "{name}.{module}"\n'
        )
        (package_dir / f"{module}.py").write_text(text, encoding="utf-8")
        created.append(f"{name}/{module}.py")
    return sorted(created)


def list_modules(package_dir: Path) -> list[str]:
    """Return the sorted module names (file names without ".py") in a package
    folder. `__init__` is not a module name for this purpose. Subfolders and
    other files are ignored.

    list_modules(base / "pkg")  -> ["helpers", "util"]
    """
    return sorted(
        p.stem for p in Path(package_dir).glob("*.py") if p.is_file() and p.stem != "__init__"
    )


def find_missing_init(root: Path) -> list[str]:
    """Find folders below `root` (not `root` itself) that contain `.py` files
    but have no `__init__.py`. Return their paths relative to `root` with
    forward slashes, sorted.

    Folders that contain no `.py` file directly are fine.
    """
    root = Path(root)
    missing = []
    for folder in root.rglob("*"):
        if not folder.is_dir():
            continue
        has_python = any(folder.glob("*.py"))
        if has_python and not (folder / "__init__.py").exists():
            missing.append(folder.relative_to(root).as_posix())
    return sorted(missing)


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        print(create_package(Path(tmp), "toolbox", ["text", "maths"]))
