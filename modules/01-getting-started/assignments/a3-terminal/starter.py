"""Assignment 3: Terminal commands, written in Python.

pwd -> where_am_i()          ls *.py -> list_python_files()
"""

from pathlib import Path


def where_am_i() -> str:
    """Return the current working directory as a string (like `pwd`).

    Hint: Path.cwd()
    """
    # TODO
    ...


def list_python_files(directory: Path) -> list[str]:
    """Return the sorted names of the .py files directly inside `directory`.

    - Do not include files in sub-folders.
    - Do not include folders, even if the folder name ends in .py.
    Hint: directory.iterdir(), path.is_file(), path.suffix, path.name
    """
    # TODO
    ...


if __name__ == "__main__":
    print(where_am_i())
    for name in list_python_files(Path(".")):
        print(name)
