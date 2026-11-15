"""Assignment 4: A tiny text-adventure command parser."""

DIRECTIONS = {"north", "south", "east", "west"}


def parse(text: str) -> tuple:
    """Turn a typed command into a tuple. Ignore case and extra spaces.

    ""                    -> ("noop",)
    "quit" or "exit"      -> ("quit",)
    "look"                -> ("look",)
    "go north"            -> ("move", "north")     (only the four DIRECTIONS)
    "take brass lamp"     -> ("take", "brass lamp") (one or more words)
    anything else         -> ("unknown", <the text with outer spaces removed>)

    Use `match words:` where words = text.lower().split(), with sequence
    patterns such as  case ["go", direction] if direction in DIRECTIONS:
    and a star pattern such as  case ["take", first, *rest]:
    """
    words = text.lower().split()
    match words:
        case []:
            return ("noop",)
        case ["quit"] | ["exit"]:
            return ("quit",)
        case ["look"]:
            return ("look",)
        case ["go", direction] if direction in DIRECTIONS:
            return ("move", direction)
        case ["take", first, *rest]:
            return ("take", " ".join([first, *rest]))
        case _:
            return ("unknown", text.strip())


if __name__ == "__main__":
    for line in ("look", "GO North", "take brass lamp", "dance"):
        print(line, "->", parse(line))
