from unittest import TestCase

from adding_puzzle import AddingBoardGraph
from queued_board import QueuedBoard


class AddingBoardGraphTest(TestCase):
    def test_first_move(self):
        board = QueuedBoard.create("""\
0|1

0|0
""",
                                   border=1)
        graph = AddingBoardGraph()
        expected = iter("""\
01l
###
0|1 x

x 0|0

###
01r
###
x 0|1

0|0 x

###
01h
###
0|0
===
0|1
""".split('\n###\n'))
        expected_moves = set(zip(expected, expected))

        moves = set(graph.generate_moves(board))

        self.assertEqual(expected_moves, moves)

    def test_second_move(self):
        board = QueuedBoard.create("""\
x 0|1

0|0 x
""",
                                   border=1)
        graph = AddingBoardGraph()
        expected = iter("""\
01l
###
0|1

0|0
""".split('\n###\n'))
        expected_moves = set(zip(expected, expected))

        moves = set(graph.generate_moves(board))

        self.assertEqual(expected_moves, moves)

    def test_walk(self):
        board = QueuedBoard.create("""\
1|6

0|0
""")
        graph = AddingBoardGraph()
        expected_states = set("""\
1|6

0|0
###
x 1|6

0|0 x
###
1|6 x

x 0|0
###
0|0
===
1|6
""".split('###\n'))

        states = graph.walk(board)
        self.assertEqual(expected_states, states)
