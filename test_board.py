import unittest
from random import Random
from unittest.mock import patch

from domino_puzzle import Board, Cell, Domino, BoardError
from test_domino_puzzle import DummyRandom


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

    def testCreateWithSpaces(self):
        board = Board.create("""\
            4
            -
3|1   4|6 4 1
          -
  2 4     4 2|5
  - -
  3 2   4|0 5
            -
  5 0|0 1|1 4
  -
  6 5|5 3|3 6|3
""")
        expected_display = """\
x x x x x x 4 x
            -
3|1 x 4|6 4 1 x
          -
x 2 4 x x 4 2|5
  - -
x 3 2 x 4|0 5 x
            -
x 5 0|0 1|1 4 x
  -
x 6 5|5 3|3 6|3
"""

        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

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

        with self.assertRaisesRegex(BoardError, 'Position 1, 0 is occupied.'):
            board.add(Domino(1, 2), 0, 0)

    def testOffBoard(self):
        board = Board(4, 3)

        with self.assertRaisesRegex(BoardError,
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

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFill(self, mock_choose):
        mock_choose.side_effect = [[Domino(0, 0)],
                                   [Domino(0, 1)]]
        dummy_random = DummyRandom(randints={(0, 3): [1, 1]})  # directions
        board = Board(2, 2, max_pips=6)
        expected_display = """\
0 1
- -
0 0
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFillWithRandomDomino(self, mock_choose):
        mock_choose.side_effect = [[Domino(0, 5)],
                                   [Domino(0, 2)]]
        dummy_random = DummyRandom(randints={(0, 3): [1, 1]})  # directions
        board = Board(2, 2, max_pips=6)
        expected_display = """\
5 2
- -
0 0
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFillWithNoMatchesFlip(self, mock_choose):
        mock_choose.side_effect = [[Domino(0, 5)],
                                   [Domino(0, 2)]]
        dummy_random = DummyRandom(randints={(0, 3): [1, 1],  # directions
                                             (0, 1): [0, 0]})
        board = Board(2, 2, max_pips=6)
        expected_display = """\
5 0
- -
0 2
"""

        board.fill(dummy_random, matches_allowed=False)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFillWithNoMatchesNext(self, mock_choose):
        mock_choose.side_effect = [[Domino(0, 5)],
                                   [Domino(0, 0), Domino(0, 1)]]
        dummy_random = DummyRandom(randints={(0, 3): [1, 1]})  # directions
        board = Board(2, 2, max_pips=6)
        expected_display = """\
5 0
- -
0 1
"""

        board.fill(dummy_random, matches_allowed=False)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFillWithFlip(self, mock_choose):
        mock_choose.side_effect = [[Domino(0, 0)],
                                   [Domino(0, 1)]]
        dummy_random = DummyRandom(randints={(0, 3): [1, 1],   # directions
                                             (0, 1): [1, 1]})  # flips
        board = Board(2, 2, max_pips=6)
        expected_display = """\
0 0
- -
0 1
"""

        board.fill(dummy_random)
        display = board.display()

        self.assertMultiLineEqual(expected_display, display)

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFillWithMoreRotation(self, mock_choose):
        mock_choose.side_effect = [[Domino(0, 0)],
                                   [Domino(0, 1)],
                                   [Domino(0, 2)],
                                   [Domino(0, 2)],
                                   [Domino(0, 2)],
                                   [Domino(0, 2)]]
        dummy_random = DummyRandom(randints={(0, 3): [1, 1, 1]})  # directions
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

    @patch('domino_puzzle.Board.choose_extra_dominoes')
    def testFillWithBacktrack(self, mock_choose):
        """ Force a backtrack.

        This scenario will get to the following grid and then be forced to
        backtrack, because the gaps are size 1 and 3: odd.
        x 3 x x
          -
        0 0 x 2
        -     -
        0 0|1 0
        """
        mock_choose.side_effect = [[Domino(0, 0)],
                                   [Domino(0, 1)],
                                   [Domino(0, 2)],
                                   [Domino(0, 3)],
                                   [Domino(0, 3)],
                                   [Domino(0, 3)],
                                   [Domino(0, 3)],
                                   [Domino(0, 4)],
                                   [Domino(0, 5)]]
        dummy_random = DummyRandom(
            randints={(0, 3): [1, 0, 1, 1]})  # directions
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

    def testFillFailForMatching(self):
        """ Fail because all of the remaining dominoes have matches.
        """
        random = Random()
        start = """\
0 x x
-
0 1|1
"""
        board = Board.create(start, max_pips=1)

        result = board.fill(random, matches_allowed=False)

        self.assertFalse(result)
        self.assertMultiLineEqual(start, board.display())

    def testFillFailForBadFit(self):
        """ Fail because a domino won't fit in the hole.

        Don't bother trying other dominoes.
        """
        random = Random()
        start = """\
x 3 4 x
  - -
0 1 0 2
-     -
5 0|1 0
"""
        board = Board.create(start, max_pips=6)

        result = board.fill(random, matches_allowed=False)

        self.assertFalse(result)
        self.assertMultiLineEqual(start, board.display())

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

    def testHasNoMatch(self):
        state = """\
1 0
- -
0 2
"""
        board = Board.create(state)

        self.assertFalse(board.hasMatch())

    def testHasMatch(self):
        state = """\
1 2
- -
0 0
"""
        board = Board.create(state)

        self.assertTrue(board.hasMatch())

    def testFindNoMatch(self):
        state = """\
1 0
- -
0 2
"""
        board = Board.create(state)
        matches = board.findMatches()
        expected_matches = []

        self.assertEqual(expected_matches, matches)

    def testFindMatch(self):
        state = """\
1 2
- -
0 0
"""
        board = Board.create(state)
        matches = board.findMatches()
        coordinates = [(cell.x, cell.y) for cell in matches]
        expected_coordinates = [(0, 0), (1, 0)]

        self.assertEqual(expected_coordinates, coordinates)

    def testHasEvenGapsNoGaps(self):
        state = """\
4|5 6 0
    - -
1 2 1 5
- -
0 3 2|4
"""
        board = Board.create(state)
        has_even_gaps = board.hasEvenGaps()

        self.assertTrue(has_even_gaps)

    def testHasEvenGapsTwoUnevenGaps(self):
        state = """\
4|5 x 0
      -
1 2 6 5
- - -
0 3 1 x
"""
        board = Board.create(state)
        has_even_gaps = board.hasEvenGaps()

        self.assertFalse(has_even_gaps)

    def testHasEvenGapsOneEvenGap(self):
        state = """\
4|5 6 0
    - -
1 2 1 5
- -
0 3 x x
"""
        board = Board.create(state)
        has_even_gaps = board.hasEvenGaps()

        self.assertTrue(has_even_gaps)

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

    def testDifferentGap(self):
        state1 = """\
0|4 0|5

0 x x 2
-     -
0 0|1 0
"""
        state2 = """\
0|4 0|5

0 x 0 2
-   - -
0 x 1 0
"""
        board1 = Board.create(state1)
        board2 = Board.create(state2)

        eq_result = (board1 == board2)
        neq_result = (board1 != board2)
        self.assertFalse(eq_result)
        self.assertTrue(neq_result)

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

    def testParseCellsAndDominoes(self):
        state = """\
0 1
-
2 3
"""
        board = Board.create(state)

        self.assertIsInstance(board[0][1].domino, Domino)
        self.assertIsNone(board[1][0].domino)

    def testDisplayCellsAndDominoes(self):
        state = """\
0 1
-
2 3
"""
        board = Board.create(state)
        display = board.display()

        self.assertEqual(display, state)

    def testJoinCellsRight(self):
        state = """\
0 1 1
-
2 3 2
"""
        expected_state = """\
0 1|1
-
2 3 2
"""
        board = Board.create(state)
        cell1 = board[1][1]
        cell2 = board[2][1]

        board.join(cell1, cell2)

        display = board.display()

        self.assertEqual(display, expected_state)
        self.assertEqual(cell1.domino.degrees, 0)
        self.assertEqual(len(board.dominoes), 2)

    def testJoinCellsUp(self):
        state = """\
0 1 1
-
2 3 2
"""
        expected_state = """\
0 1 1
- -
2 3 2
"""
        board = Board.create(state)
        cell1 = board[1][0]
        cell2 = board[1][1]

        board.join(cell1, cell2)

        display = board.display()

        self.assertEqual(display, expected_state)
        self.assertEqual(cell1.domino.degrees, 90)

    def testJoinCellsLeft(self):
        state = """\
0 1 1
-
2 3 2
"""
        expected_state = """\
0 1|1
-
2 3 2
"""
        board = Board.create(state)
        cell1 = board[2][1]
        cell2 = board[1][1]

        board.join(cell1, cell2)

        display = board.display()

        self.assertEqual(display, expected_state)
        self.assertEqual(cell1.domino.degrees, 180)

    def testJoinCellsDown(self):
        state = """\
0 1 1
-
2 3 2
"""
        expected_state = """\
0 1 1
- -
2 3 2
"""
        board = Board.create(state)
        cell1 = board[1][1]
        cell2 = board[1][0]

        board.join(cell1, cell2)

        display = board.display()

        self.assertEqual(display, expected_state)
        self.assertEqual(cell1.domino.degrees, 270)

    def testJoinCellsNotNeighbours(self):
        state = """\
0 1 1
-
2 3 2
"""
        board = Board.create(state)
        cell1 = board[2][1]
        cell2 = board[1][0]

        with self.assertRaisesRegex(ValueError,
                                    r"Cells are not neighbours: 2,1 and 1,0."):
            board.join(cell1, cell2)

    def testJoinCellsNotAvailable(self):
        state = """\
0 1 1
-
2 3 2
"""
        board = Board.create(state)
        cell1 = board[0][0]
        cell2 = board[1][0]

        with self.assertRaisesRegex(ValueError,
                                    r"Cell is not available: 0,0."):
            board.join(cell1, cell2)

    def testSplitDomino(self):
        state = """\
0 1|1
-
2 3 2
"""
        expected_display = """\
0 1|1

2 3 2
"""
        board = Board.create(state)
        domino = board[0][0].domino

        board.split(domino)

        display = board.display()
        self.assertEqual(display, expected_display)
        self.assertEqual(board.dominoes, [Domino(1, 1)])

    def testSplitAll(self):
        state = """\
0 1|1
-
2 3 2
"""
        expected_display = """\
0 1 1

2 3 2
"""
        board = Board.create(state)

        board.split_all()

        display = board.display()
        self.assertEqual(display, expected_display)
        self.assertEqual(board.dominoes, [])
