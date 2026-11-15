---
layout: module
module: 23-http-and-web
kind: assignments
title: "HTTP and the web - assignments"
permalink: /modules/23-http-and-web/assignments/
---
Four tasks on URLs, routing, fetching JSON and serving JSON. None of them needs the internet. Tasks 3 and 4 start a small server on your own computer (127.0.0.1, port chosen by the operating system), so you may see a firewall prompt on some systems. Allow it or ignore it. The tests talk only to your own machine.

{% include practice-setup.md %}

No extra libraries are needed. Everything uses the Python standard library (`urllib`, `http.server`, `json`).

Run all tests for this topic:

```bash
uv run pytest modules/23-http-and-web
```

---

<div class="assignment" markdown="1">

## Assignment 1: Build URLs and parse a request line

**Goal:** Write `build_url` with correct slashes and percent-encoded parameters, and `parse_request_line` that splits a raw HTTP request line. Practises `urllib.parse` and input validation.

**Files:** [`starter.py`]({{ 'modules/23-http-and-web/assignments/a1-urls/starter.py' | relative_url }}), test file `test_a1_urls.py` in the same folder.

```python
{% include_relative assignments/a1-urls/starter.py %}
```

Run: `uv run pytest modules/23-http-and-web/assignments/a1-urls`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a1-urls/solution.py %}
```

`urlencode(..., doseq=True)` does all the escaping, so no quoting is written by hand. `rstrip("/")` and `lstrip("/")` give exactly one slash. `parse_qs` returns lists, so the solution keeps `values[0]`.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 2: A router and a raw HTTP response

**Goal:** Write `route(method, target)`, which returns a status and a JSON payload, and `to_http_response`, which turns them into the bytes of an HTTP/1.1 response. Practises routing, status codes and the response format.

**Files:** [`starter.py`]({{ 'modules/23-http-and-web/assignments/a2-router/starter.py' | relative_url }}), test file `test_a2_router.py` in the same folder.

```python
{% include_relative assignments/a2-router/starter.py %}
```

Run: `uv run pytest modules/23-http-and-web/assignments/a2-router`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a2-router/solution.py %}
```

The path decides whether a route exists (404 if not). Only then is the method checked (405). `Content-Length` is computed from the encoded body, because it counts bytes. `HTTPStatus(status).phrase` supplies "OK" and "Not Found".
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 3: Fetch JSON with urllib

**Goal:** Write `fetch_json`, which adds query parameters and headers, decodes the JSON body and turns every failure into one `ApiError`. Practises `urllib.request`, `HTTPError` versus `URLError`, and timeouts.

**Files:** [`starter.py`]({{ 'modules/23-http-and-web/assignments/a3-fetch-json/starter.py' | relative_url }}), test file `test_a3_fetch_json.py` in the same folder.

```python
{% include_relative assignments/a3-fetch-json/starter.py %}
```

Run: `uv run pytest modules/23-http-and-web/assignments/a3-fetch-json`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a3-fetch-json/solution.py %}
```

`HTTPError` is a subclass of `URLError`, so it must be caught first. The `with` block closes the response. `raise ... from exc` keeps the original error attached for debugging.
</details>

</div>

<div class="assignment" markdown="1">

## Assignment 4: A JSON echo server

**Goal:** Finish a `BaseHTTPRequestHandler` that serves `GET /health` and `POST /echo`, with correct status codes for bad JSON, unknown paths and wrong methods. Practises `http.server` and reading a request body.

**Files:** [`starter.py`]({{ 'modules/23-http-and-web/assignments/a4-echo-server/starter.py' | relative_url }}), test file `test_a4_echo_server.py` in the same folder.

```python
{% include_relative assignments/a4-echo-server/starter.py %}
```

Run: `uv run pytest modules/23-http-and-web/assignments/a4-echo-server`

<details markdown="1">
<summary>Show solution</summary>

```python
{% include_relative assignments/a4-echo-server/solution.py %}
```

`send_json` is the one place that writes a response, so every route sends the same headers. The body size comes from `Content-Length`, and `rfile.read(length)` reads exactly that many bytes. Bad JSON raises `ValueError`, which the handler turns into `400`.
</details>

</div>

<ul class="checks">
  <li><label><input type="checkbox" data-progress="23-http-and-web:assignments"> I have finished the assignments</label></li>
</ul>
