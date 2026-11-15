"""Assignment 3: A to-do list stored in a JSON file (code that tests use tmp_path for).

Each to-do is a dict {"text": str, "done": bool}. The list is stored in a JSON file.
"""

import json
from pathlib import Path


def load_todos(path: Path) -> list[dict]:
    """Read the to-do list from the JSON file at `path`.

    Return [] when the file does not exist. Otherwise return the stored list.
    """
    # TODO
    ...


def save_todos(path: Path, todos: list[dict]) -> None:
    """Write `todos` to `path` as JSON (UTF-8, indent=2).

    Create missing parent folders.
    """
    # TODO
    ...


def add_todo(path: Path, text: str) -> dict:
    """Append a new not-done to-do and save the file. Return the new to-do dict.

    The text is stripped. Empty text (after stripping) raises ValueError and
    leaves the file untouched.
    """
    # TODO
    ...


def complete_todo(path: Path, number: int) -> None:
    """Mark to-do number `number` (counting from 1) as done and save.

    A number that is out of range (0, negative or too large) raises IndexError
    and leaves the file untouched.
    """
    # TODO
    ...


def prompt_add(path: Path) -> None:
    """Ask the user for a to-do with input("New to-do: "), add it, and print
    "Added: <text>" (the stripped text). If the user types nothing (empty after
    stripping), print "Nothing to add" instead and do not touch the file.

    Call the built-in input() directly so that tests can replace it.
    """
    # TODO
    ...


if __name__ == "__main__":
    import tempfile

    demo_path = Path(tempfile.mkdtemp()) / "todos.json"
    add_todo(demo_path, "write tests")
    add_todo(demo_path, "run tests")
    complete_todo(demo_path, 1)
    print(load_todos(demo_path))
