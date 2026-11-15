---
layout: module
module: 23-http-and-web
kind: learn
title: HTTP and the web
permalink: /modules/23-http-and-web/
---

<div class="box key" markdown="1">

## Key learning points

- HTTP is a text protocol. A **client** sends a **request** (method, path, headers, optional body). A **server** sends back a **response** (status code, headers, optional body).
- The method says what you want (`GET` reads, `POST` creates, `PUT` replaces, `DELETE` removes). The status code says what happened (`2xx` success, `3xx` redirect, `4xx` your mistake, `5xx` server mistake).
- A URL has parts (scheme, host, port, path, query, fragment). Use `urllib.parse` to build and split URLs. Never glue query strings together by hand.
- `urllib.request.urlopen` fetches a URL with the standard library. Always pass a `timeout`.
- `http.server` can run a tiny web server. A server on port `0` picks a free port, which makes it easy to test offline.
- A JSON API returns JSON text and a `Content-Type: application/json` header. Decode it with `json.load`.

</div>

## 1. What a request and a response look like

When you open `http://example.com/hello?name=Ada`, the client sends text like this:

```text
GET /hello?name=Ada HTTP/1.1
Host: example.com
Accept: application/json

```

The first line is the **request line**: method, target (path plus query) and protocol version. The lines after it are **headers** (`Name: value`). An empty line ends the headers. A `POST` request has a body after that line.

The server answers:

```text
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 18

{"message": "hi"}
```

The first line is the **status line**. Common status codes:

| Code | Meaning |
|---|---|
| 200 | OK |
| 201 | Created |
| 301 / 302 | Moved (redirect) |
| 400 | Bad request (the client sent something invalid) |
| 404 | Not found |
| 405 | Method not allowed |
| 500 | Server error (a bug on the server) |

HTTP is **stateless**: each request stands alone. A server does not remember the previous one unless the client sends something (a cookie or a token) that identifies it.

## 2. URLs with urllib.parse

```python
from urllib.parse import urlencode, urlsplit, parse_qs, quote, urljoin

print(urlencode({"q": "python tips", "page": 2, "tag": ["a", "b"]}, doseq=True))
```

```text
q=python+tips&page=2&tag=a&tag=b
```

`urlencode` escapes spaces and special characters for you. `doseq=True` repeats the key for list values.

```python
u = urlsplit("https://example.com:8080/search/items?q=cat+food&page=2#top")
print(u.scheme, u.hostname, u.port, u.path)
print(parse_qs(u.query))
```

```text
https example.com 8080 /search/items
{'q': ['cat food'], 'page': ['2']}
```

`parse_qs` always gives lists, because a key can repeat. Two more helpers:

```python
print(quote("a b/ü"))                                  # a%20b/%C3%BC
print(urljoin("https://example.com/a/b", "../c"))      # https://example.com/c
```

## 3. Fetching with urllib.request

```python
import json
import urllib.request

with urllib.request.urlopen("http://127.0.0.1:8000/hello", timeout=5) as response:
    print(response.status, response.headers["Content-Type"])
    data = json.load(response)
```

`urlopen` returns a response you can use in a `with` block. `json.load` reads the body and decodes it. To set headers or a method, build a `Request`:

```python
req = urllib.request.Request(
    "http://127.0.0.1:8000/hello",
    headers={"Accept": "application/json"},
    method="GET",
)
```

For a `4xx` or `5xx` status, `urlopen` raises `urllib.error.HTTPError`. The code is `error.code`. If the server cannot be reached at all you get `urllib.error.URLError`. `HTTPError` is a subclass of `URLError`, so catch it first.

## 4. A tiny web server

`http.server` is for learning and tests, not production. You write a handler class with one method per HTTP method:

```python
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/hello":
            body = json.dumps({"message": "hi"}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
print(server.server_address[1])    # the port the OS picked
# server.serve_forever()           # blocks; run it in a thread in tests
```

Order matters: `send_response`, then headers, then `end_headers()`, then the body. The handler reads the request line from `self.command` (the method) and `self.path`. For a `POST`, read the body with `self.rfile.read(length)`, where `length` comes from the `Content-Length` header.

To test a server, start it in a background thread and call `server.shutdown()` at the end:

```python
import threading

thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
# ... make requests to http://127.0.0.1:<port> ...
server.shutdown()
server.server_close()
```

Run on `127.0.0.1` so only your own machine can connect.

## 5. REST and JSON APIs in brief

REST is a style for naming things. A resource has a URL and the method says the action:

| Request | Meaning |
|---|---|
| `GET /notes` | list notes |
| `POST /notes` | create a note (body is JSON) |
| `GET /notes/3` | read note 3 |
| `DELETE /notes/3` | delete note 3 |

Good APIs return the right status (`201` after creating, `404` for a missing note, `400` for bad input) and a JSON error body the client can read.

Beyond a toy server, Python web code usually runs under **WSGI** (a standard function signature that frameworks such as Flask and Django use) or **ASGI** (the async version, used by FastAPI). For client code, the third-party **httpx** library is easier than `urllib`. You will use it in topic 35.

<div class="box warn" markdown="1">

## Common mistakes

- **Building URLs with string addition.** `"?q=" + text` breaks on spaces, `&` and non-ASCII characters. Use `urlencode`.
- **No timeout.** `urlopen(url)` without `timeout` can wait forever. Always set one.
- **Forgetting `Content-Length`.** Without it (or a closed connection), the client cannot tell where the body ends.
- **Sending a `str` to `wfile.write`.** It needs `bytes`. Call `.encode("utf-8")`.
- **Trusting the client.** A request body can be anything. Catch `json.JSONDecodeError` and answer `400`, not `500`.

</div>

## Try it yourself

1. Use `urlencode` to build the query string for `{"city": "São Paulo", "units": "metric"}`. What does the `ã` become?
2. Start the server from section 4 in a thread, fetch `/hello` with `urlopen`, and print the decoded JSON. Then fetch `/missing` and print the status code from the `HTTPError`.
3. Add a `do_POST` method to the handler that reads a JSON body and replies with the same JSON.

## Where this comes from

*Introducing Python*, chapter 22 (Data in Space: Networks) and chapter 24 (The Web). *Learn Python the Hard Way*, exercises 50 to 52 (web projects). For the standard library modules used here, see the Python docs for [`urllib`](https://docs.python.org/3/library/urllib.html) and [`http.server`](https://docs.python.org/3/library/http.server.html).

## Done with this page?

<ul class="checks">
  <li><label><input type="checkbox" data-progress="23-http-and-web:learn"> I have read this page</label></li>
</ul>

Next: [take the 10-question test]({{ '/modules/23-http-and-web/quiz/' | relative_url }}) and then the [assignments]({{ '/modules/23-http-and-web/assignments/' | relative_url }}).
