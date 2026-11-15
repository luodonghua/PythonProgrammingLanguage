---
layout: module
module: 19-dates-and-times
kind: learn
title: Dates and times
permalink: /modules/19-dates-and-times/
---

<div class="box key" markdown="1">

## Key learning points

- The `datetime` module has `date`, `time`, `datetime` and `timedelta`. Subtracting two dates gives a `timedelta`. Adding a `timedelta` to a date gives a new date.
- `strftime` turns a value into text with format codes such as `%Y-%m-%d`. `strptime` parses text into a `datetime`. For ISO 8601 text use `isoformat()` and `fromisoformat()`.
- A **naive** datetime has no time zone. An **aware** datetime has one. You cannot compare or subtract the two kinds.
- Store and compute in **UTC**. Convert to a local zone with `zoneinfo.ZoneInfo` only when you show a time to people.
- Daylight saving time (DST) makes some local times missing or repeated, and "one day later" can be 23 or 25 hours.
- Do not call `date.today()` deep inside your logic. Pass `today` in as a parameter so the code is easy to test.

</div>

## 1. date, time, datetime and timedelta

```python
from datetime import date, time, datetime, timedelta

d = date(2025, 3, 14)
print(d, d.year, d.month, d.day)
print(d.weekday(), d.isoweekday())
```

```text
2025-03-14 2025 3 14
4 5
```

`weekday()` counts Monday as 0. `isoweekday()` counts Monday as 1. March 14, 2025 is a Friday.

```python
dt = datetime(2025, 3, 14, 9, 30, 15)
print(dt, dt.date(), dt.time())
print(time(9, 30, 15))
```

```text
2025-03-14 09:30:15 2025-03-14 09:30:15
09:30:15
```

### timedelta

A `timedelta` is a length of time. It stores days, seconds and microseconds.

```python
td = timedelta(hours=1, minutes=30)
print(td, td.total_seconds())
print(dt + td)
print(date(2025, 12, 25) - d)
print((date(2025, 12, 25) - d).days)
```

```text
1:30:00 5400.0
2025-03-14 11:00:15
286 days, 0:00:00
286
```

`timedelta` has no months or years, because their length varies. For "next month" logic, work with `date.year` and `date.month` yourself, or use `calendar` (section 5).

## 2. Formatting and parsing

```python
print(dt.strftime("%Y-%m-%d %H:%M"))
print(dt.strftime("%A %d %B %Y"))
print(dt.strftime("%I:%M %p"))
```

```text
2025-03-14 09:30
Friday 14 March 2025
09:30 AM
```

| Code | Meaning |
|---|---|
| `%Y` `%m` `%d` | year, month, day (zero-padded) |
| `%H` `%M` `%S` | hour (24h), minute, second |
| `%I` `%p` | hour (12h), AM or PM |
| `%A` `%B` | weekday name, month name |

`strptime` goes the other way. The format must match the text exactly, or it raises `ValueError`.

```python
p = datetime.strptime("14/03/2025 18:05", "%d/%m/%Y %H:%M")
print(p)
```

```text
2025-03-14 18:05:00
```

Names such as `%A` and `%B` depend on the locale, so prefer ISO format for data you store or exchange:

```python
print(dt.isoformat())
print(datetime.fromisoformat("2025-03-14T09:30:15"))
print(date.fromisoformat("2025-03-14"))
```

```text
2025-03-14T09:30:15
2025-03-14 09:30:15
2025-03-14
```

## 3. Naive and aware datetimes

A datetime without `tzinfo` is naive. It does not say which time zone it is in. An aware datetime carries an offset from UTC.

```python
from datetime import UTC

naive = datetime(2025, 3, 14, 9, 0)
aware = datetime(2025, 3, 14, 9, 0, tzinfo=UTC)
print(naive.tzinfo, aware.tzinfo)
print(aware)
try:
    naive < aware
except TypeError as exc:
    print(exc)
```

```text
None UTC
2025-03-14 09:00:00+00:00
can't compare offset-naive and offset-aware datetimes
```

Get the current time as an aware UTC value with `datetime.now(UTC)`. Avoid `datetime.utcnow()`: it returns a naive value, and it is deprecated since Python 3.12.

`aware.isoformat()` includes the offset (`2025-03-14T09:00:00+00:00`), and `fromisoformat` reads it back.

## 4. Time zones with zoneinfo

`zoneinfo` (standard library since Python 3.9) knows the IANA zone names, such as `America/New_York`. It reads the system time zone database. On Windows the database is missing, so install the `tzdata` package (`uv add tzdata`).

```python
from zoneinfo import ZoneInfo

ny = ZoneInfo("America/New_York")
paris = ZoneInfo("Europe/Paris")

meeting = datetime(2025, 3, 14, 9, 0, tzinfo=ny)
print(meeting)
print(meeting.astimezone(paris))
print(meeting.astimezone(UTC))
```

```text
2025-03-14 09:00:00-04:00
2025-03-14 14:00:00+01:00
2025-03-14 13:00:00+00:00
```

`astimezone(zone)` converts the same moment into another zone. Pass the zone to the constructor with `tzinfo=` for a new value. Do not use `.replace(tzinfo=...)` on a value that already has the wrong zone, because it relabels the clock time without converting it.

### DST pitfalls

New York clocks jumped forward on March 9, 2025, so that day has only 23 hours.

```python
before = datetime(2025, 3, 8, 12, 0, tzinfo=ny)
after = before + timedelta(days=1)
print(after)
print(after - before)
print(after.astimezone(UTC) - before.astimezone(UTC))
```

```text
2025-03-09 12:00:00-04:00
1 day, 0:00:00
23:00:00
```

Arithmetic on aware values in the same zone works on the wall clock, so "plus one day" gives noon again. Real elapsed time is 23 hours. To measure elapsed time, convert both values to UTC first.

Local times can also be missing or repeated:

```python
gap = datetime(2025, 3, 9, 2, 30, tzinfo=ny)      # this time never happened
print(gap.astimezone(UTC).astimezone(ny))

amb = datetime(2025, 11, 2, 1, 30, tzinfo=ny)    # this time happened twice
print(amb.utcoffset(), amb.replace(fold=1).utcoffset())
```

```text
2025-03-09 03:30:00-04:00
-1 day, 20:00:00 -1 day, 19:00:00
```

The `fold` attribute picks the first (`0`) or second (`1`) occurrence of a repeated time. The offsets above are -4 hours and -5 hours.

**Rule:** store timestamps in UTC (or ISO text with an offset). Convert to a local zone only for display.

## 5. The calendar module

```python
import calendar

print(calendar.isleap(2024))
print(calendar.monthrange(2025, 2)[1])      # days in February 2025
print(calendar.month_name[3], calendar.day_name[0])
```

```text
True
28
March Monday
```

`calendar.monthrange(year, month)` returns the weekday of the first day and the number of days in the month.

## 6. Testing time-dependent code

Code that calls `date.today()` gives different answers every day. Pass the date in:

```python
def age_on(birthday: date, today: date) -> int:
    had_birthday = (today.month, today.day) >= (birthday.month, birthday.day)
    return today.year - birthday.year - (not had_birthday)


print(age_on(date(2000, 6, 15), today=date(2025, 6, 14)))
print(age_on(date(2000, 6, 15), today=date(2025, 6, 15)))
```

```text
24
25
```

Give `today` a default only at the top level, for example `today = today or date.today()` in the function that the user calls.

<div class="box warn" markdown="1">

## Common mistakes

- **Mixing naive and aware values.** Comparing or subtracting them raises `TypeError`. Make everything aware.
- **Using `datetime.now()` for stored data.** It gives local naive time. Use `datetime.now(UTC)`.
- **Using `.replace(tzinfo=...)` to convert.** It changes the label, not the moment. Use `astimezone`.
- **Treating a day as 24 hours.** DST days have 23 or 25. Compute elapsed time in UTC.
- **Assuming `strptime` is forgiving.** `"2025-3-5"` parses with `%Y-%m-%d`, but `"2025/03/05"` does not.
- **Adding 365 days for "a year".** Leap years break this. Use `date.replace(year=...)` and handle February 29 on purpose.

</div>

## Try it yourself

1. Print how many days remain until December 31 of this year, starting from `date.today()`.
2. Parse `"2025-07-04 15:00"` as a New York time and print it in Tokyo time (`Asia/Tokyo`).
3. Find out what `datetime(2025, 1, 31) + timedelta(days=30)` gives, and write down why "one month later" has no single answer.

## Further reading

- [datetime](https://docs.python.org/3/library/datetime.html)
- [zoneinfo](https://docs.python.org/3/library/zoneinfo.html)
- [calendar](https://docs.python.org/3/library/calendar.html)

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="19-dates-and-times:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/19-dates-and-times/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/19-dates-and-times/assignments/' | relative_url }}).
