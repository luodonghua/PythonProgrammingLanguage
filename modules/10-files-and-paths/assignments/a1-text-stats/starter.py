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
    # TODO: open the file with `with` and iterate over it.
    ...


def count_words(path: Path) -> int:
    """Return the number of whitespace-separated words in the file."""
    # TODO: read the whole text and use str.split().
    ...


def count_chars(path: Path) -> int:
    """Return the number of characters (not bytes) in the file, newlines included.

    "Café" counts as 4 characters even though it needs 5 bytes in UTF-8.
    """
    # TODO: read_text(encoding="utf-8") and take len().
    ...


def longest_line(path: Path) -> str:
    """Return the longest line without its newline.
    If several lines tie, return the first one. For an empty file return "".
    """
    # TODO: strip the trailing newline from each line, then use max(..., key=len).
    ...


def report(path: Path) -> str:
    """Return a one-line summary: "<name>: <lines> lines, <words> words, <chars> chars".

    <name> is the file name only, not the folder.
    report(Path("sample.txt"))  -> "sample.txt: 5 lines, 17 words, 82 chars"
    """
    # TODO: combine the functions above and path.name.
    ...


if __name__ == "__main__":
    print(report(SAMPLE))
