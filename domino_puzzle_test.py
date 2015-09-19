import unittest

from domino_puzzle import Domino, Cell, Board
    
class DummyRandom(object):
    def __init__(self, choiceIndexes=None, randints=None):
        self.choiceIndexes = choiceIndexes or []
        self.randints = randints or []
        
    def choice(self, seq):
        choiceIndex = self.choiceIndexes.pop(0)
        for i, item in enumerate(seq):
            if i == choiceIndex:
                return item
        raise IndexError(choiceIndex)
    
    def randint(self, a, b):
        return self.randints[(a, b)].pop(0)

class CellTest(unittest.TestCase):
    def testRepr(self):
        cell = Cell(4)

        s = repr(cell)
        
        self.assertEqual("Cell(4)", s)

    def testPips(self):
        cell = Cell(5)
        
        pips = cell.pips
        
        self.assertEqual(5, pips)
    
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

    def testRotate(self):
        board = Board(4, 3)
        domino = Domino(5, 6)
        board.add(domino, 1, 2)
        domino.rotate(-90)
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
        domino = Domino(5, 6)
        board.add(domino, 1, 2)
        domino.move(1, 0)
        expected_display = """\
x x 5|6
       
x x x x
       
x x x x
"""

        display = board.display()
        
        self.assertMultiLineEqual(expected_display, display)
        
    def testMoveLeft(self):
        board = Board(4, 3)
        domino = Domino(5, 6)
        board.add(domino, 1, 2)
        domino.move(-1, 0)
        expected_display = """\
5|6 x x
       
x x x x
       
x x x x
"""

        display = board.display()
        
        self.assertMultiLineEqual(expected_display, display)
        
    def testRotateWithoutBoard(self):
        domino = Domino(5, 6)
        domino.rotate(90)
        
        self.assertEqual(90, domino.degrees)

    def testRotateAndAdd(self):
        board = Board(4, 3)
        domino = Domino(5, 6)
        domino.rotate(-90)
        board.add(domino, 1, 2)
        expected_display = """\
x 5 x x
  -    
x 6 x x
       
x x x x
"""

        display = board.display()
        
        self.assertMultiLineEqual(expected_display, display)
    
class DominoTest(unittest.TestCase):
    def testRepr(self):
        domino = Domino(5, 3)
        
        s = repr(domino)
        
        self.assertEqual("Domino(5, 3)", s)
        
    def testInit(self):
        domino = Domino(5, 3)
        
        pips = domino.head.pips
        
        self.assertEqual(5, pips)
