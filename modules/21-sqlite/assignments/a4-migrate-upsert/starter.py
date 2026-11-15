"""Assignment 4: Schema migrations and upserts.

A migration list holds SQL steps. The database remembers how many steps it has
already run in `PRAGMA user_version` (an integer kept inside the database
file). Running `migrate` on an old database brings it up to date, and running
it again does nothing.
"""

import sqlite3

MIGRATIONS = [
    # step 1
    "CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
    # step 2
    "ALTER TABLE settings ADD COLUMN updates INTEGER NOT NULL DEFAULT 0",
    # step 3
    "CREATE INDEX idx_settings_value ON settings(value)",
]


def get_version(conn: sqlite3.Connection) -> int:
    """Return PRAGMA user_version (0 for a brand-new database)."""
    # TODO: conn.execute("PRAGMA user_version").fetchone()[0]
    ...


def migrate(conn: sqlite3.Connection, migrations: list[str] = MIGRATIONS) -> int:
    """Apply every migration step that has not run yet and return how many
    steps were applied in this call.

    - A database at version v needs steps v+1 ... len(migrations).
    - After each step, set PRAGMA user_version to that step's number and
      commit. PRAGMA cannot take ? parameters, so build the text with an int:
      f"PRAGMA user_version = {number}".
    - A database that is already up to date: apply nothing and return 0.
    """
    # TODO: loop over migrations[version:], execute each, set the version.
    ...


def upsert_setting(conn: sqlite3.Connection, key: str, value: str) -> None:
    """Store a setting. If the key is new, insert it with updates = 0.
    If it exists, replace the value and add 1 to `updates`.

    Use one statement: INSERT ... ON CONFLICT(key) DO UPDATE SET ...
    The database must already be migrated to version 2 or later.
    """
    # TODO: INSERT with ON CONFLICT(key) DO UPDATE, inside `with conn:`.
    ...


def get_setting(conn: sqlite3.Connection, key: str, default: str | None = None) -> str | None:
    """Return the value of a setting, or `default` when the key does not exist."""
    # TODO: SELECT value FROM settings WHERE key = ?
    ...


def setting_updates(conn: sqlite3.Connection, key: str) -> int | None:
    """Return how many times the setting was replaced, or None if the key is unknown."""
    # TODO: SELECT updates FROM settings WHERE key = ?
    ...


if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    print(migrate(db), get_version(db))
    upsert_setting(db, "theme", "dark")
    upsert_setting(db, "theme", "light")
    print(get_setting(db, "theme"), setting_updates(db, "theme"))
