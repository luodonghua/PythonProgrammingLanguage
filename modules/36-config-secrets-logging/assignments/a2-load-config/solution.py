"""Assignment 2: load settings from environment variables into a frozen dataclass.

Settings come from outside the program (``os.environ``). Read them once, check
them, and turn them into typed values. Report ALL problems together, so a user
can fix the whole setup in one go.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field

TRUE_WORDS = {"1", "true", "yes", "on"}
FALSE_WORDS = {"0", "false", "no", "off"}


class ConfigError(Exception):
    """Raised for invalid settings. ``problems`` lists one message per problem."""

    def __init__(self, problems: list[str]):
        super().__init__("; ".join(problems))
        self.problems = problems


@dataclass(frozen=True)
class Config:
    api_key: str = field(repr=False)  # a secret: never shown in repr()
    app_name: str = "app"
    port: int = 8000
    debug: bool = False
    timeout: float = 5.0


def parse_bool(text: str) -> bool:
    """Convert ``text`` to a bool, ignoring case and outer spaces.

    "1", "true", "yes", "on" give True. "0", "false", "no", "off" give False.
    Anything else raises ``ValueError``.
    """
    word = text.strip().lower()
    if word in TRUE_WORDS:
        return True
    if word in FALSE_WORDS:
        return False
    raise ValueError(f"not a boolean: {text!r}")


def load_config(env: Mapping[str, str]) -> Config:
    """Build a ``Config`` from a mapping such as ``os.environ``.

    Variable          Field       Rule
    API_KEY           api_key     required, not empty after stripping spaces
    APP_NAME          app_name    default "app"
    PORT              port        int from 1 to 65535, default 8000
    DEBUG             debug       ``parse_bool``, default False
    TIMEOUT           timeout     float greater than 0, default 5.0

    A variable that is missing uses its default. A variable that is present but
    invalid is a problem, even when a default exists. Collect one message per
    problem; each message must contain the variable name (for example
    ``"PORT must be an integer from 1 to 65535"``). If there is at least one
    problem, raise ``ConfigError(problems)``. Do not stop at the first problem.
    """
    problems: list[str] = []
    values: dict = {}

    api_key = env.get("API_KEY", "").strip()
    if api_key:
        values["api_key"] = api_key
    else:
        problems.append("API_KEY is required")

    if "APP_NAME" in env:
        values["app_name"] = env["APP_NAME"]

    if "PORT" in env:
        try:
            port = int(env["PORT"])
            if not 1 <= port <= 65535:
                raise ValueError
            values["port"] = port
        except ValueError:
            problems.append("PORT must be an integer from 1 to 65535")

    if "DEBUG" in env:
        try:
            values["debug"] = parse_bool(env["DEBUG"])
        except ValueError:
            problems.append("DEBUG must be true or false")

    if "TIMEOUT" in env:
        try:
            timeout = float(env["TIMEOUT"])
            if not timeout > 0:
                raise ValueError
            values["timeout"] = timeout
        except ValueError:
            problems.append("TIMEOUT must be a number greater than 0")

    if problems:
        raise ConfigError(problems)
    return Config(**values)


if __name__ == "__main__":
    print(load_config({"API_KEY": "sk-secret-123", "PORT": "9000", "DEBUG": "yes"}))
    try:
        load_config({"PORT": "99999", "DEBUG": "maybe"})
    except ConfigError as exc:
        print(exc.problems)
