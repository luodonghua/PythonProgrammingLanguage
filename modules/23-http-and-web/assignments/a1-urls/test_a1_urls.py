import pytest

from practice import load

m = load(__file__)


@pytest.mark.parametrize(
    ("base", "path"),
    [
        ("https://api.example.com", "v1/items"),
        ("https://api.example.com/", "/v1/items"),
        ("https://api.example.com/", "v1/items"),
        ("https://api.example.com", "/v1/items"),
    ],
)
def test_build_url_slashes(base, path):
    assert m.build_url(base, path) == "https://api.example.com/v1/items"


def test_build_url_params_encoded():
    url = m.build_url("https://x.org", "/s", {"q": "a b", "page": 2})
    assert url == "https://x.org/s?q=a+b&page=2"


def test_build_url_special_characters():
    assert m.build_url("https://x.org", "/s", {"q": "a&b=c"}) == "https://x.org/s?q=a%26b%3Dc"


def test_build_url_skips_none_and_repeats_lists():
    url = m.build_url("https://x.org", "/s", {"a": None, "tag": ["x", "y"]})
    assert url == "https://x.org/s?tag=x&tag=y"


@pytest.mark.parametrize("params", [None, {}, {"a": None}])
def test_build_url_no_question_mark_without_params(params):
    assert m.build_url("https://x.org", "/s", params) == "https://x.org/s"


def test_parse_request_line():
    assert m.parse_request_line("GET /search?q=cat+food&page=2 HTTP/1.1") == {
        "method": "GET",
        "path": "/search",
        "query": {"q": "cat food", "page": "2"},
        "version": "HTTP/1.1",
    }


def test_parse_request_line_without_query():
    result = m.parse_request_line("DELETE /notes/3 HTTP/1.0")
    assert result["method"] == "DELETE"
    assert result["path"] == "/notes/3"
    assert result["query"] == {}


def test_parse_request_line_first_value_wins():
    result = m.parse_request_line("GET /s?tag=a&tag=b HTTP/1.1")
    assert result["query"] == {"tag": "a"}


@pytest.mark.parametrize(
    "line",
    [
        "",
        "GET /",
        "GET / HTTP/1.1 extra",
        "get / HTTP/1.1",
        "G3T / HTTP/1.1",
        "GET / FTP/1.1",
    ],
)
def test_parse_request_line_invalid(line):
    with pytest.raises(ValueError):
        m.parse_request_line(line)
