from unittest import TestCase

from domino_puzzle import Domino
from queued_board import QueuedBoard
from test_domino_puzzle import DummyRandom


class QueuedBoardTest(TestCase):
    def test_create(self):
        state = """\
0 1|2
-
1 0|0
===
4 5
- -
5 6
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
1 0|0
"""
        expected_queue = []

        board = QueuedBoard.create(state)

        self.assertEqual(expected_queue, board.queue)

    def test_equal(self):
        board1 = QueuedBoard.create("""\
0 1|2
-
1 0|0
===
4 5
- -
5 6
""")
        # no change
        board2 = QueuedBoard.create("""\
0 1|2
-
1 0|0
===
4 5
- -
5 6
""")
        # change a domino on the board
        board3 = QueuedBoard.create("""\
0 2|1
-
1 0|0
===
4 5
- -
5 6
""")
        # change a domino in the queue
        board4 = QueuedBoard.create("""\
0 1|2
-
1 0|0
===
4 6
- -
5 5
""")
        self.assertNotEqual(board1, board4)
        self.assertEqual(board1, board2)
        self.assertNotEqual(board1, board3)

    def test_extra_dominoes(self):
        state = """\
0 1|2
-
1 0|0
===
0 1
- -
2 1
"""
        expected_extras = [Domino(2, 2)]

        board = QueuedBoard.create(state, max_pips=2)

        self.assertEqual(expected_extras, board.extra_dominoes)

    def test_get_from_queue(self):
        state = """\
0 1|2
-
1 0|0
===
0 1
- -
2 1
"""
        board = QueuedBoard.create(state)
        expected_from_queue = Domino(0, 2)
        expected_queue = [Domino(1, 1)]

        from_queue = board.get_from_queue()

        self.assertEqual(expected_from_queue, from_queue)
        self.assertEqual(expected_queue, board.queue)

    def test_display(self):
        state = """\
0 1|2
-
1 0|0
===
4 5
- -
5 6
"""
        board = QueuedBoard.create(state)

        display = board.display()

        self.assertEqual(state, display)

    def test_display_empty_queue(self):
        state = """\
0 1|2
-
1 0|0
"""
        board = QueuedBoard.create(state)

        display = board.display()

        self.assertEqual(state, display)

    def test_fill(self):
        dummy_random = DummyRandom(samples=[[Domino(0, 1),
                                             Domino(1, 2),
                                             Domino(2, 3),
                                             Domino(3, 4),
                                             Domino(4, 5),
                                             Domino(6, 6)]],
                                   randints={(0, 1): [0, 1, 0, 0, 0, 0]})
        board = QueuedBoard(4, 3, max_pips=6)
        expected_state = """\
===
0 2 2 3 4 6
- - - - - -
1 1 3 4 5 6
"""

        board.fill(dummy_random)

        state = board.display(cropped=True)
        self.assertEqual(expected_state, state)

    def test_mutate(self):
        dummy_random = DummyRandom(samples=[[Domino(5, 5)]],
                                   randints={(1, 21): [1],  # mutation count
                                             (0, 5): [2, 4]})  # to remove or add
        board = QueuedBoard.create("""\
===
0 2 2 3 4 6
- - - - - -
1 1 3 4 5 6
""", max_pips=6)
        expected_state = """\
===
0 2 3 4 5 6
- - - - - -
1 1 4 5 5 6
"""

        new_board = board.mutate(dummy_random, QueuedBoard)

        state = new_board.display(cropped=True)
        self.assertEqual(expected_state, state)

    def test_mutate_last(self):
        dummy_random = DummyRandom(samples=[[Domino(5, 1)]],
                                   randints={(1, 21): [1],  # mutation count
                                             (0, 5): [2, 5],  # to remove or add
                                             (0, 1): [1]})  # to flip?
        start_state = """\
===
0 2 2 3 4 6
- - - - - -
1 1 3 4 5 6
"""
        board = QueuedBoard.create(start_state, max_pips=6)
        expected_state = """\
===
0 2 3 4 6 1
- - - - - -
1 1 4 5 6 5
"""

        new_board = board.mutate(dummy_random, QueuedBoard)

        state = board.display(cropped=True)
        self.assertEqual(start_state, state)

        new_state = new_board.display(cropped=True)
        self.assertEqual(expected_state, new_state)
