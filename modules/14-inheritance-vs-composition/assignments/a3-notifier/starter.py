"""Assignment 3: A notifier with pluggable senders."""


class DeliveryError(Exception):
    """Raised by a sender when it cannot deliver a message."""


class EmailSender:
    """Pretend e-mail sender. Records messages instead of sending them.

    EmailSender()
    .name            "email"
    .outbox          list of (recipient, text) tuples, oldest first.
    .send(recipient, text)
                     Raise DeliveryError if "@" is not in recipient.
                     Otherwise append (recipient, text) to outbox.
    """

    name = "email"

    def __init__(self):
        # TODO: create the empty outbox list.
        ...

    def send(self, recipient, text):
        # TODO
        ...


class SmsSender:
    """Pretend SMS sender.

    SmsSender(max_length=20)
    .name            "sms"
    .outbox          list of (recipient, text) tuples.
    .send(recipient, text)
                     Raise DeliveryError if text is longer than max_length.
                     Otherwise append (recipient, text) to outbox.
    """

    name = "sms"

    def __init__(self, max_length=20):
        # TODO: keep max_length and create the outbox.
        ...

    def send(self, recipient, text):
        # TODO
        ...


class Notifier:
    """Sends one message through every sender it was given (composition).

    Notifier(senders)   senders is any iterable of objects with .name and
                        .send(recipient, text). Store them in a list.
    .add_sender(sender) add one more sender.
    .notify(recipient, text)
                        Try each sender in order. A sender that raises DeliveryError
                        is skipped (the others still run). Return a dict that maps
                        each sender name to True (delivered) or False (failed).
                        Other exceptions are not caught.
    """

    def __init__(self, senders=()):
        # TODO: keep the senders in a list.
        ...

    def add_sender(self, sender):
        # TODO
        ...

    def notify(self, recipient, text):
        # TODO
        ...


if __name__ == "__main__":
    notifier = Notifier([EmailSender(), SmsSender()])
    print(notifier.notify("ann@example.com", "Your order has shipped and is on its way"))
