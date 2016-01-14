from datetime import datetime, timedelta
from functools import partial
from itertools import chain
from multiprocessing import Pool, Manager
from Queue import Empty
from random import Random
from sys import maxint

from deap import base, creator, tools
from deap.algorithms import eaSimple
from deap.tools.support import Statistics, HallOfFame
import matplotlib
from networkx.classes.digraph import DiGraph
from networkx.algorithms.shortest_paths.generic import shortest_path

# Avoid loading Tkinter back end when we won't use it.
matplotlib.use('Agg')
import matplotlib.pyplot as plt  # @IgnorePep8


class Cell(object):
    def __init__(self, pips):
        self.pips = pips
        self.domino = None
        self.board = None
        self.x = None
        self.y = None

    def __repr__(self):
        return 'Cell({})'.format(self.pips)

    def findNeighbourCells(self, dx, dy, exclude_sibling=True):
        x = self.x + dx
        y = self.y + dy
        board = self.board
        if 0 <= x < board.width and 0 <= y < board.height:
            neighbour = board[x][y]
            if (exclude_sibling and
                    neighbour is not None and
                    neighbour.domino is self.domino):
                pass
            elif neighbour is not None:
                yield neighbour

    def findNeighbours(self, exclude_sibling=True):
        return chain(
            self.findNeighbourCells(0, 1, exclude_sibling=exclude_sibling),
            self.findNeighbourCells(1, 0, exclude_sibling=exclude_sibling),
            self.findNeighbourCells(0, -1, exclude_sibling=exclude_sibling),
            self.findNeighbourCells(-1, 0, exclude_sibling=exclude_sibling))


class BoardError(StandardError):
    pass


class Board(object):
    @classmethod
    def create(cls, state, border=0, max_pips=None):
        lines = state.splitlines(False)
        lines.reverse()
        height = (len(lines)+1) / 2
        line_length = height and max(map(len, lines))
        width = height and (line_length+1) / 2
        lines = [line + ((line_length-len(line)) * ' ') for line in lines]
        board = cls(width + 2*border, height + 2*border, max_pips=max_pips)
        for x in range(width):
            for y in range(height):
                head = lines[y*2][x*2]
                if head != 'x':
                    right_joint = x+1 < width and lines[y*2][x*2+1] or ' '
                    upper_joint = y+1 < height and lines[y*2+1][x*2] or ' '
                    if right_joint != ' ':
                        tail = lines[y*2][x*2+2]
                        degrees = 0
                    elif upper_joint != ' ':
                        tail = lines[y*2+2][x*2]
                        degrees = 90
                    else:
                        tail = None
                    if tail:
                        domino = Domino(int(head), int(tail))
                        domino.rotate(degrees)
                        board.add(domino, x+border, y+border)
        return board

    def __init__(self, width, height, max_pips=None):
        self.width = width
        self.height = height
        self.dominoes = []
        self.max_pips = max_pips
        if max_pips is None:
            self.extra_dominoes = []
        else:
            self.extra_dominoes = Domino.create(max_pips)
        self.cells = []
        for _ in range(width):
            self.cells.append([None] * height)

    def __eq__(self, other):
        for x in range(self.width):
            for y in range(self.height):
                cell1 = self[x][y]
                cell2 = other[x][y]
                if cell1 is None or cell2 is None:
                    if cell1 is not cell2:
                        return False
                elif cell1.pips != cell2.pips or cell1.domino != cell2.domino:
                    return False
        return True

    def __ne__(self, other):
        return not (self == other)

    def add(self, item, x, y):
        try:
            dx, dy = item.direction
            self.add(item.head, x, y)
            try:
                self.add(item.tail, x+dx, y+dy)
            except BoardError:
                self.remove(item.head)
                raise
            self.dominoes.append(item)
            if self.extra_dominoes:
                self.extra_dominoes.remove(item)
        except AttributeError:
            if item.x is not None:
                self.cells[item.x][item.y] = None
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise BoardError('Position {}, {} is off the board.'.format(x,
                                                                            y))
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
            self.extra_dominoes.append(item)
        except AttributeError:
            self.cells[item.x][item.y] = None
            item.x = item.y = item.board = None

    def mutate(self, random, boardType=None):
        boardType = boardType or Board
        domino1 = random.choice(self.dominoes)
        neighbours = list(domino1.findNeighbours())
        domino2 = neighbours and random.choice(neighbours) or domino1
        new_board = boardType(self.width, self.height, max_pips=self.max_pips)
        for domino in self.dominoes:
            if domino != domino1 and domino != domino2:
                i = new_board.extra_dominoes.index(domino)
                new_domino = new_board.extra_dominoes[i]
                new_domino.rotate_to(domino.degrees)
                new_board.add(new_domino, domino.head.x, domino.head.y)
        new_board.fill(random)
        return new_board

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
        return ''.join(''.join(row).rstrip() + '\n' for row in display)

    def fill(self, random):
        for y in range(self.height):
            for x in range(self.width):
                if self[x][y] is None:
                    domino = random.choice(self.extra_dominoes)
                    rotation = random.randint(0, 4) * 90
                    domino.rotate(rotation)
                    for _ in range(4):
                        try:
                            self.add(domino, x, y)
                            if random.randint(0, 1):
                                domino.flip()
                            if self.fill(random):
                                return True
                            self.remove(domino)
                        except BoardError:
                            pass
                        domino.rotate(90)
                    return False
        return True

    def getCells(self):
        for domino in self.dominoes:
            yield domino.head
            yield domino.tail

    def isConnected(self):
        def visitConnected(cell):
            cell.visited = True
            for neighbour in cell.findNeighbours(exclude_sibling=False):
                if not neighbour.visited:
                    visitConnected(neighbour)

        cell = None
        for cell in self.getCells():
            cell.visited = False
        if cell is None:
            return True

        visitConnected(cell)

        return all((cell.visited for cell in self.getCells()))

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
    direction_names = 'ruld'

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
        self.degrees = 0  # 0, 90, 180, or 270
        self.calculateDirection()

    def __repr__(self):
        return "Domino({}, {})".format(self.head.pips, self.tail.pips)

    def __eq__(self, other):
        return ((self.head.pips == other.head.pips and
                 self.tail.pips == other.tail.pips) or
                (self.head.pips == other.tail.pips and
                 self.tail.pips == other.head.pips))

    def __ne__(self, other):
        return not (self == other)

    def rotate(self, degrees):
        self.rotate_to((self.degrees + degrees) % 360)

    def rotate_to(self, degrees):
        self.degrees = degrees
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

    def describe_move(self, dx, dy):
        name = '{}{}'.format(self.head.pips, self.tail.pips)
        if 90 <= self.degrees <= 180:
            name = name[::-1]  # reverse
        direction_index = self.directions.index((dx, dy))
        direction_name = self.direction_names[direction_index]
        return name + direction_name

    def flip(self):
        board = self.tail.board
        x, y = self.tail.x, self.tail.y
        board.remove(self)
        self.rotate(180)
        board.add(self, x, y)
        pass

    def calculateDirection(self):
        self.direction = Domino.directions[self.degrees/90]

    def findNeighbours(self):
        neighbour_cells = chain(self.head.findNeighbours(),
                                self.tail.findNeighbours())
        neighbour_dominoes = set(cell.domino for cell in neighbour_cells)
        return neighbour_dominoes

    def isMatch(self, other):
        return (self.head.pips == other.head.pips or
                self.tail.pips == other.tail.pips or
                self.head.pips == other.tail.pips or
                self.tail.pips == other.head.pips)


class GraphLimitExceeded(RuntimeError):
    def __init__(self, limit):
        super(GraphLimitExceeded, self).__init__(
            'Graph size limit of {} exceeded.'.format(limit))
        self.limit = limit


class BoardGraph(object):
    def walk(self, board, size_limit=maxint):
        pending_nodes = []
        self.graph = DiGraph()
        self.start = board.display(cropped=True)
        self.graph.add_node(self.start)
        pending_nodes.append(self.start)
        self.min_domino_count = len(board.dominoes)
        while pending_nodes:
            if len(self.graph) >= size_limit:
                raise GraphLimitExceeded(size_limit)
            state = pending_nodes.pop()
            board = Board.create(state, border=1)
            dominoes = set(board.dominoes)
            self.min_domino_count = min(self.min_domino_count, len(dominoes))
            for domino in dominoes:
                dx, dy = domino.direction
                self.try_move(state, domino, dx, dy, pending_nodes)
                self.try_move(state, domino, -dx, -dy, pending_nodes)
        self.last = state
        return set(self.graph.nodes())

    def try_move(self, old_state, domino, dx, dy, pending_states):
        try:
            new_state = self.move(domino, dx, dy)
            move = domino.describe_move(dx, dy)
            if not self.graph.has_node(new_state):
                # new node
                self.graph.add_node(new_state)
                pending_states.append(new_state)
            self.graph.add_edge(old_state, new_state, move=move)
        except BoardError:
            pass

    def move(self, domino, dx, dy):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state
        @raise BoardError: if the move is illegal
        """
        domino.move(dx, dy)
        try:
            board = domino.head.board
            if not board.isConnected():
                raise BoardError('Board is not connected.')
            if board.hasLoner():
                raise BoardError('Board has a lonely domino.')
            return board.display(cropped=True)
        finally:
            domino.move(-dx, -dy)


class CaptureBoardGraph(BoardGraph):
    def move(self, domino, dx, dy):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state
        @raise BoardError: if the move is illegal
        """
        matching_dominoes = set()
        complement_found = False
        domino.move(dx, dy)
        try:
            board = domino.head.board
            if not board.isConnected():
                raise BoardError('Board is not connected after move.')
            for cell in (domino.head, domino.tail):
                for neighbour in cell.findNeighbours():
                    if neighbour.pips == cell.pips:
                        matching_dominoes.add((neighbour.domino,
                                               neighbour.domino.head.x,
                                               neighbour.domino.head.y))
                    complement_found = (complement_found or
                                        neighbour.pips + cell.pips == 6)
            if matching_dominoes:
                matching_dominoes.add((domino, domino.head.x, domino.head.y))
            elif not complement_found:
                raise BoardError(
                    'A legal move must have captures or complements.')
            for matching_domino, _, _ in matching_dominoes:
                board.remove(matching_domino)
            if not board.isConnected():
                raise BoardError('Board is not connected after capture.')
            return board.display(cropped=True)
        finally:
            for matching_domino, x, y in matching_dominoes:
                board.add(matching_domino, x, y)
            domino.move(-dx, -dy)

    def get_solution(self):
        solution_nodes = shortest_path(self.graph, self.start, '')
        solution = []
        for i in range(len(solution_nodes)-1):
            source, target = solution_nodes[i:i+2]
            solution.append(self.graph[source][target]['move'])
        return solution

    def get_choice_counts(self):
        solution_nodes = shortest_path(self.graph, self.start, '')
        return [len(self.graph[node]) for node in solution_nodes[:-1]]

    def get_average_choices(self):
        choices = self.get_choice_counts()
        return sum(choices) / float(len(choices))

    def get_max_choices(self):
        choices = self.get_choice_counts()
        return max(choices)


class BoardAnalysis(object):
    WEIGHTS = (-1, -1, 1, -1, -1)

    @classmethod
    def calculate_score(cls, values):
        (min_dominoes,
         max_choices,
         solution_length,
         avg_choices,
         _graph_size) = values
        if min_dominoes > 0:
            return -min_dominoes*100
        return max_choices * 100 - solution_length + avg_choices * 0.1

    @classmethod
    def best_score(cls, population):
        scores = [cls.calculate_score(ind.fitness.values)
                  for ind in population]
        positives = [score for score in scores if score > 0]
        if positives:
            return min(positives)
        return max(score for score in scores if score <= 0)

    def get_values(self):
        return (self.min_dominoes,
                self.max_choices,
                len(self.solution),
                self.average_choices,
                self.graph_size)

    def __init__(self, board, size_limit=maxint):
        self.board = board
        self.start = board.display()
        try:
            graph = CaptureBoardGraph()
            states = graph.walk(board, size_limit)
        except GraphLimitExceeded:
            raise
        except StandardError:
            print self.start
            raise
        self.min_dominoes = graph.min_domino_count
        self.graph_size = len(graph.graph)
        if '' not in states:
            self.solution = self.choice_counts = []
            self.average_choices = self.max_choices = 0
        else:
            self.solution = graph.get_solution()
            self.average_choices = graph.get_average_choices()
            self.max_choices = graph.get_max_choices()
            self.choice_counts = graph.get_choice_counts()

    def display(self):
        score = BoardAnalysis.calculate_score(self.get_values())
        return ('{} score, {} nodes{}{}, '
                'avg {} and max {} choices {}').format(
                    score,
                    self.graph_size,
                    200 * ' ',
                    ', '.join(self.solution),
                    self.average_choices,
                    self.max_choices,
                    self.choice_counts)


def createRandomBoard(boardType, random):
    board = boardType(3, 2, max_pips=6)
    board.fill(random)
    return board


def mutateBoard(boardType, random, board):
    return board.mutate(random, boardType=boardType),

SLOW_BOARD_SIZE = 2000
MAX_BOARD_SIZE = 70000  # 140000 Bad, 70000 Good


def evaluateBoard(slow_queue, individual):
    try:
        analysis = BoardAnalysis(individual, size_limit=SLOW_BOARD_SIZE)
        return analysis.get_values()
    except GraphLimitExceeded:
        slow_queue.put(individual.display())
        return (len(individual.dominoes) + 1), 0, 0, 0, 0


def evaluateSlowBoards(slow_queue, results_queue):
    while True:
        start = slow_queue.get()
        board = Board.create(start, max_pips=6)
        try:
            analysis = BoardAnalysis(board, size_limit=MAX_BOARD_SIZE)
            results_queue.put((start, analysis.get_values()))
        except GraphLimitExceeded:
            pass

scores = []
graph_sizes = []


def loggedMap(pool, function, *args):
    results = pool.map(function, *args)
    if function.func is evaluateBoard:
        for fitness_values in results:
            graph_size = fitness_values[-1]
            score = BoardAnalysis.calculate_score(fitness_values)
            graph_sizes.append(graph_size)
            scores.append(score)
        iterations = len(scores)
        plt.title('Score vs. Graph Size (n={})'.format(iterations))
        plt.plot(graph_sizes, scores, 'o', alpha=0.3)
        plt.ylabel("score")
        plt.xlabel("graph size")
        plt.savefig('scores.png')
        plt.close()
    return results


def selectBoards(selector,
                 results_queue,
                 hall_of_fame,
                 boardType,
                 population,
                 count):
    try:
        while True:
            start, fitness_values = results_queue.get_nowait()
            board = boardType.create(start, max_pips=6)
            board.fitness.values = fitness_values
            graph_size = fitness_values[-1]
            score = BoardAnalysis.calculate_score(fitness_values)
            scores.append(score)
            graph_sizes.append(graph_size)
            hall_of_fame.update([board])
            population.append(board)
    except Empty:
        pass
    return selector(population, count)


def findCaptureBoardsWithDeap():
    random = Random()
    manager = Manager()
    slow_queue = manager.Queue()
    results_queue = manager.Queue()
    creator.create("FitnessMax", base.Fitness, weights=BoardAnalysis.WEIGHTS)
    creator.create("Individual",
                   Board,
                   fitness=creator.FitnessMax)  # @UndefinedVariable

    toolbox = base.Toolbox()
    pool = Pool()
    halloffame = HallOfFame(10)
    pool.apply_async(evaluateSlowBoards, [slow_queue, results_queue])
    toolbox.register("map", loggedMap, pool)
    toolbox.register("individual",
                     createRandomBoard,
                     creator.Individual,  # @UndefinedVariable
                     random)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate",
                     mutateBoard,
                     creator.Individual,  # @UndefinedVariable
                     random)
    toolbox.register("select",
                     selectBoards,
                     partial(tools.selTournament, tournsize=3),
                     results_queue,
                     halloffame,
                     creator.Individual)  # @UndefinedVariable
    toolbox.register("evaluate", evaluateBoard, slow_queue)

    pop = toolbox.population(n=100)
    CXPB, MUTPB, NGEN = 0.0, 0.5, 3000
    stats = Statistics()
    stats.register("best", BoardAnalysis.best_score)
    verbose = True
    eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats, halloffame, verbose)
    for board in halloffame:
        print
        print board.display()
        score = board.fitness.values[0]
        if score < 0:
            print('{} score.'.format(score))
        else:
            analysis = BoardAnalysis(board)
            print(analysis.display())


def testPerformance():
    state = """\
1|2 4|5 1|1

1|4 5|3 1|0

4 0 2|0 6|2
- -
2 5 4 6|6 2
    -     -
6 4 4 0|4 2
- -
0 3 4|6 2|5
"""
    board = Board.create(state, max_pips=6)
    analysis = BoardAnalysis(board)
    print analysis.display()


def analyseRandomBoard(random):
    # start_time = datetime.now()
    board = Board(6, 5, max_pips=6)
    board.fill(random)
    analysis = BoardAnalysis(board)
    # duration = (datetime.now() - start_time).total_seconds()
    return analysis.graph_size, analysis.score


def plotPerformance():
    iterations = 20
    random = Random()
    end_time = datetime.now() + timedelta(minutes=10)
    sizes = []
    scores = []
    while datetime.now() < end_time:
        size, score = analyseRandomBoard(random)
        sizes.append(size)
        scores.append(score)
    plt.title('Score vs. Graph Size (n={})'.format(iterations))
    plt.plot(sizes, scores, 'o', alpha=0.5)
    plt.ylabel("score")
    plt.xlabel("graph size")
    plt.savefig('times.png')
    print('Done.')


if __name__ == '__main__':
    # plotPerformance()
    findCaptureBoardsWithDeap()
    # testPerformance()
elif __name__ == '__live_coding__':
    import unittest

    def testSomething(self):
        state = """\
1 0|2 x x
-
0 0|4 0|3
"""
        board = Board.create(state)

        self.assertTrue(board.isConnected())

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

    class DummyTest(unittest.TestCase):

        def test_delegation(self):
            testSomething(self)

    suite = unittest.TestSuite()
    suite.addTest(DummyTest("test_delegation"))
    test_results = unittest.TextTestRunner().run(suite)

    print(test_results.errors)
    print(test_results.failures)
