import http.client
import json
import threading

import pytest

from practice import load

m = load(__file__)


@pytest.fixture
def server():
    srv = m.make_server()
    thread = threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True)
    thread.start()
    try:
        yield srv
    finally:
        srv.shutdown()
        srv.server_close()
        thread.join()


def request(server, method, path, body=None):
    conn = http.client.HTTPConnection("127.0.0.1", server.server_address[1], timeout=5)
    try:
        conn.request(method, path, body=body)
        response = conn.getresponse()
        return response.status, response.getheader("Content-Type"), response.read()
    finally:
        conn.close()


def test_health(server):
    status, content_type, body = request(server, "GET", "/health")
    assert status == 200
    assert content_type == "application/json"
    assert json.loads(body) == {"status": "ok"}


def test_echo_returns_json_and_length(server):
    payload = b'{"a": [1, 2], "b": "x"}'
    status, content_type, body = request(server, "POST", "/echo", payload)
    assert status == 200
    assert content_type == "application/json"
    assert json.loads(body) == {"received": {"a": [1, 2], "b": "x"}, "length": len(payload)}


def test_echo_accepts_any_json_value(server):
    status, _, body = request(server, "POST", "/echo", b"[1, 2, 3]")
    assert status == 200
    assert json.loads(body)["received"] == [1, 2, 3]


def test_length_counts_bytes_not_characters(server):
    payload = json.dumps({"name": "é"}, ensure_ascii=False).encode("utf-8")
    status, _, body = request(server, "POST", "/echo", payload)
    assert status == 200
    assert json.loads(body)["length"] == len(payload)
    assert len(payload) > len(payload.decode("utf-8"))


@pytest.mark.parametrize("bad", [b"not json", b"{", b""])
def test_invalid_json_is_400(server, bad):
    status, content_type, body = request(server, "POST", "/echo", bad)
    assert status == 400
    assert content_type == "application/json"
    assert json.loads(body) == {"error": "invalid JSON"}


@pytest.mark.parametrize(("method", "path"), [("GET", "/nope"), ("POST", "/nope")])
def test_unknown_path_is_404(server, method, path):
    status, _, body = request(server, method, path, b"{}" if method == "POST" else None)
    assert status == 404
    assert json.loads(body) == {"error": "not found"}


@pytest.mark.parametrize(("method", "path"), [("GET", "/echo"), ("POST", "/health")])
def test_wrong_method_is_405(server, method, path):
    status, _, body = request(server, method, path, b"{}" if method == "POST" else None)
    assert status == 405
    assert json.loads(body) == {"error": "method not allowed"}
