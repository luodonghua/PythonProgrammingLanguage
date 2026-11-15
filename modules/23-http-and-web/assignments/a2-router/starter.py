"""Assignment 2: A router and a raw HTTP response, with no server at all.

A web framework is mostly a function from (method, path) to a response.
Write that function as plain Python so it is easy to test.
"""

import json  # noqa: F401  (use it in to_http_response)
from http import HTTPStatus  # noqa: F401  (HTTPStatus(200).phrase == "OK")
from urllib.parse import parse_qs, urlsplit  # noqa: F401


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
    # TODO: split the target with urlsplit, then decide the response.
    ...


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
    # TODO: encode the body first, so Content-Length counts bytes, not characters.
    ...


if __name__ == "__main__":
    print(route("GET", "/hello/Ada"))
    print(to_http_response(*route("GET", "/add?a=2&b=3")).decode())
