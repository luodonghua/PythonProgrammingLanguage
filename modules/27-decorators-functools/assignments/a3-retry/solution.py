"""Assignment 3: retry with exponential backoff.

``retry(times, exceptions=(Exception,), delay=1.0, backoff=2.0, sleep=time.sleep)``
returns a decorator.

The decorated function is called up to ``times`` times in total (so
``times=3`` means one first try and two retries).

* If the call returns, return its result at once.
* If it raises an exception that is an instance of ``exceptions``, wait and try
  again. The first wait is ``delay`` seconds; every later wait is multiplied by
  ``backoff`` (1.0, 2.0, 4.0 with the defaults). Waiting means calling
  ``sleep(seconds)``.
* After the last failed attempt, re-raise that last exception. Do not sleep
  after the last attempt.
* An exception that is NOT in ``exceptions`` propagates at once, with no sleep
  and no retry.

``sleep`` is a parameter so that tests do not have to wait.
Keep ``__name__`` and ``__doc__`` of the function (functools.wraps).
"""

import functools
import time


def retry(times, exceptions=(Exception,), delay=1.0, backoff=2.0, sleep=time.sleep):
    """Return a decorator that retries a failing function."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
                    sleep(wait)
                    wait *= backoff

        return wrapper

    return decorator


if __name__ == "__main__":
    attempts = []

    @retry(3, exceptions=(ConnectionError,), delay=0.0)
    def flaky():
        attempts.append(1)
        if len(attempts) < 3:
            raise ConnectionError("down")
        return "ok"

    print(flaky(), "after", len(attempts), "attempts")
