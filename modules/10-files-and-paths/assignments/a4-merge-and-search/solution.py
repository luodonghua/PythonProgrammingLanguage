"""Assignment 4: Merge and search text files.

The folder `notes/` next to this script holds a few small text files.
Combine them and search them. All functions take paths so tests can also
use temporary folders.
"""

from pathlib import Path

NOTES = Path(__file__).parent / "notes"


def list_notes(folder: Path) -> list[Path]:
    """Return the `.txt` files directly inside `folder`, sorted by name.
    Other file types and subfolders are ignored.
    """
    return sorted(p for p in Path(folder).glob("*.txt") if p.is_file())


def merge_notes(folder: Path, dest: Path) -> int:
    """Write all `.txt` notes of `folder` into the single file `dest`.

    For each note, in the order of `list_notes`, write a header line
    "== <file name> ==" followed by the lines of the note, and one blank line
    after the note. Return the number of notes merged. Create the parent
    folders of `dest` if they do not exist.

    Example output for two notes a.txt ("x\\n") and b.txt ("y\\n"):
        == a.txt ==
        x

        == b.txt ==
        y

    """
    notes = list_notes(folder)
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as out:
        for note in notes:
            out.write(f"== {note.name} ==\n")
            with open(note, encoding="utf-8") as src:
                for line in src:
                    out.write(line if line.endswith("\n") else line + "\n")
            out.write("\n")
    return len(notes)


def search(folder: Path, word: str) -> list[tuple[str, int, str]]:
    """Find lines containing `word` (ignore case) in the `.txt` notes of `folder`.

    Return (file name, line number starting at 1, line without newline)
    tuples, in note order and then line order.

    search(NOTES, "buy")  -> [("monday.txt", 1, "Buy milk"), ("tuesday.txt", 2, "Buy stamps")]
    """
    needle = word.lower()
    hits = []
    for note in list_notes(folder):
        with open(note, encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                text = line.rstrip("\n")
                if needle in text.lower():
                    hits.append((note.name, number, text))
    return hits


def number_lines(src: Path, dst: Path) -> int:
    """Copy `src` to `dst`, putting "<n>: " before each line (n starts at 1).
    Blank lines are numbered too. Return the number of lines.

    "a\\n\\nb\\n"  ->  "1: a\\n2: \\n3: b\\n"
    """
    count = 0
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for count, line in enumerate(fin, start=1):
            fout.write(f"{count}: {line}")
    return count


def safe_read(path: Path, default: str = "") -> str:
    """Return the file text, or `default` if the file does not exist.
    Do not hide other problems: a directory should still raise an error.
    """
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return default


if __name__ == "__main__":
    print(list_notes(NOTES))
    print(search(NOTES, "trip"))
