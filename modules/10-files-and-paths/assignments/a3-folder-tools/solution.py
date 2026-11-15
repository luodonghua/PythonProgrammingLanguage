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
    folder = Path(folder)
    return sorted(
        p.relative_to(folder).as_posix()
        for p in folder.rglob("*")
        if p.is_file() and p.name.endswith(suffix)
    )


def count_by_suffix(folder: Path) -> dict[str, int]:
    """Count the files directly inside `folder` (no subfolders) by suffix.

    The key is the lower-case suffix, or "" for files without one.

    count_by_suffix(folder)  -> {".txt": 2, ".py": 1, "": 1}
    """
    counts: dict[str, int] = {}
    for p in Path(folder).iterdir():
        if p.is_file():
            key = p.suffix.lower()
            counts[key] = counts.get(key, 0) + 1
    return counts


def largest_file(folder: Path) -> str | None:
    """Return the name of the biggest file directly inside `folder`
    (compare `stat().st_size`). If sizes tie, pick the name that sorts first.
    Return None if the folder has no files.
    """
    files = sorted(p for p in Path(folder).iterdir() if p.is_file())
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_size).name


def make_tree(base: Path, names: list[str]) -> None:
    """Create an empty file for every relative path in `names` under `base`,
    creating missing parent folders. Existing files are left alone.

    make_tree(base, ["a.txt", "docs/b.md"])  creates base/a.txt and base/docs/b.md
    """
    for name in names:
        path = Path(base) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()


def change_suffix(folder: Path, old: str, new: str) -> list[str]:
    """Rename every file directly inside `folder` that ends in `old` so it ends
    in `new` instead (both include the dot). Return the new names, sorted.

    change_suffix(folder, ".txt", ".md")   "a.txt" becomes "a.md"
    """
    new_names = []
    for p in sorted(Path(folder).iterdir()):
        if p.is_file() and p.name.endswith(old):
            target = p.with_name(p.name[: -len(old)] + new)
            p.rename(target)
            new_names.append(target.name)
    return sorted(new_names)


def total_size(folder: Path) -> int:
    """Return the total size in bytes of all files below `folder` (any depth)."""
    return sum(p.stat().st_size for p in Path(folder).rglob("*") if p.is_file())


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        make_tree(base, ["a.txt", "docs/b.md", "docs/c.txt"])
        print(find_files(base, ".txt"))
