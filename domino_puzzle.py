class Cell(object):
    def __init__(self, pips):
        self.pips = pips
        self.domino = None
        self.board = None
        self.x = None
        self.y = None
    
    def __repr__(self):
        return 'Cell({})'.format(self.pips)

class Board(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = []
        for _ in range(width):
            self.cells.append([None] * height)
    
    def add(self, item, x, y):
        try:
            dx, dy = item.direction
            self.add(item.head, x, y)
            self.add(item.tail, x+dx, y+dy)
        except AttributeError:
            if item.x is not None:
                self.cells[item.x][item.y] = None
            self.cells[x][y] = item
            item.board = self
            item.x = x
            item.y = y
    
    def remove(self, item):
        try:
            self.remove(item.head)
            self.remove(item.tail)
        except AttributeError:
            self.cells[item.x][item.y] = None
            item.x = item.y = None
    
    def __getitem__(self, x):
        return self.cells[x]
    
    def __repr__(self):
        return 'Board({}, {})'.format(self.width, self.height)
    
    def display(self):
        display = [[' '] * (self.width*2-1) for _ in range(self.height*2-1)]

        for y in range(self.height):
            for x in range(self.width):
                row = (self.height - y - 1)*2
                col = x*2
                cell = self[x][y]
                cell_display = 'x' if cell is None else str(cell.pips)
                display[row][col] = cell_display
                if cell is not None and cell.domino.head == cell:
                    dx, dy = cell.domino.direction
                    divider = '|' if dx else '-'
                    display[row-dy][col+dx] = divider
        return ''.join(''.join(row) + '\n' for row in display)

class Domino(object):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    def __init__(self, head_pips, tail_pips):
        self.head = Cell(head_pips)
        self.tail = Cell(tail_pips)
        self.head.domino = self
        self.tail.domino = self
        self.degrees = 0 # 0, 90, 180, or 270
        self.calculateDirection()
        
    def __repr__(self):
        return "Domino({}, {})".format(self.head.pips, self.tail.pips)
    
    def rotate(self, degrees):
        self.degrees = self.degrees + degrees
        self.calculateDirection()
        if self.head.board:
            dx, dy = self.direction
            self.head.board.add(self.tail, self.head.x+dx, self.head.y+dy)
    
    def move(self, dx, dy):
        x = self.head.x + dx
        y = self.head.y + dy
        board = self.head.board
        board.remove(self)
        board.add(self, x, y)
        pass
        
    def calculateDirection(self):
        self.direction = Domino.directions[self.degrees/90]

if __name__ == '__main__':
    print 'Searching...'
elif __name__ == '__live_coding__':
    import unittest
    def testSomething(self):
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
        
    class DummyTest(unittest.TestCase):
        
        def test_delegation(self):
            testSomething(self)

    suite = unittest.TestSuite()
    suite.addTest(DummyTest("test_delegation"))
    test_results = unittest.TextTestRunner().run(suite)

    print(test_results.errors)
    print(test_results.failures)
