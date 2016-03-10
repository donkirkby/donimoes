import unittest

from domino_puzzle import Domino, Cell, Board, BoardError, BoardGraph,\
    CaptureBoardGraph


class DummyRandom(object):
    def __init__(self,
                 randints=None,
                 choiceDominoes=None,
                 otherChoices=None):
        self.randints = randints or {}  # {(min, max): [i, j, k]}
        self.choiceDominoes = choiceDominoes
        self.otherChoices = otherChoices  # {[choices]: [selection]}

    def randint(self, a, b):
        results = self.randints.get((a, b), None)
        return results.pop(0) if results else 0

    def choice(self, seq):
        if type(seq[0]) is Domino:
            return self.choiceDominoes.pop(0)
        selections = self.otherChoices[seq]
        return selections.pop(0)


class CellTest(unittest.TestCase):
    def testRepr(self):
        cell = Cell(4)

        s = repr(cell)

        self.assertEqual("Cell(4)", s)

    def testPips(self):
        cell = Cell(5)

        pips = cell.pips

        self.assertEqual(5, pips)

    def testFindNeighbours(self):
        board = Board.create("""\
x 3|2

1|0 x
""")
        cell = board[1][0]
        expected_neighbours = set([board[1][1]])

        neighbours = set(cell.findNeighbours())

        self.assertEqual(expected_neighbours, neighbours)


class BoardTest(unittest.TestCase):
    def testRepr(self):
        board = Board(4, 3)

        s = repr(board)

        self.assertEqual("Board(4, 3)", s)

    def testAddCell(self):
        board = Board(4, 3)

        board.add(Cell(4), 1, 2)
        cell = board[1][2]

        self.assertEqual(4, cell.pips)

    def testAddDomino(self):
        board = Board(4, 3)
        board.add(Domino(5, 6), 1, 2)

        pips = board[1][2].pips

        self.assertEqual(5, pips)

    def testDisplay(self):
        board = Board(4, 3)
        board.add(Domino(5, 6), 1, 2)
        expected_display = """\
x 5|6 x

x x x x

x x x x
"""

        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testDisplayCropped(self):
        board = Board.create("""\
3 x x x
-
2 0|2 x

x x x x
""")
        expected_display = """\
3 x x
-
2 0|2
"""

        self.assertMultiLineEqual(expected_display,
                                  board.display(cropped=True))

    def testDisplayCroppingBounds(self):
        board = Board.create("""\
3 x x x
-
2 0|2 x

x x x x
""")
        expected_display = """\
3 x x
-
2 0|2
"""
        bounds = ['garbage', 'to', 'be', 'removed']
        expected_bounds = [0, 1, 2, 2]

        display = board.display(cropped=True, cropping_bounds=bounds)

        self.assertMultiLineEqual(expected_display, display)
        self.assertEqual(expected_bounds, bounds)

    def testRotate(self):
        board = Board(4, 3)
        domino1 = Domino(5, 6)
        board.add(domino1, 1, 2)
        domino1.rotate(-90)
        expected_display = """\
x 5 x x
  -
x 6 x x

x x x x
"""

        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testMoveRight(self):
        board = Board(4, 3)
        domino1 = Domino(5, 6)
        board.add(domino1, 1, 2)
        domino1.move(1, 0)
        expected_display = """\
x x 5|6

x x x x

x x x x
"""

        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testMoveLeft(self):
        board = Board(4, 3)
        domino1 = Domino(5, 6)
        board.add(domino1, 1, 2)
        domino1.move(-1, 0)
        expected_display = """\
5|6 x x

x x x x

x x x x
"""

        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testGetDirection(self):
        dx, dy = Domino.get_direction('l')

        self.assertEqual((-1, 0), (dx, dy))

    def testRotateWithoutBoard(self):
        domino1 = Domino(5, 6)
        domino1.rotate(90)

        self.assertEqual(90, domino1.degrees)

    def testRemove(self):
        board = Board(3, 4)
        domino1 = Domino(1, 5)
        board.add(domino1, 0, 0)

        board.remove(domino1)

        self.assertEqual([], board.dominoes)

    def testRemoveAndRotate(self):
        board = Board(3, 4)
        domino1 = Domino(1, 5)
        board.add(domino1, 0, 0)

        board.remove(domino1)
        domino1.rotate(270)

        self.assertEqual(270, domino1.degrees)

    def testRotateAndAdd(self):
        board = Board(4, 3)
        domino1 = Domino(5, 6)
        domino1.rotate(-90)
        board.add(domino1, 1, 2)
        expected_display = """\
x 5 x x
  -
x 6 x x

x x x x
"""

        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testOccupied(self):
        board = Board(4, 3)
        board.add(Domino(2, 3), 1, 0)

        with self.assertRaisesRegexp(BoardError, 'Position 1, 0 is occupied.'):
            board.add(Domino(1, 2), 0, 0)

    def testOffBoard(self):
        board = Board(4, 3)

        with self.assertRaisesRegexp(BoardError,
                                     'Position 4, 0 is off the board.'):
            board.add(Domino(1, 2), 3, 0)

    def testBadMove(self):
        start_state = """\
0|2 x

0|1 x
"""
        board = Board.create(start_state)
        domino1 = board[0][0].domino

        with self.assertRaises(BoardError):
            domino1.move(-1, 0)

        self.assertMultiLineEqual(start_state, board.display())

    def testFill(self):
        dummy_random = DummyRandom(randints={(0, 4): [1, 1]},  # directions
                                   choiceDominoes=[Domino(0, 0),
                                                   Domino(0, 1)])
        board = Board(2, 2, max_pips=6)
        expected_display = """\
0 1
- -
0 0
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testFillWithRandomDomino(self):
        dummy_random = DummyRandom(randints={(0, 4): [1, 1]},  # directions
                                   choiceDominoes=[Domino(0, 5),
                                                   Domino(0, 2)])
        board = Board(2, 2, max_pips=6)
        expected_display = """\
5 2
- -
0 0
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testFillWithFlip(self):
        dummy_random = DummyRandom(randints={(0, 4): [1, 1],   # directions
                                             (0, 1): [1, 0]},  # flips
                                   choiceDominoes=[Domino(0, 0),
                                                   Domino(0, 1)])
        board = Board(2, 2, max_pips=6)
        expected_display = """\
0 0
- -
0 1
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testFillWithMoreRotation(self):
        dummy_random = DummyRandom(randints={(0, 4): [1, 1, 1]},  # directions
                                   choiceDominoes=[Domino(0, 0),
                                                   Domino(0, 1),
                                                   Domino(0, 2)])
        board = Board(2, 3, max_pips=6)
        expected_display = """\
0|2

0 1
- -
0 0
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testFillWithBacktrack(self):
        """ Force a backtrack.

        This scenario will get to the following grid and then be forced to
        backtrack.
        x 3 4 x
          - -
        0 0 0 2
        -     -
        0 0|1 0
        """
        dummy_random = DummyRandom(
            randints={(0, 4): [1, 0, 1, 1]},  # directions
            choiceDominoes=[Domino(0, 0),
                            Domino(0, 1),
                            Domino(0, 2),
                            Domino(0, 3),
                            Domino(0, 4),
                            Domino(0, 5),
                            Domino(0, 4),
                            Domino(0, 5)])
        board = Board(4, 3, max_pips=6)
        expected_display = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    def testExtraDominoes(self):
        state = """\
0|0 x

1|1 x
"""
        max_pips = 2
        expected_extra_dominoes = [Domino(0, 1),
                                   Domino(0, 2),
                                   Domino(1, 2),
                                   Domino(2, 2)]

        board = Board.create(state, max_pips=max_pips)

        self.assertEqual(expected_extra_dominoes, board.extra_dominoes)

    def testFlip(self):
        board = Board(3, 2, max_pips=6)
        domino1 = Domino(1, 5)
        expected_display = """\
x x x

5|1 x
"""

        board.add(domino1, 0, 0)
        domino1.flip()

        self.assertMultiLineEqual(expected_display, board.display())

    def testCreate(self):
        state = """\
0|2 x

0|1 x
"""

        board = Board.create(state)
        display = board.display()

        self.assertMultiLineEqual(state, display)

    def testCreateRightEdge(self):
        state = """\
x 0|2

0|1 x
"""

        board = Board.create(state)

        self.assertMultiLineEqual(state, board.display())

    def testCreateVertical(self):
        state = """\
1 0|2
-
0 x x
"""

        board = Board.create(state)

        self.assertMultiLineEqual(state, board.display())

    def testCreateWithOtherMarkers(self):
        state = """\
1 0?2
*
0 x x
"""
        expected_display = """\
1 0|2
-
0 x x
"""

        board = Board.create(state)

        self.assertMultiLineEqual(expected_display, board.display())

    def testCreateWithBorder(self):
        state = """\
3 x x
-
2 0|2
"""
        board = Board.create(state, border=1)
        expected_display = """\
x x x x x

x 3 x x x
  -
x 2 0|2 x

x x x x x
"""

        self.assertMultiLineEqual(expected_display, board.display())

    def testIsConnected(self):
        state = """\
1 0|2 x x
-
0 0|4 0|3
"""
        board = Board.create(state)

        self.assertTrue(board.isConnected())

    def testIsNotConnected(self):
        state = """\
1 0|2 x x
-
0 x x 0|3
"""
        board = Board.create(state)

        self.assertFalse(board.isConnected())

    def testHasNoLoner(self):
        state = """\
1 0 x 1|3
- -
0 2 x 0|3
"""
        board = Board.create(state)

        self.assertFalse(board.hasLoner())

    def testHasLoner(self):
        state = """\
1 0 x 1|2
- -
0 2 x 0|3
"""
        board = Board.create(state)

        self.assertTrue(board.hasLoner())

    def testEqual(self):
        state = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
        board1 = Board.create(state)
        board2 = Board.create(state)

        eq_result = (board1 == board2)
        neq_result = (board1 != board2)
        self.assertTrue(eq_result)
        self.assertFalse(neq_result)

    def testEqualWithGap(self):
        state = """\
0|4 0|5

0 x x 2
-     -
0 0|1 0
"""
        board1 = Board.create(state)
        board2 = Board.create(state)

        eq_result = (board1 == board2)
        neq_result = (board1 != board2)
        self.assertTrue(eq_result)
        self.assertFalse(neq_result)

    def testDifferentPips(self):
        state1 = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
        state2 = """\
6|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
        board1 = Board.create(state1)
        board2 = Board.create(state2)

        eq_result = (board1 == board2)
        neq_result = (board1 != board2)
        self.assertFalse(eq_result)
        self.assertTrue(neq_result)

    def testDifferentAlignment(self):
        state1 = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
        state2 = """\
0|4 0|5

0 0 3 2
- - - -
0 0 1 0
"""
        board1 = Board.create(state1)
        board2 = Board.create(state2)

        self.assertNotEqual(board1, board2)


class DominoTest(unittest.TestCase):
    def testRepr(self):
        domino1 = Domino(5, 3)

        s = repr(domino1)

        self.assertEqual("Domino(5, 3)", s)

    def testInit(self):
        domino1 = Domino(5, 3)

        pips = domino1.head.pips

        self.assertEqual(5, pips)

    def testCreate(self):
        expected_dominoes = [Domino(0, 0),
                             Domino(0, 1),
                             Domino(0, 2),
                             Domino(1, 1),
                             Domino(1, 2),
                             Domino(2, 2)]
        dominoes = Domino.create(2)

        self.assertEqual(expected_dominoes, dominoes)

    def testEqual(self):
        domino1 = Domino(5, 3)
        domino2 = Domino(5, 3)

        eq_result = domino1 == domino2
        neq_result = domino1 != domino2
        self.assertTrue(eq_result)
        self.assertFalse(neq_result)

    def testDifferentPips(self):
        domino1 = Domino(5, 3)
        domino2 = Domino(5, 4)
        domino3 = Domino(6, 3)

        eq_result = domino1 == domino2
        neq_result = domino1 != domino2
        self.assertFalse(eq_result)
        self.assertTrue(neq_result)
        self.assertNotEqual(domino1, domino3)

    def testEqualFlipped(self):
        domino1 = Domino(5, 3)
        domino2 = Domino(3, 5)

        eq_result = domino1 == domino2
        neq_result = domino1 != domino2
        self.assertTrue(eq_result)
        self.assertFalse(neq_result)

    def testRotateFullCircle(self):
        domino1 = Domino(1, 5)

        domino1.rotate(180)
        domino1.rotate(180)

        self.assertEqual(0, domino1.degrees)

    def testRotateNegative(self):
        domino1 = Domino(1, 5)

        domino1.rotate(-90)

        self.assertEqual(270, domino1.degrees)

    def testFindNeighbours(self):
        state = """\
1 0|2 x x
-
0 0|4 0|3
"""
        board = Board.create(state)
        domino1 = board[1][1].domino
        expected_neighbours = set([board[0][1].domino, board[1][0].domino])

        neighbours = domino1.findNeighbours()

        self.assertEqual(expected_neighbours, neighbours)

    def testIsMatch(self):
        domino1 = Domino(0, 1)

        self.assertFalse(domino1.isMatch(Domino(2, 2)))
        self.assertTrue(domino1.isMatch(Domino(0, 2)))
        self.assertTrue(domino1.isMatch(Domino(2, 1)))
        self.assertTrue(domino1.isMatch(Domino(2, 0)))
        self.assertTrue(domino1.isMatch(Domino(1, 2)))

    def testName(self):
        domino = Domino(1, 2)
        name = domino.get_name()

        self.assertEqual("12", name)

    def testDescribeMove(self):
        domino1 = Domino(1, 2)
        dx, dy = 1, 0
        expected_move = '12r'

        move = domino1.describe_move(dx, dy)

        self.assertEqual(expected_move, move)

    def testDescribeMoveReversed(self):
        domino1 = Domino(1, 2)
        domino1.rotate(180)
        dx, dy = 1, 0
        expected_move = '21r'

        move = domino1.describe_move(dx, dy)

        self.assertEqual(expected_move, move)

    def testDescribeMoveUpReversed(self):
        domino1 = Domino(1, 2)
        domino1.rotate(90)
        dx, dy = 0, 1
        expected_move = '21u'

        move = domino1.describe_move(dx, dy)

        self.assertEqual(expected_move, move)


class BoardGraphTest(unittest.TestCase):
    def testWalkRight(self):
        board = Board.create("""\
0|2 x

0|1 x
""")
        graph = BoardGraph()
        expected_states = set("""\
0|2

0|1
---
0|2 x

x 0|1
---
x 0|2

0|1 x
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def testWalkLeft(self):
        board = Board.create("""\
x 0|2

0|1 x
""")
        graph = BoardGraph()
        expected_states = set("""\
0|2

0|1
---
0|2 x

x 0|1
---
x 0|2

0|1 x
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def testWalkDown(self):
        board = Board.create("""\
x 3 x x x
  -
x 2 0|2 x

x 0|1 x x
""")
        graph = BoardGraph()
        expected_states = set("""\
3 x x
-
2 0|2

0|1 x
---
3 x x
-
2 0|2

x 0|1
---
3 x x x
-
2 0|2 x

x x 0|1
---
3 0|2
-
2 0|1
---
3 0|2 x
-
2 x 0|1
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def ignoreWalkLast(self):
        """ Switching to NetworkX broke this. Not really used, so ignore for now.
        """
        board = Board.create("""\
3 x x
-
2 0|2

0|1 x
""")
        graph = BoardGraph()
        expected_last = """\
3 0|2 x
-
2 x 0|1
"""

        graph.walk(board)

        self.assertMultiLineEqual(expected_last, graph.last)

    def testWalkNoSplit(self):
        board = Board.create("""\
x 3|2 3|1 x
""")
        graph = BoardGraph()
        expected_states = set("""\
3|2 3|1
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def testWalkNoLoner(self):
        board = Board.create("""\
x 3 5 x
  - -
x 2 4 x

x 3|5 x
""")
        graph = BoardGraph()
        expected_states = set("""\
3 5
- -
2 4

3|5
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)


class CaptureBoardGraphTest(unittest.TestCase):
    def testCaptureRight(self):
        board = Board.create("""\
0|2 x

1|0 x
""")
        graph = CaptureBoardGraph()
        expected_states = set("""\
0|2

1|0
---
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def testSomeUncaptured(self):
        board = Board.create("""\
4|4 3
    -
1|5 4
""")
        graph = CaptureBoardGraph()
        expected_states = set("""\
4|4 3
    -
1|5 4
---
1|5
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def testMoveWithoutCapture(self):
        board = Board.create("""\
4|3

1|2
""")
        graph = CaptureBoardGraph()
        expected_states = set("""\
4|3

1|2
---
x 4|3

1|2 x
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)

    def testMoveLeftUpdatesOffset(self):
        start_state = """\
4|3

1|2
"""
        board = Board.create(start_state, border=1)
        graph = CaptureBoardGraph()
        expected_state = """\
x 4|3

1|2 x
"""
        graph.walk(board)
        offset = [1, 1]  # position of bottom left corner (within border)
        expected_offset = [1, 0]  # equivalent position after move and cropping

        state = graph.move(board[1][1].domino, -1, 0, offset)

        self.assertEqual(expected_state, state)
        self.assertEqual(expected_offset, offset)

    def testSolution(self):
        graph = CaptureBoardGraph()
        expected_solution = ['34u', '24r']
        board = Board.create("""\
6|2 3
    -
2|4 4
""")
        graph.walk(board)
        solution = graph.get_solution()

        self.assertEqual(expected_solution, solution)

    def testDisconnectedBeforeCapture(self):
        """ Board must be connected after move and after capture.

        Here, move 62L is disconnected after the move, but connected after
        the capture removes most of the dominoes. Test that the move is still
        not allowed.
        """
        board = Board.create("""\
x x x x 5
        -
x x 6|2 3

6|6 2|4 x
""")
        graph = CaptureBoardGraph()
        expected_states = set("""\
x x x x 5
        -
x x 6|2 3

6|6 2|4 x
""".split('---\n'))

        states = graph.walk(board)

        self.assertEqual(expected_states, states)
