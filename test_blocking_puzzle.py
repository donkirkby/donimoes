from unittest.case import TestCase

from blocking_puzzle import BlockingBoardGraph
from domino_puzzle import Board


class BlockingBoardGraphTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.addTypeEqualityFunc(str, self.assertMultiLineEqual)

    def test_no_blocking(self):
        board = Board.create("""\
1|2

3|4
""")
        graph = BlockingBoardGraph()
        expected_states = set("""\
1|2

3|4
---
1|2 x

x 3|4
---
x 1|2

3|4 x
""".split('---\n'))

        states = graph.walk(board)
        self.assertEqual(expected_states, states)

    def test_blocking(self):
        board = Board.create("""\
1|2

2|4
""")
        graph = BlockingBoardGraph()
        expected_states = set("""\
1|2

2|4
---
x 1|2

2|4 x
""".split('---\n'))

        states = graph.walk(board)
        self.assertEqual(expected_states, states)

    def test_start_and_last(self):
        expected_start = """\
x x 1|2

2|4 3 x
    -
x x 2 x
"""
        expected_last = """\
1|2 3
    -
2|4 2
"""
        board = Board.create(expected_last)
        graph = BlockingBoardGraph()

        graph.walk(board)
        self.assertEqual(expected_start, graph.start)
        self.assertEqual(expected_last, graph.last)

    def test_solution(self):
        board = Board.create("""\
1|2 3
    -
2|4 2
""")
        graph = BlockingBoardGraph()
        expected_solution = ['12l', '12l', '32u']

        graph.walk(board)
        solution = graph.get_solution()

        self.assertEqual(expected_solution, solution)

    def test_choice_counts(self):
        board = Board.create("""\
1|2 3
    -
2|4 2
""")
        graph = BlockingBoardGraph()
        expected_counts = [1, 2, 2]

        graph.walk(board)
        counts = graph.get_choice_counts()

        self.assertEqual(expected_counts, counts)
