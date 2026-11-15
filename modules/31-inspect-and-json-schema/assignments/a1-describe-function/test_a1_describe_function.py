from practice import load

m = load(__file__)


def sample(a, b=2, /, c=3, *args, d, e=None, **kwargs):
    pass


def test_describe_params_names_and_kinds():
    result = m.describe_params(sample)
    assert [p["name"] for p in result] == ["a", "b", "c", "args", "d", "e", "kwargs"]
    assert [p["kind"] for p in result] == [
        "positional_only",
        "positional_only",
        "positional_or_keyword",
        "var_positional",
        "keyword_only",
        "keyword_only",
        "var_keyword",
    ]


def test_describe_params_required_and_defaults():
    result = {p["name"]: p for p in m.describe_params(sample)}
    assert result["a"]["required"] is True
    assert result["b"]["required"] is False
    assert result["b"]["default"] == 2
    assert result["d"]["required"] is True
    assert result["d"]["default"] is None
    assert result["args"]["required"] is False
    assert result["kwargs"]["required"] is False
    assert set(result["a"]) == {"name", "kind", "required", "default"}


def test_describe_params_no_parameters():
    assert m.describe_params(lambda: 1) == []


def test_summary_line_single_and_multi_paragraph():
    def one():
        """Do one thing."""

    def many():
        """
        Do many things.

        Longer explanation follows here.
        """

    assert m.summary_line(one) == "Do one thing."
    assert m.summary_line(many) == "Do many things."


def test_summary_line_without_docstring():
    def bare():
        pass

    assert m.summary_line(bare) == ""


class Greeter:
    greeting = "hello"

    def hello(self, name: str, excited: bool = False) -> str:
        return self.greeting + name

    def _secret(self):
        pass

    def alpha(self):
        pass

    @staticmethod
    def util(x: int) -> int:
        return x

    @classmethod
    def build(cls, size: int = 1):
        return cls()


def test_public_methods():
    assert m.public_methods(Greeter()) == {
        "alpha": "()",
        "build": "(size: int = 1)",
        "hello": "(name: str, excited: bool = False) -> str",
        "util": "(x: int) -> int",
    }


def test_public_methods_sorted_and_skips_data():
    result = m.public_methods(Greeter())
    assert list(result) == sorted(result)
    assert "greeting" not in result
    assert "_secret" not in result
