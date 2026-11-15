import pytest

from practice import load

m = load(__file__)


class Recorder:
    """A custom sender written by the test. Notifier must accept any such object."""

    name = "recorder"

    def __init__(self):
        self.seen = []

    def send(self, recipient, text):
        self.seen.append((recipient, text))


class Exploding:
    name = "boom"

    def send(self, recipient, text):
        raise RuntimeError("bug in sender")


def test_email_sender():
    e = m.EmailSender()
    assert e.name == "email"
    e.send("a@b.com", "hi")
    assert e.outbox == [("a@b.com", "hi")]


def test_email_rejects_bad_address():
    e = m.EmailSender()
    with pytest.raises(m.DeliveryError):
        e.send("nobody", "hi")
    assert e.outbox == []


def test_sms_sender_limit():
    s = m.SmsSender(max_length=5)
    assert s.name == "sms"
    s.send("123", "hello")
    with pytest.raises(m.DeliveryError):
        s.send("123", "too long")
    assert s.outbox == [("123", "hello")]


def test_sms_default_limit_is_20():
    s = m.SmsSender()
    s.send("1", "x" * 20)
    with pytest.raises(m.DeliveryError):
        s.send("1", "x" * 21)


def test_senders_do_not_share_outboxes():
    a, b = m.EmailSender(), m.EmailSender()
    a.send("a@b.c", "x")
    assert b.outbox == []


def test_notify_all_succeed():
    email, sms = m.EmailSender(), m.SmsSender()
    n = m.Notifier([email, sms])
    assert n.notify("a@b.com", "hi") == {"email": True, "sms": True}
    assert email.outbox == [("a@b.com", "hi")]
    assert sms.outbox == [("a@b.com", "hi")]


def test_failure_is_reported_and_others_still_run():
    email, sms = m.EmailSender(), m.SmsSender(max_length=3)
    result = m.Notifier([email, sms]).notify("a@b.com", "long message")
    assert result == {"email": True, "sms": False}
    assert len(email.outbox) == 1
    assert sms.outbox == []


def test_custom_sender_and_add_sender():
    rec = Recorder()
    n = m.Notifier()
    assert n.notify("x", "y") == {}
    n.add_sender(rec)
    assert n.notify("x", "y") == {"recorder": True}
    assert rec.seen == [("x", "y")]


def test_other_exceptions_are_not_hidden():
    n = m.Notifier([Exploding()])
    with pytest.raises(RuntimeError):
        n.notify("x", "y")


def test_accepts_any_iterable():
    n = m.Notifier(s for s in [m.EmailSender()])
    assert n.notify("a@b.com", "hi") == {"email": True}
    assert n.notify("a@b.com", "again") == {"email": True}
