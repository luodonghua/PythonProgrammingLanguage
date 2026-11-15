"""Assignment 3: Convert times between time zones.

Use zoneinfo.ZoneInfo with IANA names such as "America/New_York".
"""

from datetime import datetime


def convert_time(text: str, from_zone: str, to_zone: str) -> str:
    """Convert a local time to another zone and return it as ISO text.

    `text` has the form "YYYY-MM-DD HH:MM" and is a wall-clock time in
    `from_zone`. Return the same moment in `to_zone` as
    datetime.isoformat(timespec="minutes"), for example
    convert_time("2025-03-14 09:00", "America/New_York", "Europe/Paris")
    returns "2025-03-14T14:00+01:00".

    Raise ValueError for text that does not match the format. An unknown zone
    name raises zoneinfo.ZoneInfoNotFoundError, which you do not need to catch.
    """
    # TODO: strptime, attach the zone with tzinfo=, then astimezone().
    ...


def to_utc(text: str, zone: str) -> datetime:
    """Parse "YYYY-MM-DD HH:MM" as a time in `zone` and return an aware
    datetime in UTC (tzinfo is datetime.UTC)."""
    # TODO: reuse the same steps and convert to UTC.
    ...


def elapsed_hours(start: str, end: str, zone: str) -> float:
    """Return the real hours between two local times in `zone`.

    Both texts have the form "YYYY-MM-DD HH:MM". Daylight saving changes count:
    in America/New_York, "2025-03-09 00:00" to "2025-03-10 00:00" is 23.0 hours.
    Return a negative number if `end` is before `start`.
    """
    # TODO: convert both to UTC first, then subtract and use total_seconds().
    ...


if __name__ == "__main__":
    print(convert_time("2025-03-14 09:00", "America/New_York", "Europe/Paris"))
    print(elapsed_hours("2025-03-09 00:00", "2025-03-10 00:00", "America/New_York"))
