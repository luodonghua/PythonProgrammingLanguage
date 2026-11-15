"""Assignment 1: Hello, you."""


def greet(name: str) -> str:
    """Return 'Hello, <name>!'.

    Surrounding spaces in the name are ignored. If the name is empty
    (or only spaces), greet the world instead: 'Hello, world!'.
    """
    name = name.strip()
    if not name:
        name = "world"
    return f"Hello, {name}!"


def main() -> None:
    print(greet("Python"))


if __name__ == "__main__":
    main()
