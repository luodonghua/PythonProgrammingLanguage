import pytest

from practice import load

m = load(__file__)

SCHEMA = """
CREATE TABLE events (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    kind TEXT NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
)
"""


@pytest.fixture
def db(pg):
    pg.execute(SCHEMA)
    pg.commit()
    return pg


@pytest.fixture
def filled(db):
    ids = [
        m.add_event(db, "login", {"user": "ann", "ok": True, "ms": 10}),
        m.add_event(db, "login", {"user": "bo", "ok": False, "ms": 30}),
        m.add_event(db, "login", {"user": "ann", "ok": False}),
        m.add_event(db, "click", {"user": "ann", "target": "buy", "tags": ["a", "b"]}),
    ]
    return db, ids


def test_add_event_returns_increasing_ids(db):
    first = m.add_event(db, "x", {"a": 1})
    second = m.add_event(db, "x", {"a": 2})
    assert second > first


def test_payload_round_trip(db):
    payload = {"name": "Ann", "n": 3, "pi": 3.5, "ok": True, "none": None, "tags": ["a", "b"], "nested": {"k": [1, 2]}}
    event_id = m.add_event(db, "x", payload)
    assert m.get_payload(db, event_id) == payload


def test_get_payload_unknown_id(db):
    event_id = m.add_event(db, "x", {"a": 1})
    assert m.get_payload(db, event_id) == {"a": 1}
    assert m.get_payload(db, event_id + 1000) is None


def test_events_containing_one_field(filled):
    db, ids = filled
    assert m.events_containing(db, user="ann") == [ids[0], ids[2], ids[3]]


def test_events_containing_several_fields(filled):
    db, ids = filled
    assert m.events_containing(db, user="ann", ok=False) == [ids[2]]
    assert m.events_containing(db, user="ann", ok=True) == [ids[0]]


def test_events_containing_value_types_matter(filled):
    db, ids = filled
    assert m.events_containing(db, ms=30) == [ids[1]]
    assert m.events_containing(db, ms="30") == []


def test_events_containing_nothing_and_everything(filled):
    db, ids = filled
    assert m.events_containing(db, user="zed") == []
    assert m.events_containing(db) == ids


def test_events_containing_array_element(filled):
    db, ids = filled
    assert m.events_containing(db, tags=["b"]) == [ids[3]]


def test_field_text(filled):
    db, ids = filled
    assert m.field_text(db, ids[0], "user") == "ann"
    assert m.field_text(db, ids[0], "ms") == "10"
    assert m.field_text(db, ids[0], "ok") == "true"


def test_field_text_missing(filled):
    db, ids = filled
    assert m.field_text(db, ids[0], "user") == "ann"
    assert m.field_text(db, ids[2], "ms") is None
    assert m.field_text(db, 999999, "user") is None


def test_field_text_key_is_a_parameter(filled):
    db, ids = filled
    assert m.field_text(db, ids[0], "user") == "ann"
    assert m.field_text(db, ids[0], "user' OR 'x'='x") is None


def test_count_by_kind(filled):
    db, _ = filled
    result = m.count_by_kind(db)
    assert result == {"click": 1, "login": 3}
    assert list(result) == ["click", "login"]


def test_count_by_kind_empty(db):
    assert m.count_by_kind(db) == {}
    m.add_event(db, "a", {})
    assert m.count_by_kind(db) == {"a": 1}


def test_average_ms(filled):
    db, _ = filled
    assert m.average_ms(db, "login") == 20.0
    assert isinstance(m.average_ms(db, "login"), float)


def test_average_ms_none(filled):
    db, _ = filled
    assert m.average_ms(db, "login") == 20.0
    assert m.average_ms(db, "click") is None
    assert m.average_ms(db, "unknown") is None
