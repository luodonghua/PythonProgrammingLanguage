"""Assignment 4: A tiny JSON echo server with http.server.

Write the handler. The tests start it on 127.0.0.1 with a free port and send
real requests to it. Nothing leaves your computer.
"""

import json  # noqa: F401
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def send_json(handler: BaseHTTPRequestHandler, status: int, payload) -> None:
    """Send a complete JSON response through `handler`.

    Call, in this order: handler.send_response(status), then the headers
    "Content-Type: application/json" and "Content-Length: <bytes in body>",
    then handler.end_headers(), then write the body to handler.wfile.
    The body is json.dumps(payload) encoded as UTF-8.
    """
    # TODO
    ...


class EchoHandler(BaseHTTPRequestHandler):
    """Routes:

    GET  /health -> 200 {"status": "ok"}
    POST /echo   -> read the body (its size is the Content-Length header).
                    Valid JSON      -> 200 {"received": <the decoded JSON>, "length": <body size in bytes>}
                    Invalid JSON, or empty body -> 400 {"error": "invalid JSON"}
    Any other path (any method)     -> 404 {"error": "not found"}
    GET /echo or POST /health       -> 405 {"error": "method not allowed"}
    """

    def do_GET(self):
        # TODO: answer /health, /echo (405) and everything else (404).
        ...

    def do_POST(self):
        # TODO: answer /echo, /health (405) and everything else (404).
        # Read the body with self.rfile.read(length).
        # json.loads raises json.JSONDecodeError (a ValueError) on bad input.
        ...

    def log_message(self, format, *args):
        """Keep the test output quiet."""


def make_server(host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    """Create (but do not start) a server. Port 0 means 'any free port'."""
    return ThreadingHTTPServer((host, port), EchoHandler)


if __name__ == "__main__":
    server = make_server(port=8000)
    print("Serving on http://127.0.0.1:8000  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
