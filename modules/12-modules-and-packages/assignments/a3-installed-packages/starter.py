"""Assignment 3: Ask Python about installed packages and importable modules.

Uses `importlib.metadata` (versions of installed packages) and `importlib`
(importing a module whose name you only know at run time).
"""

import importlib
import importlib.metadata
import importlib.util


def installed_version(package: str) -> str | None:
    """Return the installed version of a package (for example "8.3.2"),
    or None if the package is not installed.

    installed_version("pytest")             -> "8.3.2"   (your version may differ)
    installed_version("no-such-package-x")  -> None
    """
    # TODO: importlib.metadata.version(...) raises PackageNotFoundError.
    ...


def report_versions(packages: list[str]) -> dict[str, str]:
    """Return {package: version} for every installed package in the list,
    in the same order, and leave out the ones that are not installed.

    report_versions(["pytest", "no-such-package-x"])  -> {"pytest": "8.3.2"}
    """
    # TODO: reuse installed_version.
    ...


def format_report(packages: list[str]) -> str:
    """Return one line per package: "<name> <version>" or "<name> MISSING".
    Lines are in the order given and joined with "\\n" (no trailing newline).
    An empty list gives "".

    format_report(["pytest", "no-such-package-x"])
        -> "pytest 8.3.2\\nno-such-package-x MISSING"
    """
    # TODO: build the lines with a loop or comprehension.
    ...


def can_import(module: str) -> bool:
    """Return True if `module` can be imported, without importing it.

    can_import("json")           -> True
    can_import("json.decoder")   -> True
    can_import("not_a_module_x") -> False
    can_import("not_a_pkg_x.sub") -> False   (must not raise)

    Use importlib.util.find_spec. For a dotted name it imports the parent
    package and raises ModuleNotFoundError if the parent is missing.
    """
    # TODO: call find_spec inside try/except ModuleNotFoundError.
    ...


def load_function(dotted_path: str):
    """Return the function or object at a dotted path like "math.sqrt".

    The last part is the attribute and everything before it is the module:
    load_function("os.path.join")  -> the function os.path.join
    load_function("json.dumps")    -> the function json.dumps

    Raise ValueError("need module.attribute") if there is no dot in the path.
    Let ImportError and AttributeError propagate for bad names.
    """
    # TODO: str.rpartition(".") then importlib.import_module and getattr.
    ...


if __name__ == "__main__":
    print(format_report(["pytest", "no-such-package-x"]))
    print(load_function("math.sqrt"))
