"""Assignment 4: a cache whose entries expire.

``ttl_cache(seconds, clock=time.monotonic)`` returns a decorator.

The decorated function remembers its result for each distinct combination of
arguments (positional and keyword, all hashable). A stored result is used again
while it is *younger than* ``seconds``. When ``clock() - stored_at >= seconds``
the entry is expired: call the function again and store the new result with
the current time.

* ``clock`` is a function returning the current time in seconds. Tests pass a
  fake one.
* Call ``clock()`` once per call of the decorated function.
* Keep the metadata of the function (functools.wraps).
* Add ``wrapper.cache_clear()`` which forgets every entry.
* Add ``wrapper.hits`` and ``wrapper.misses``: counters of calls answered from
  the cache and calls that ran the function. Both start at 0 and
  ``cache_clear()`` resets them too.
* ``f(1, 2)`` and ``f(a=1, b=2)`` may be treated as different keys.
"""

import functools
import time


def ttl_cache(seconds, clock=time.monotonic):
    """Return a decorator that caches results for ``seconds``."""
    # TODO
    ...


if __name__ == "__main__":
    now = [0.0]

    @ttl_cache(10, clock=lambda: now[0])
    def square(n):
        print("computing", n)
        return n * n

    print(square(4))
    print(square(4))
    now[0] = 11.0
    print(square(4))
