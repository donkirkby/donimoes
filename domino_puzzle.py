from random import Random
import os

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
    @classmethod
    def create(cls, state, border=0):
        lines = state.splitlines(False)
        lines.reverse()
        height = (len(lines)+1) / 2
        width = (len(lines[0])+1) / 2
        board = Board(width + 2*border, height + 2*border)
        for x in range(width):
            for y in range(height):
                head = lines[y*2][x*2]
                if head != 'x':
                    right_joint = x+1 < width and lines[y*2][x*2+1]
                    upper_joint = y+1 < height and lines[y*2+1][x*2]
                    if right_joint == '|':
                        tail = lines[y*2][x*2+2]
                        degrees = 0
                    elif upper_joint == '-':
                        tail = lines[y*2+2][x*2]
                        degrees = 90
                    else:
                        tail = None
                    if tail:
                        domino = Domino(int(head), int(tail))
                        domino.rotate(degrees)
                        board.add(domino, x+border, y+border)
        return board
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dominoes = set()
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
            self.dominoes.add(item)
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
            self.dominoes.remove(item)
        except AttributeError:
            self.cells[item.x][item.y] = None
            item.x = item.y = item.board = None
    
    def __getitem__(self, x):
        return self.cells[x]
    
    def __repr__(self):
        return 'Board({}, {})'.format(self.width, self.height)
    
    def display(self, cropped=False):
        if not cropped:
            xmin = ymin = 0
            xmax, ymax = self.width-1, self.height-1
        else:
            xmin = self.width
            ymin = self.height
            xmax = ymax = 0
            for domino in self.dominoes:
                for cell in (domino.head, domino.tail):
                    xmin = min(xmin, cell.x)
                    xmax = max(xmax, cell.x)
                    ymin = min(ymin, cell.y)
                    ymax = max(ymax, cell.y)
        width = xmax-xmin+1
        height = ymax-ymin+1
        display = [[' '] * (width*2-1) for _ in range(height*2-1)]

        for y in range(height):
            for x in range(width):
                row = (height - y - 1)*2
                col = x*2
                cell = self[x+xmin][y+ymin]
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
    
    def isConnected(self):
        visited = set()
        unvisited = set()
        for domino in self.dominoes:
            unvisited.add(domino)
            break
        while unvisited:
            domino = unvisited.pop()
            new_neighbours = domino.findNeighbours()
            unvisited |= new_neighbours - visited
            visited.add(domino)
            
        return visited == self.dominoes
    
    def hasLoner(self):
        for domino in self.dominoes:
            neighbours = domino.findNeighbours()
            has_matching_neighbour = any(domino.isMatch(neighbour)
                                         for neighbour in neighbours)
            if not has_matching_neighbour:
                return True
        return False
    
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
        x = self.head.x
        y = self.head.y
        board = self.head.board
        board.remove(self)
        try:
            board.add(self, x+dx, y+dy)
        except StandardError:
            board.add(self, x, y)
            raise
    
    def flip(self):
        board = self.tail.board
        x, y = self.tail.x, self.tail.y
        board.remove(self)
        self.rotate(180)
        board.add(self, x, y)
        pass
        
    def calculateDirection(self):
        self.direction = Domino.directions[self.degrees/90]
    
    def findNeighbourCell(self, dx, dy):
        x = self.head.x + dx
        y = self.head.y + dy
        board = self.head.board
        if 0 <= x < board.width and 0 <= y < board.height:
            return board[x][y]
        
    def findNeighbours(self):
        neighbour_cells = set()
        dx, dy = self.direction
        neighbour_cells.add(self.findNeighbourCell(-dx, -dy))
        neighbour_cells.add(self.findNeighbourCell(2*dx, 2*dy))
        neighbour_cells.add(self.findNeighbourCell(dy, dx))
        neighbour_cells.add(self.findNeighbourCell(-dy, -dx))
        neighbour_cells.add(self.findNeighbourCell(dx+dy, dy+dx))
        neighbour_cells.add(self.findNeighbourCell(dx-dy, dy-dx))
        neighbour_cells.discard(None)
        neighbour_dominoes = set([cell.domino for cell in neighbour_cells])
        return neighbour_dominoes
    
    def isMatch(self, other):
        return (self.head.pips == other.head.pips or
                self.tail.pips == other.tail.pips or
                self.head.pips == other.tail.pips or
                self.tail.pips == other.head.pips)

class BoardGraph(object):
    def walk(self, board):
        complete = set()
        new = set()
        new.add(board.display(cropped=True))
        while new:
            state = new.pop()
            board = Board.create(state, border=1)
            dominoes = board.dominoes
            for domino in dominoes:
                dx, dy = domino.direction
                self._try_move(domino, dx, dy, new, complete)
                self._try_move(domino, -dx, -dy, new, complete)
            complete.add(state)
        self.last = state
        return complete
    
    def _try_move(self, domino, dx, dy, new, complete):
        try:
            domino.move(dx, dy)
            board = domino.head.board
            new_state = board.display(cropped=True)
            if (new_state not in complete and
                board.isConnected() and
                not board.hasLoner()):
                
                new.add(new_state)
            domino.move(-dx, -dy)
        except BoardError:
            pass
        
def main():
    print 'Searching...'
    out_path = 'problems'
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    random = Random()
    max_states = 0
    best_last = None
    for _ in range(50):
        while True:
            dominoes = Domino.create(6)
            board = Board(5, 4)
            board.fill(dominoes, random)
            if not board.hasLoner():
                break
        graph = BoardGraph()
        states = graph.walk(board)
        state_count = len(states)
        print state_count
        filename = os.path.join(out_path, 'length{:05}.txt'.format(state_count))
        with open(filename, 'a') as f:
            f.write(graph.last + '\n\n\n##########\n\n')
        if len(states) > max_states:
            best_last = graph.last
            max_states = state_count
            
    print Board.create(best_last).display(cropped=True)
    
    """ Interesting puzzles:
    length 58: (good starter)
    x x x x 0 x
            -  
    2|5 3|5 3 x
               
    4|3 4|4 x x
               
    x x 6|1 1|2
               
    6|0 3 x 1|4
        -      
    x x 6 x x x
    
    medium 390:
    x x x x x 5 x x
              -    
    x x x x x 3 x x
                   
    0|3 x x x 3|2 4
                  -
    x 3|6 x x x 3 0
                -  
    x x 3|4 x x 1 4
                  -
    x x x 0|0 0|6 4
    
    challenge 877:
    1|4 1|0 x x x 1
                  -
    x x 3|1 1|2 x 5
                   
    x 0|4 x x 1 5|4
              -    
    0|0 x x x 6 5|2
    
    other:
    
    x x x x x x x x 6 x
                    -  
    x x x x x x x 6 6 x
                  -    
    x x x x 5 4|5 2 2|4
            -          
    x x 5|5 6 x x x 4 x
                    -  
    x 3|5 x x x x x 3 x
                       
    5|1 x x x x x 0|3 x
    
    Another:
    x x 0 x 3 x x x x x x
        -   -            
    0|3 6 x 4 1|5 x x x x
                         
    x x 2|3 5|3 x x x x x
                         
    x x x x x 4|0 x x 3|1
                         
    x x x x x x 0|0 1|4 x    
    """
        
if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    import unittest
    def testSomething(self):
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
