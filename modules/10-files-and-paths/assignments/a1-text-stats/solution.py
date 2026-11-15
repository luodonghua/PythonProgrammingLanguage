"""Assignment 1: Text file statistics.

Read a text file and report numbers about it. The file `sample.txt` sits
next to this script. Always open text files with encoding="utf-8".
"""

from pathlib import Path

SAMPLE = Path(__file__).parent / "sample.txt"


def count_lines(path: Path) -> int:
    """Return the number of lines in the file. An empty file has 0 lines.

    A last line without a final newline still counts.
    """
    with open(path, encoding="utf-8") as f:
        return sum(1 for _ in f)


def count_words(path: Path) -> int:
    """Return the number of whitespace-separated words in the file."""
    return len(Path(path).read_text(encoding="utf-8").split())


def count_chars(path: Path) -> int:
    """Return the number of characters (not bytes) in the file, newlines included.

    "Café" counts as 4 characters even though it needs 5 bytes in UTF-8.
    """
    return len(Path(path).read_text(encoding="utf-8"))


def longest_line(path: Path) -> str:
    """Return the longest line without its newline.
    If several lines tie, return the first one. For an empty file return "".
    """
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return max(lines, key=len, default="")


def report(path: Path) -> str:
    """Return a one-line summary: "<name>: <lines> lines, <words> words, <chars> chars".

    <name> is the file name only, not the folder.
    report(Path("sample.txt"))  -> "sample.txt: 5 lines, 17 words, 82 chars"
    """
    path = Path(path)
    return (
        f"{path.name}: {count_lines(path)} lines, "
        f"{count_words(path)} words, {count_chars(path)} chars"
    )


if __name__ == "__main__":
    print(report(SAMPLE))
