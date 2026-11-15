"""Assignment 2: A router and a raw HTTP response, with no server at all.

A web framework is mostly a function from (method, path) to a response.
Write that function as plain Python so it is easy to test.
"""

import json
from http import HTTPStatus
from urllib.parse import parse_qs, urlsplit


def route(method: str, target: str) -> tuple[int, dict]:
    """Return (status_code, payload_dict) for a request.

    `target` is the path plus an optional query, e.g. "/add?a=2&b=3".

    Routes (all answer JSON dicts):
      GET /                -> 200, {"status": "ok"}
      GET /hello/<name>    -> 200, {"message": "Hello, <name>!"}
                              (<name> is one non-empty path segment)
      GET /add?a=..&b=..   -> 200, {"sum": a + b}   with a and b as ints
                              400, {"error": "a and b must be integers"} if
                              either is missing or not an integer

    Errors:
      A known path used with another method -> 405, {"error": "method not allowed"}
      Any other path                        -> 404, {"error": "not found"}

    "Known path" means "/", "/add", or "/hello/<name>".
    """
    parts = urlsplit(target)
    path = parts.path
    segments = path.split("/")  # "/hello/Ada" -> ["", "hello", "Ada"]

    if path == "/":
        handler = _home
    elif path == "/add":
        handler = _add
    elif len(segments) == 3 and segments[1] == "hello" and segments[2]:
        handler = _hello
    else:
        return 404, {"error": "not found"}

    if method != "GET":
        return 405, {"error": "method not allowed"}
    return handler(segments, parse_qs(parts.query))


def _home(segments: list[str], query: dict) -> tuple[int, dict]:
    return 200, {"status": "ok"}


def _hello(segments: list[str], query: dict) -> tuple[int, dict]:
    return 200, {"message": f"Hello, {segments[2]}!"}


def _add(segments: list[str], query: dict) -> tuple[int, dict]:
    try:
        total = int(query["a"][0]) + int(query["b"][0])
    except (KeyError, ValueError):
        return 400, {"error": "a and b must be integers"}
    return 200, {"sum": total}


def to_http_response(status: int, payload: dict) -> bytes:
    """Build the raw bytes of an HTTP/1.1 response with a JSON body.

    The text is, with "\\r\\n" line endings:

        HTTP/1.1 <status> <phrase>
        Content-Type: application/json
        Content-Length: <number of BYTES in the body>
        <empty line>
        <body>

    The body is json.dumps(payload) encoded as UTF-8. The phrase comes from
    http.HTTPStatus (200 -> "OK", 404 -> "Not Found").
    """
    body = json.dumps(payload).encode("utf-8")
    head = (
        f"HTTP/1.1 {status} {HTTPStatus(status).phrase}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        "\r\n"
    )
    return head.encode("ascii") + body


if __name__ == "__main__":
    print(route("GET", "/hello/Ada"))
    print(to_http_response(*route("GET", "/add?a=2&b=3")).decode())
