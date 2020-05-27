import pytest

from priority import PriorityQueue


def test_add():
    queue = PriorityQueue()

    queue.add('two', 2)
    queue.add('three', 3)
    queue.add('one', 1)

    item = queue.pop()

    assert item == 'one'


def test_add_default_priority():
    queue = PriorityQueue()

    queue.add('one', 1)
    queue.add('zero')

    item = queue.pop()

    assert item == 'zero'


def test_pop_empty():
    queue = PriorityQueue()

    with pytest.raises(KeyError):
        queue.pop()


def test_bool_false():
    queue = PriorityQueue()

    assert not queue


def test_bool_true():
    queue = PriorityQueue()
    queue.add('foo')

    assert queue


def test_change_priority():
    queue = PriorityQueue()

    queue.add('one', 3)
    queue.add('two', 2)
    queue.add('one', 1)

    assert queue.pop() == 'one'
    assert queue.pop() == 'two'
    assert not queue

    with pytest.raises(KeyError):
        queue.pop()
