import json

import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("method", "target", "expected"),
    [
        ("GET", "/", (200, {"status": "ok"})),
        ("GET", "/hello/Ada", (200, {"message": "Hello, Ada!"})),
        ("GET", "/add?a=2&b=3", (200, {"sum": 5})),
        ("GET", "/add?a=-4&b=10", (200, {"sum": 6})),
        ("GET", "/add?a=2", (400, {"error": "a and b must be integers"})),
        ("GET", "/add?a=x&b=3", (400, {"error": "a and b must be integers"})),
        ("GET", "/add", (400, {"error": "a and b must be integers"})),
        ("GET", "/nothing", (404, {"error": "not found"})),
        ("GET", "/hello/", (404, {"error": "not found"})),
        ("GET", "/hello", (404, {"error": "not found"})),
        ("GET", "/hello/a/b", (404, {"error": "not found"})),
        ("POST", "/", (405, {"error": "method not allowed"})),
        ("DELETE", "/hello/Ada", (405, {"error": "method not allowed"})),
        ("PUT", "/add?a=1&b=2", (405, {"error": "method not allowed"})),
        ("POST", "/nothing", (404, {"error": "not found"})),
    ],
)
def test_route(method, target, expected):
    assert tuple(m.route(method, target)) == expected


def test_response_layout():
    raw = m.to_http_response(200, {"status": "ok"})
    assert isinstance(raw, bytes)
    head, _, body = raw.partition(b"\r\n\r\n")
    lines = head.split(b"\r\n")
    assert lines[0] == b"HTTP/1.1 200 OK"
    assert b"Content-Type: application/json" in lines
    assert b"Content-Length: %d" % len(body) in lines
    assert json.loads(body) == {"status": "ok"}


def test_response_status_phrase():
    raw = m.to_http_response(404, {"error": "not found"})
    assert raw.startswith(b"HTTP/1.1 404 Not Found\r\n")


def test_content_length_matches_body():
    raw = m.to_http_response(200, {"name": "é"})
    head, _, body = raw.partition(b"\r\n\r\n")
    assert b"Content-Length: %d" % len(body) in head.split(b"\r\n")
    assert json.loads(body.decode("utf-8")) == {"name": "\u00e9"}
