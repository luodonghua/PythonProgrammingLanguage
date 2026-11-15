"""Assignment 1: Build URLs and read a raw request line.

Practise urllib.parse. Do not join query strings by hand.
"""

from urllib.parse import parse_qs, urlencode, urlsplit  # noqa: F401  (use these)


def build_url(base: str, path: str, params: dict | None = None) -> str:
    """Join a base URL, a path and optional query parameters.

    - Exactly one "/" separates base and path, whatever slashes you pass in:
      build_url("https://api.example.com/", "/v1/items") and
      build_url("https://api.example.com", "v1/items") both give
      "https://api.example.com/v1/items".
    - params is a dict. Entries whose value is None are skipped.
      A list value repeats the key: {"tag": ["a", "b"]} -> "tag=a&tag=b".
    - Values are percent-encoded (a space becomes "+").
    - If there are no parameters left, do not add a "?".
    """
    # TODO: use urlencode(..., doseq=True) and string joining for the path.
    ...


def parse_request_line(line: str) -> dict:
    """Split an HTTP request line into its parts.

    "GET /search?q=cat+food&page=2 HTTP/1.1" returns
    {"method": "GET", "path": "/search",
     "query": {"q": "cat food", "page": "2"}, "version": "HTTP/1.1"}

    - query maps each key to its FIRST value (a plain string).
    - Raise ValueError if the line does not have exactly three
      space-separated parts, if the method is not upper-case letters only,
      or if the version does not start with "HTTP/".
    """
    # TODO: split the line, validate it, then use urlsplit and parse_qs.
    ...


if __name__ == "__main__":
    print(build_url("https://api.example.com/", "/v1/items", {"q": "a b", "page": 2}))
    print(parse_request_line("GET /search?q=cat+food&page=2 HTTP/1.1"))
