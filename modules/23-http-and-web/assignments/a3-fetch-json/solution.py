"""Assignment 3: Fetch JSON from an API with urllib.

The tests start a small server on 127.0.0.1 and call your function.
Nothing leaves your computer.
"""

import json
import urllib.error
import urllib.request
from urllib.parse import urlencode


class ApiError(Exception):
    """Raised when a request fails. `status` is the HTTP code, or None."""

    def __init__(self, message: str, status: int | None = None):
        super().__init__(message)
        self.status = status


def fetch_json(url: str, params: dict | None = None, headers: dict | None = None,
               timeout: float = 5.0):
    """GET `url` and return the decoded JSON body.

    - If `params` is given, add it to the URL as a query string
      (use "&" instead of "?" when the URL already contains a "?").
    - Send every entry of `headers` as a request header. Always send
      "Accept: application/json" unless `headers` already sets Accept.
    - Pass `timeout` to urlopen.
    - HTTP 4xx/5xx (urllib.error.HTTPError)  -> ApiError(<message>, status=<code>)
    - Server not reachable (urllib.error.URLError) -> ApiError(<message>, status=None)
    - A 2xx body that is not valid JSON -> ApiError("invalid JSON", status=<code>)
    """
    if params:
        url += ("&" if "?" in url else "?") + urlencode(params)
    all_headers = dict(headers or {})
    if not any(name.lower() == "accept" for name in all_headers):
        all_headers["Accept"] = "application/json"
    request = urllib.request.Request(url, headers=all_headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.status
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise ApiError(f"HTTP {exc.code}: {exc.reason}", status=exc.code) from exc
    except urllib.error.URLError as exc:
        raise ApiError(f"cannot reach server: {exc.reason}") from exc
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ApiError("invalid JSON", status=status) from exc


def fetch_item_names(base_url: str) -> list[str]:
    """Call fetch_json(base_url + "/items") and return the "name" of each item.

    The API answers a list such as [{"id": 1, "name": "pen"}, ...].
    """
    return [item["name"] for item in fetch_json(base_url + "/items")]


if __name__ == "__main__":
    try:
        fetch_json("http://127.0.0.1:9/", timeout=1)
    except ApiError as exc:
        print("failed:", exc, exc.status)
