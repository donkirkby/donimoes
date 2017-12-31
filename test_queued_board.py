from unittest import TestCase

from domino_puzzle import Domino
from queued_board import QueuedBoard


class QueuedBoardTest(TestCase):
    def test_create(self):
        state = """\
0 1|2
-
1 3|4
===
4|5
5|6
"""
        expected_queue = [Domino(4, 5), Domino(5, 6)]

        board = QueuedBoard.create(state)

        self.assertEqual(1, board[0][0].pips)
        self.assertEqual(2, board[2][1].pips)
        self.assertEqual(expected_queue, board.queue)

    def test_create_without_queue(self):
        state = """\
0 1|2
-
1 3|4
"""
        expected_queue = []

        board = QueuedBoard.create(state)

        self.assertEqual(expected_queue, board.queue)

    def test_extra_dominoes(self):
        state = """\
0 1|2
-
1 2|0
===
0|0
1|1
"""
        expected_extras = [Domino(2, 2)]

        board = QueuedBoard.create(state, max_pips=2)

        self.assertEqual(expected_extras, board.extra_dominoes)

    def test_get_from_queue(self):
        state = """\
0 1|2
-
1 2|0
===
0|0
1|1
"""
        board = QueuedBoard.create(state)
        expected_from_queue = Domino(0, 0)
        expected_queue = [Domino(1, 1)]

        from_queue = board.get_from_queue()

        self.assertEqual(expected_from_queue, from_queue)
        self.assertEqual(expected_queue, board.queue)

    def test_display(self):
        state = """\
0 1|2
-
1 3|4
===
4|5
5|6
"""
        board = QueuedBoard.create(state)

        display = board.display()

        self.assertEqual(state, display)

    def test_display_empty_queue(self):
        state = """\
0 1|2
-
1 3|4
"""
        board = QueuedBoard.create(state)

        display = board.display()

        self.assertEqual(state, display)
