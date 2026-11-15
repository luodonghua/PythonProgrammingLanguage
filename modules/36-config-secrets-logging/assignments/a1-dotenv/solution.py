"""Assignment 1: parse the text of a .env file.

A ``.env`` file keeps settings for one machine, one per line:

    # database settings
    export DB_HOST=localhost
    DB_NAME = "my app"
    DEBUG=true   # turn off in production
"""

import re

KEY_PATTERN = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def parse_dotenv(text: str) -> dict[str, str]:
    """Parse ``text`` and return a dict of names to string values.

    Rules, applied line by line (line numbers start at 1):

    * Leading and trailing spaces of a line are ignored.
    * Blank lines and lines that start with ``#`` are skipped.
    * An optional ``export `` prefix is removed.
    * Split at the FIRST ``=``. The name (stripped) must match
      ``[A-Za-z_][A-Za-z0-9_]*``, otherwise raise ``ValueError`` whose message
      starts with ``"line N:"`` (N is the line number). A line without ``=``
      is also a ``ValueError`` in that form.
    * The value is stripped. If it starts and ends with the same quote
      character (``"`` or ``'``) and has at least two characters, remove the
      quotes and keep everything inside exactly (including ``#`` and spaces).
    * Otherwise it is an unquoted value: remove an inline comment, which starts
      at the first ``#`` that is at the start of the value or has whitespace
      before it, and strip again.
    * If a name appears twice, the later value wins.
    """
    result: dict[str, str] = {}
    for number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        line = line.removeprefix("export ").lstrip()
        name, sep, value = line.partition("=")
        name = name.strip()
        if not sep:
            raise ValueError(f"line {number}: expected NAME=value")
        if not KEY_PATTERN.fullmatch(name):
            raise ValueError(f"line {number}: invalid name {name!r}")
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        else:
            value = re.split(r"(?:^|\s)#", value, maxsplit=1)[0].strip()
        result[name] = value
    return result


if __name__ == "__main__":
    sample = 'export HOST=localhost\nNAME = "my app"  \nDEBUG=true   # dev only\n'
    print(parse_dotenv(sample))
