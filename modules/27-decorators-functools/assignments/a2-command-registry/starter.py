"""Assignment 2: a command registry.

``COMMANDS`` is a dict that maps a command name to a function.

``command`` registers a function in ``COMMANDS`` and returns the function
unchanged. It works in two forms:

* ``@command``          registers under ``func.__name__``
* ``@command("name")``  registers under the given name

``run(line)`` runs one command line:

* split ``line`` on whitespace; the first word is the command name, the rest
  are string arguments passed to the function
* return what the function returns
* an empty or blank line returns ``""``
* an unknown name returns ``"unknown command: <name>"``
"""

COMMANDS = {}


def command(arg):
    """Register a function as a command (with or without a name)."""
    # TODO
    ...


def run(line):
    """Run one command line and return its result."""
    # TODO
    ...


if __name__ == "__main__":

    @command
    def hello(name):
        return f"hello {name}"

    @command("bye")
    def goodbye(name):
        return f"bye {name}"

    print(run("hello Ada"))
    print(run("bye Ada"))
    print(run("dance"))
