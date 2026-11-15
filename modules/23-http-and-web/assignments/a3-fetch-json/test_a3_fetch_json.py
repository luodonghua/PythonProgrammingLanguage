import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

import pytest

from practice import load

m = load(__file__)

ITEMS = [{"id": 1, "name": "pen"}, {"id": 2, "name": "ink"}]


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body: bytes, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parts = urlsplit(self.path)
        if parts.path == "/items":
            self._send(200, json.dumps(ITEMS).encode())
        elif parts.path == "/query":
            self._send(200, json.dumps(parse_qs(parts.query)).encode())
        elif parts.path == "/headers":
            seen = {"accept": self.headers.get("Accept"), "token": self.headers.get("X-Token")}
            self._send(200, json.dumps(seen).encode())
        elif parts.path == "/broken":
            self._send(200, b"<html>not json</html>", "text/html")
        elif parts.path == "/boom":
            self._send(500, b'{"error": "boom"}')
        else:
            self._send(404, b'{"error": "not found"}')

    def log_message(self, format, *args):
        pass


@pytest.fixture
def base():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_address[1]}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def test_fetch_json_returns_decoded_body(base):
    assert m.fetch_json(base + "/items") == ITEMS


def test_params_are_encoded(base):
    result = m.fetch_json(base + "/query", params={"q": "a b", "n": 2})
    assert result == {"q": ["a b"], "n": ["2"]}


def test_params_appended_to_existing_query(base):
    result = m.fetch_json(base + "/query?x=1", params={"y": "2"})
    assert result == {"x": ["1"], "y": ["2"]}


def test_default_accept_header(base):
    assert m.fetch_json(base + "/headers")["accept"] == "application/json"


def test_custom_headers_are_sent(base):
    result = m.fetch_json(base + "/headers", headers={"X-Token": "abc", "Accept": "text/plain"})
    assert result == {"accept": "text/plain", "token": "abc"}


@pytest.mark.parametrize(("path", "status"), [("/missing", 404), ("/boom", 500)])
def test_http_errors_become_api_error(base, path, status):
    with pytest.raises(m.ApiError) as info:
        m.fetch_json(base + path)
    assert info.value.status == status


def test_invalid_json(base):
    with pytest.raises(m.ApiError) as info:
        m.fetch_json(base + "/broken")
    assert info.value.status == 200
    assert "invalid JSON" in str(info.value)


def test_unreachable_server():
    # Start and stop a server to get a port that nothing listens on.
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    server.server_close()
    with pytest.raises(m.ApiError) as info:
        m.fetch_json(f"http://127.0.0.1:{port}/", timeout=2)
    assert info.value.status is None


def test_fetch_item_names(base):
    assert m.fetch_item_names(base) == ["pen", "ink"]
