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
    # TODO: loop over text.splitlines() and apply the rules above.
    ...


if __name__ == "__main__":
    sample = 'export HOST=localhost\nNAME = "my app"  \nDEBUG=true   # dev only\n'
    print(parse_dotenv(sample))
