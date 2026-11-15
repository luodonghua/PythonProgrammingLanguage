"""Assignment 3: Working with folders and paths (pathlib).

Every function takes a folder as a `Path`. Return paths **relative to that
folder** where the text says so, written with forward slashes via
`.as_posix()`, so results look the same on every system.
"""

from pathlib import Path


def find_files(folder: Path, suffix: str) -> list[str]:
    """Return all files below `folder` (any depth) whose name ends with `suffix`.

    Results are relative paths like "sub/a.txt", sorted alphabetically.
    Directories are not included. `suffix` includes the dot, for example ".txt".

    find_files(folder, ".txt")  -> ["a.txt", "sub/b.txt"]
    """
    # TODO: folder.rglob("*") or rglob(f"*{suffix}"), p.is_file(), p.relative_to(folder).as_posix().
    ...


def count_by_suffix(folder: Path) -> dict[str, int]:
    """Count the files directly inside `folder` (no subfolders) by suffix.

    The key is the lower-case suffix, or "" for files without one.

    count_by_suffix(folder)  -> {".txt": 2, ".py": 1, "": 1}
    """
    # TODO: folder.iterdir(), p.is_file(), p.suffix.lower().
    ...


def largest_file(folder: Path) -> str | None:
    """Return the name of the biggest file directly inside `folder`
    (compare `stat().st_size`). If sizes tie, pick the name that sorts first.
    Return None if the folder has no files.
    """
    # TODO: use max() with a key, over files sorted by name.
    ...


def make_tree(base: Path, names: list[str]) -> None:
    """Create an empty file for every relative path in `names` under `base`,
    creating missing parent folders. Existing files are left alone.

    make_tree(base, ["a.txt", "docs/b.md"])  creates base/a.txt and base/docs/b.md
    """
    # TODO: path.parent.mkdir(parents=True, exist_ok=True) and path.touch().
    ...


def change_suffix(folder: Path, old: str, new: str) -> list[str]:
    """Rename every file directly inside `folder` that ends in `old` so it ends
    in `new` instead (both include the dot). Return the new names, sorted.

    change_suffix(folder, ".txt", ".md")   "a.txt" becomes "a.md"
    """
    # TODO: path.with_suffix(new) and path.rename(...).
    ...


def total_size(folder: Path) -> int:
    """Return the total size in bytes of all files below `folder` (any depth)."""
    # TODO: sum of p.stat().st_size over files found by rglob.
    ...


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        make_tree(base, ["a.txt", "docs/b.md", "docs/c.txt"])
        print(find_files(base, ".txt"))
