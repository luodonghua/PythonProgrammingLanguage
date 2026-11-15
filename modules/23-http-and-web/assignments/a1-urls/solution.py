"""Assignment 1: Build URLs and read a raw request line.

Practise urllib.parse. Do not join query strings by hand.
"""

from urllib.parse import parse_qs, urlencode, urlsplit


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
    url = base.rstrip("/") + "/" + path.lstrip("/")
    kept = {k: v for k, v in (params or {}).items() if v is not None}
    if kept:
        url += "?" + urlencode(kept, doseq=True)
    return url


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
    parts = line.split(" ")
    if len(parts) != 3:
        raise ValueError(f"bad request line: {line!r}")
    method, target, version = parts
    if not (method.isascii() and method.isalpha() and method.isupper()):
        raise ValueError(f"bad method: {method!r}")
    if not version.startswith("HTTP/"):
        raise ValueError(f"bad version: {version!r}")
    split = urlsplit(target)
    query = {key: values[0] for key, values in parse_qs(split.query).items()}
    return {"method": method, "path": split.path, "query": query, "version": version}


if __name__ == "__main__":
    print(build_url("https://api.example.com/", "/v1/items", {"q": "a b", "page": 2}))
    print(parse_request_line("GET /search?q=cat+food&page=2 HTTP/1.1"))
