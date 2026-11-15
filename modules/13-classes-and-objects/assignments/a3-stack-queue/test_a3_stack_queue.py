import pytest

from practice import load

m = load(__file__)


def test_stack_lifo():
    s = m.Stack()
    for n in (1, 2, 3):
        s.push(n)
    assert [s.pop(), s.pop(), s.pop()] == [3, 2, 1]


def test_stack_peek_does_not_remove():
    s = m.Stack([1, 2])
    assert s.peek() == 2
    assert len(s) == 2


def test_stack_empty_errors():
    s = m.Stack()
    with pytest.raises(IndexError, match="pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError, match="pop from empty stack"):
        s.peek()


def test_stack_len_bool_iter_repr():
    s = m.Stack([1, 2, 3])
    assert len(s) == 3
    assert bool(s) is True
    assert list(s) == [3, 2, 1]
    assert repr(s) == "Stack([1, 2, 3])"
    assert bool(m.Stack()) is False


def test_stack_initial_items_are_copied():
    source = [1, 2]
    s = m.Stack(source)
    s.push(3)
    assert s.peek() == 3
    assert source == [1, 2]


def test_queue_fifo():
    q = m.Queue()
    for n in (1, 2, 3):
        q.enqueue(n)
    assert [q.dequeue(), q.dequeue(), q.dequeue()] == [1, 2, 3]


def test_queue_empty_error():
    with pytest.raises(IndexError, match="dequeue from empty queue"):
        m.Queue().dequeue()


def test_queue_len_bool_iter_repr():
    q = m.Queue(["a", "b"])
    assert len(q) == 2
    assert bool(q) is True
    assert list(q) == ["a", "b"]
    assert repr(q) == "Queue(['a', 'b'])"
    assert bool(m.Queue()) is False


def test_mixed_use_keeps_order():
    q = m.Queue([1])
    q.enqueue(2)
    assert q.dequeue() == 1
    q.enqueue(3)
    assert list(q) == [2, 3]
