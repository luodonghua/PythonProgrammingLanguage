"""Assignment 2: Reading and writing text files.

Practises `open()` modes ("r", "w", "a"), `with`, iterating over lines and
encoding="utf-8". All functions take paths, so tests can use temporary folders.
"""

from pathlib import Path


def read_lines(path: Path) -> list[str]:
    """Return the non-blank lines of the file, each stripped of outer whitespace.

    File "  a \n\n b\n   \n"  -> ["a", "b"]
    """
    with open(path, encoding="utf-8") as f:
        stripped = (line.strip() for line in f)
        return [line for line in stripped if line]


def write_report(path: Path, rows: list[tuple[str, float]]) -> int:
    """Write one line per (name, amount) row, as "<name>: <amount:.2f>",
    and finish with a line "Total: <sum:.2f>". Every line ends with "\\n".
    Return the number of lines written. Overwrite an existing file.

    write_report(p, [("tea", 3), ("cake", 4.5)]) writes
        tea: 3.00
        cake: 4.50
        Total: 7.50
    and returns 3. With no rows it writes only "Total: 0.00" and returns 1.
    """
    lines = [f"{name}: {amount:.2f}" for name, amount in rows]
    lines.append(f"Total: {sum(amount for _, amount in rows):.2f}")
    with open(path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
    return len(lines)


def append_log(path: Path, message: str) -> None:
    """Append `message` plus a newline to the file. Create the file if needed.
    Earlier content must stay.
    """
    with open(path, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def copy_uppercase(src: Path, dst: Path) -> int:
    """Copy `src` to `dst` with all text in upper case. Return the number of lines.
    Read and write line by line (the file might be big).

    "Café\nok\n"  ->  "CAFÉ\nOK\n"  and the return value is 2.
    """
    count = 0
    with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
        for line in fin:
            fout.write(line.upper())
            count += 1
    return count


def tail(path: Path, n: int = 3) -> list[str]:
    """Return the last `n` lines of the file without their newlines.
    If the file has fewer lines, return all of them. n <= 0 returns [].
    """
    if n <= 0:
        return []
    with open(path, encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return lines[-n:]


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        target = Path(folder) / "report.txt"
        print(write_report(target, [("tea", 3), ("cake", 4.5)]))
