import json

import pytest

from practice import load

m = load(__file__)


def test_repr_mixin():
    assert repr(m.Person("Ann", 30)) == "Person(name='Ann', age=30)"


def test_repr_mixin_on_another_class():
    class Dot(m.ReprMixin):
        def __init__(self):
            self.x = 1.5

    class Empty(m.ReprMixin):
        pass

    assert repr(Dot()) == "Dot(x=1.5)"
    assert repr(Empty()) == "Empty()"


def test_json_mixin():
    text = m.Person("Ann", 30).to_json()
    assert text == '{"age": 30, "name": "Ann"}'
    assert json.loads(text) == {"name": "Ann", "age": 30}


def test_person_uses_both_mixins():
    assert issubclass(m.Person, m.ReprMixin)
    assert issubclass(m.Person, m.JsonMixin)
    assert m.Person("Bo", 1).name == "Bo"


def test_heading_render():
    assert m.Heading("Title").render() == "# Title"
    assert m.Heading("Sub", 3).render() == "### Sub"


@pytest.mark.parametrize("level", [0, 7])
def test_heading_level_range(level):
    assert m.Heading("ok", 6).render() == "###### ok"
    with pytest.raises(ValueError):
        m.Heading("x", level)


def test_paragraph_render():
    assert m.Paragraph("  hello ").render() == "hello"


def test_renderable_protocol_matches_by_shape():
    assert isinstance(m.Heading("a"), m.Renderable)
    assert isinstance(m.Paragraph("a"), m.Renderable)
    assert not isinstance(object(), m.Renderable)
    assert m.Heading.__mro__ == (m.Heading, object)
    assert m.Paragraph.__mro__ == (m.Paragraph, object)


def test_render_all_default_separator():
    items = [m.Heading("Title"), m.Paragraph(" text ")]
    assert m.render_all(items) == "# Title\n\ntext"


def test_render_all_custom_separator_and_empty():
    assert m.render_all([m.Paragraph("a"), m.Paragraph("b")], sep=" | ") == "a | b"
    assert m.render_all([]) == ""


def test_render_all_accepts_any_object_with_render():
    class Shout:
        def render(self):
            return "HEY"

    assert m.render_all([Shout(), m.Paragraph("x")], sep="-") == "HEY-x"
