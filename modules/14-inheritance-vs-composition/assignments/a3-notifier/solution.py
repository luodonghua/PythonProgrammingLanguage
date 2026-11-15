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

    def __init__(self) -> None:
        self.outbox: list[tuple[str, str]] = []

    def send(self, recipient: str, text: str) -> None:
        if "@" not in recipient:
            raise DeliveryError(f"not an e-mail address: {recipient}")
        self.outbox.append((recipient, text))


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

    def __init__(self, max_length: int = 20) -> None:
        self.max_length = max_length
        self.outbox: list[tuple[str, str]] = []

    def send(self, recipient: str, text: str) -> None:
        if len(text) > self.max_length:
            raise DeliveryError("message too long")
        self.outbox.append((recipient, text))


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

    def __init__(self, senders=()) -> None:
        self.senders = list(senders)

    def add_sender(self, sender) -> None:
        self.senders.append(sender)

    def notify(self, recipient: str, text: str) -> dict[str, bool]:
        results = {}
        for sender in self.senders:
            try:
                sender.send(recipient, text)
            except DeliveryError:
                results[sender.name] = False
            else:
                results[sender.name] = True
        return results


if __name__ == "__main__":
    notifier = Notifier([EmailSender(), SmsSender()])
    print(notifier.notify("ann@example.com", "Your order has shipped and is on its way"))
