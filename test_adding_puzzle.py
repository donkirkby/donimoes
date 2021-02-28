from unittest import TestCase

from adding_puzzle import AddingBoardGraph
from domino_puzzle import MoveDescription
from queued_board import QueuedBoard


class AddingBoardGraphTest(TestCase):
    def test_first_move(self):
        board = QueuedBoard.create("""\
===
1 3 1
- - -
2 4 3
""",
                                   border=1)
        graph = AddingBoardGraph()
        expected_state = """\
1|3

1 3
- -
2 4
"""
        expected_moves = {MoveDescription('13h21', expected_state)}

        moves = set(graph.generate_moves(board))

        self.assertEqual(expected_moves, moves)

    def test_move_to_complement(self):
        board = QueuedBoard.create("""\
1|5

1 5
- -
2 4
""",
                                   border=1)
        graph = AddingBoardGraph()
        expected_state1 = """\
1|5 x

x 1 5
  - -
x 2 4
"""
        expected_state2 = """\
x 1|5

1 5 x
- -
2 4 x
"""
        expected_moves = {MoveDescription('15l', expected_state1, remaining=1-2/3),
                          MoveDescription('15r', expected_state2, remaining=1-2/3)}

        moves = set(graph.generate_moves(board))

        self.assertEqual(expected_moves, moves)

    def test_walk(self):
        board = QueuedBoard.create("""\
===
1 4 4
- - -
2 3 1
""")
        graph = AddingBoardGraph()
        expected_states = set("""\
===
1 4 4
- - -
2 3 1
###
1|4

1 4
- -
2 3
###
1|4

1 x
-
2 4
  -
x 3
###
1 x
-
2 4
  -
x 3
===
4
-
1
""".split('###\n'))

        states = graph.walk(board)
        self.assertEqual(expected_states, states)

    def test_solution(self):
        board = QueuedBoard.create("""\
===
1 4 4
- - -
2 3 1
""")
        graph = AddingBoardGraph()
        expected_solution = ['14h21']

        graph.walk(board)
        solution = graph.get_solution()

        self.assertEqual(expected_solution, solution)

    def test_no_moves(self):
        start_state = """\
===
4 1 4
- - -
1 0 4
"""
        board = QueuedBoard.create(start_state)
        graph = AddingBoardGraph()
        expected_states = {start_state}
        expected_last = None

        states = graph.walk(board)

        self.assertEqual(expected_states, states)
        self.assertEqual(expected_last, graph.last)

    def test_4x3_solution(self):
        board = QueuedBoard.create("""\
===
0 5 1 1 2 0
- - - - - -
1 5 5 1 5 2
""")
        graph = AddingBoardGraph()
        expected_solution = ['15h24', '01u', '15r', '11v24', '25v43', '02h32']

        graph.walk(board)
        solution = graph.get_solution()

        self.assertEqual(expected_solution, solution)

    def test_check_progress(self):
        board = QueuedBoard.create("""\
0 5 x
- -
1 5 x

x 1|5
===
1 2 0
- - -
1 5 2
""")
        expected_min_dominoes = 3
        graph = AddingBoardGraph()

        remaining = graph.check_progress(board)

        self.assertEqual(remaining, expected_min_dominoes)

    def test_check_progress_area(self):
        """ After queue is empty, track progress toward rectangular shape.

        Any gaps will make width*height more than the number of cells.
        Progress is 1 - cell_count/(width*height). Progress is 0 for a
        solution.
        """
        board = QueuedBoard.create("""\
0 0|2 x
-
1 5 2 x
  - -
1 5 5 x
-
1 x 1|5
""")

        expected_min_dominoes = 0.25  # 1 - 12 / (4*4)
        graph = AddingBoardGraph()

        remaining = graph.check_progress(board)

        self.assertEqual(remaining, expected_min_dominoes)
        self.assertIsNone(graph.last)

    def test_check_progress_solution(self):
        """ After queue is empty, track progress toward rectangular shape.

        Any gaps will make width*height more than the number of cells.
        Progress is 1 - cell_count/(width*height). Progress is 0 for a
        solution.
        """
        state = """\
0 0|2
-
1 5 2
  - -
1 5 5
-
1 1|5
"""
        board = QueuedBoard.create(state)

        expected_min_dominoes = 0  # 1 - 12 / (3*4)
        graph = AddingBoardGraph()

        remaining = graph.check_progress(board)

        self.assertEqual(remaining, expected_min_dominoes)

    def test_check_progress_ignores_border(self):
        board = QueuedBoard.create("""\
x x x x x x

x 0 0|2 x x
  -
x 1 5 2 x x
    - -
x 1 5 5 x x
  -
x 1 x 1|5 x

x x x x x x
""")

        expected_min_dominoes = 0.25  # 1 - 12 / (4*4)
        graph = AddingBoardGraph()

        remaining = graph.check_progress(board)

        self.assertEqual(remaining, expected_min_dominoes)
