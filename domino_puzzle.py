from random import Random

class Cell(object):
    def __init__(self, pips):
        self.pips = pips
        self.domino = None
        self.board = None
        self.x = None
        self.y = None
    
    def __repr__(self):
        return 'Cell({})'.format(self.pips)

class BoardError(StandardError):
    pass

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
            try:
                self.add(item.tail, x+dx, y+dy)
            except BoardError:
                self.remove(item.head)
                raise
        except AttributeError:
            if item.x is not None:
                self.cells[item.x][item.y] = None
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise BoardError('Position {}, {} is off the board.'.format(x, y))
            if self.cells[x][y] is not None:
                raise BoardError('Position {}, {} is occupied.'.format(x, y))
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
            item.x = item.y = item.board = None
    
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
    
    def fill(self, dominoes, random):
        for y in range(self.height):
            for x in range(self.width):
                if self[x][y] is None:
                    domino_index = random.randint(0, len(dominoes)-1)
                    domino = dominoes.pop(domino_index)
                    rotation = random.randint(0, 4) * 90
                    domino.rotate(rotation)
                    for _ in range(4):
                        try:
                            self.add(domino, x, y)
                            if random.randint(0, 1):
                                domino.flip()
                            if self.fill(dominoes, random):
                                return True
                            self.remove(domino)
                        except BoardError:
                            pass
                        domino.rotate(90)
                    dominoes.insert(domino_index, domino)
                    return False
        return True
    
class Domino(object):
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    @classmethod
    def create(cls, max_pips):
        dominoes = []
        for head_pips in range(max_pips+1):
            for tail_pips in range(head_pips, max_pips+1):
                dominoes.append(Domino(head_pips, tail_pips))
        return dominoes
    
    def __init__(self, head_pips, tail_pips):
        self.head = Cell(head_pips)
        self.tail = Cell(tail_pips)
        self.head.domino = self
        self.tail.domino = self
        self.degrees = 0 # 0, 90, 180, or 270
        self.calculateDirection()
        
    def __repr__(self):
        return "Domino({}, {})".format(self.head.pips, self.tail.pips)
    
    def __eq__(self, other):
        return (self.head.pips == other.head.pips and
                self.tail.pips == other.tail.pips)
    
    def rotate(self, degrees):
        self.degrees = (self.degrees + degrees) % 360
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
    
    def flip(self):
        board = self.tail.board
        x, y = self.tail.x, self.tail.y
        board.remove(self)
        self.rotate(180)
        board.add(self, x, y)
        pass
        
    def calculateDirection(self):
        self.direction = Domino.directions[self.degrees/90]

if __name__ == '__main__':
    print 'Searching...'
    random = Random()
    board = Board(8, 7)
    dominoes = Domino.create(6)
    board.fill(dominoes, random)
    print board.display()
    
elif __name__ == '__live_coding__':
    import unittest
    def testSomething(self):
        dummy_random = DummyRandom(randints={(0, 4): [1, 1], # directions
                                             (0, 1): [0, 1]})# flips
        dominoes = Domino.create(6)
        board = Board(7, 8)
        expected_display = """\
0 0
- -
0 1
"""
        
        board.fill(dominoes, dummy_random)
        display = board.display()
        
        self.assertMultiLineEqual(expected_display, display)
    
    class DummyRandom(object):
        def __init__(self, randints=None):
            self.randints = randints or {}
        
        def randint(self, a, b):
            results = self.randints.get((a, b), None)
            return results.pop(0) if results else 0 
        
    class DummyTest(unittest.TestCase):
        
        def test_delegation(self):
            testSomething(self)

    suite = unittest.TestSuite()
    suite.addTest(DummyTest("test_delegation"))
    test_results = unittest.TextTestRunner().run(suite)

    print(test_results.errors)
    print(test_results.failures)
