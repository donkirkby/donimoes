from datetime import datetime, timedelta
from functools import partial
from itertools import chain
from multiprocessing import Pool, Manager
from operator import eq
from queue import Empty
from random import Random
from sys import maxsize
from threading import Thread

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


class BoardError(Exception):
    pass


class BadPositionError(BoardError):
    pass


class Board(object):
    @classmethod
    def create(cls, state, border=0, max_pips=None):
        lines = state.splitlines(False)
        lines.reverse()
        height = (len(lines)+1) // 2
        line_length = height and max(map(len, lines))
        width = height and (line_length+1) // 2
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
        self.add_count = 0
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
            except BadPositionError:
                self.remove(item.head)
                raise
            self.dominoes.append(item)
            if self.extra_dominoes:
                self.extra_dominoes.remove(item)
        except AttributeError:
            if item.x is not None:
                self.cells[item.x][item.y] = None
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise BadPositionError(
                    'Position {}, {} is off the board.'.format(x, y))
            if self.cells[x][y] is not None:
                raise BadPositionError(
                    'Position {}, {} is occupied.'.format(x, y))
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

    def mutate(self, random, boardType=None, matches_allowed=True):
        # Choose number of mutations: 1 is most common, n is least common
        domino_count = len(self.dominoes)
        n = random.randint(1, (domino_count+1)*domino_count/2)
        mutation_count = 0
        dn = domino_count
        while n > 0:
            mutation_count += 1
            n -= dn
            dn -= 1
        is_successful = False
        while not is_successful:
            # mutation_count = min(mutation_count, 3)
            boardType = boardType or Board
            neighbours = []
            removed = set()
            for _ in range(mutation_count):
                if neighbours:
                    domino = random.choice(neighbours)
                else:
                    domino = random.choice(self.dominoes)
                removed.add(domino)
                neighbours = list(domino.findNeighbours())
            new_board = boardType(self.width,
                                  self.height,
                                  max_pips=self.max_pips)
            for domino in self.dominoes:
                if domino not in removed:
                    i = new_board.extra_dominoes.index(domino)
                    new_domino = new_board.extra_dominoes[i]
                    new_domino.rotate_to(domino.degrees)
                    new_board.add(new_domino, domino.head.x, domino.head.y)
            is_successful = new_board.fill(random,
                                           matches_allowed=matches_allowed)
        return new_board

    def __getitem__(self, x):
        return self.cells[x]

    def __repr__(self):
        return 'Board({}, {})'.format(self.width, self.height)

    def display(self, cropped=False, cropping_bounds=None):
        """ Build a display string for the board's current state.

        @param cropped: True if blank rows and columns around the outside
        should be cropped out of the display.
        @param cropping_bounds: a list that will be cleared and then have
        [xmin, ymin, xmax, ymax] appended to it. Ignored if it is None.
        """
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
        if cropping_bounds is not None:
            cropping_bounds[:] = [xmin, ymin, xmax, ymax]
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

    def choose_extra_dominoes(self, random):
        """ Iterate through self.extra_dominoes, start at random position.

        @return a generator of (domino, is_flipped) pairs. Each domino
            is returned twice, with True or False in random order.
        """
        dominoes = self.extra_dominoes[:]
        count = len(dominoes)
        start = random.randrange(count)
        for i in range(count):
            yield dominoes[(i + start) % count]

    def choose_and_flip_extra_dominoes(self, random):
        """ Iterate through self.extra_dominoes, start at random position.

        @return a generator of (domino, is_flipped) pairs. Each domino
            is returned twice, with True or False in random order.
        """
        for domino in self.choose_extra_dominoes(random):
            if domino.head.pips == domino.tail.pips:
                yield domino, False
            else:
                flip_first = random.randint(0, 1)
                for j in range(2):
                    yield domino, flip_first + j == 1

    def fill(self, random, matches_allowed=True, reset_cycles=True):
        """ Fill any remaining holes in a board with random dominoes.

        @param random: random number generator for choosing dominoes
        @param matches_allowed: True if neighbouring dominoes can match
        @return: True if the board is now filled.
        """
        if reset_cycles:
            self.cycles_remaining = 10000
        for y in range(self.height):
            for x in range(self.width):
                if self[x][y] is None:
                    return self.fillSpace(x,
                                          y,
                                          random,
                                          matches_allowed)
        return True

    def fillSpace(self, x, y, random, matches_allowed):
        """ Try all possible dominoes and positions starting at x, y. """
        rotation = random.randint(0, 3) * 90
        for _ in range(4):
            try:
                choices = self.choose_and_flip_extra_dominoes(
                    random)
                for domino, is_flipped in choices:
                    if self.cycles_remaining <= 0:
                        return False
                    self.cycles_remaining -= 1
                    domino.rotate_to(rotation)
                    self.add(domino, x, y)
                    self.add_count += 1
                    has_even_gaps = self.hasEvenGaps()
                    if not has_even_gaps:
                        self.remove(domino)
                        break
                    else:
                        if is_flipped:
                            domino.flip()
                        if not matches_allowed and domino.hasMatch():
                            pass
                        else:
                            if self.fill(random,
                                         matches_allowed,
                                         reset_cycles=False):
                                return True
                    self.remove(domino)
            except BadPositionError:
                pass
            rotation = (rotation + 90) % 360
        return False

    def visitConnected(self, cell):
        cell.visited = True
        for dx, dy in Domino.directions:
            x = cell.x + dx
            y = cell.y + dy
            if 0 <= x < self.width and 0 <= y < self.height:
                neighbour = self[x][y]
                if neighbour is not None and not neighbour.visited:
                    self.visitConnected(neighbour)

    def isConnected(self):
        domino = None
        for domino in self.dominoes:
            domino.head.visited = False
            domino.tail.visited = False
        if domino is None:
            return True

        self.visitConnected(domino.head)

        return all(domino.head.visited and domino.tail.visited
                   for domino in self.dominoes)

    def hasLoner(self):
        for domino in self.dominoes:
            neighbours = domino.findNeighbours()
            has_matching_neighbour = any(domino.isMatch(neighbour)
                                         for neighbour in neighbours)
            if not has_matching_neighbour:
                return True
        return False

    def hasMatch(self):
        for domino in self.dominoes:
            for cell in (domino.head, domino.tail):
                for neighbour in cell.findNeighbours():
                    if neighbour.pips == cell.pips:
                        return True
        return False

    def findMatches(self):
        matches = {}
        for domino in self.dominoes:
            for match in domino.findMatches():
                matches[(match.x, match.y)] = match
        match_coordinates = sorted(matches.keys())
        return [matches[coord] for coord in match_coordinates]

    def hasEvenGaps(self):
        empty_spaces = set()
        to_visit = set()
        for y in range(self.height):
            for x in range(self.width):
                if self[x][y] is None:
                    empty_spaces.add((x, y))
        while empty_spaces:
            if len(empty_spaces) % 2 != 0:
                return False
            to_visit.add(empty_spaces.pop())
            while to_visit:
                x, y = to_visit.pop()
                for dx, dy in Domino.directions:
                    neighbour = (x+dx, y+dy)
                    try:
                        empty_spaces.remove(neighbour)
                        to_visit.add(neighbour)
                    except KeyError:
                        pass
        return True


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

    @classmethod
    def get_direction(self, name):
        """ Get a direction by name.

        @return: dx, dy
        """
        index = Domino.direction_names.find(name)
        return Domino.directions[index]

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

    def __hash__(self):
        return hash(self.head.pips) ^ hash(self.tail.pips)

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
        except Exception:
            board.add(self, x, y)
            raise

    def describe_move(self, dx, dy):
        direction_index = Domino.directions.index((dx, dy))
        direction_name = Domino.direction_names[direction_index]
        return self.get_name() + direction_name

    def get_name(self):
        name = '{}{}'.format(self.head.pips, self.tail.pips)
        if 90 <= self.degrees <= 180:
            name = name[::-1]  # reverse
        return name

    def flip(self):
        board = self.tail.board
        x, y = self.tail.x, self.tail.y
        board.remove(self)
        self.rotate(180)
        board.add(self, x, y)
        pass

    def calculateDirection(self):
        self.direction = Domino.directions[self.degrees//90]

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

    def hasMatch(self):
        """ True if either cell matches one of its neighbours.

        Slightly different type of matching from isMatch().
        """
        for cell in (self.head, self.tail):
            for neighbour in cell.findNeighbours():
                if neighbour.pips == cell.pips:
                    return True
        return False

    def findMatches(self):
        matches = []
        for cell in (self.head, self.tail):
            is_match = False
            for neighbour in cell.findNeighbours():
                if neighbour.pips == cell.pips:
                    is_match = True
                    matches.append(neighbour)
            if is_match:
                matches.append(cell)
        return matches


class GraphLimitExceeded(RuntimeError):
    def __init__(self, limit):
        super(GraphLimitExceeded, self).__init__(
            'Graph size limit of {} exceeded.'.format(limit))
        self.limit = limit


class BoardGraph(object):
    def walk(self, board, size_limit=maxsize):
        pending_nodes = []
        self.graph = DiGraph()
        self.start = board.display(cropped=True)
        self.graph.add_node(self.start)
        pending_nodes.append(self.start)
        self.min_domino_count = len(board.dominoes)
        self.last = self.start
        while pending_nodes:
            if len(self.graph) >= size_limit:
                raise GraphLimitExceeded(size_limit)
            state = pending_nodes.pop()
            board = Board.create(state, border=1)
            dominoes = set(board.dominoes)
            domino_count = len(dominoes)
            if domino_count < self.min_domino_count:
                self.min_domino_count = domino_count
                self.last = state
            for domino in dominoes:
                dx, dy = domino.direction
                self.try_move(state, domino, dx, dy, pending_nodes)
                self.try_move(state, domino, -dx, -dy, pending_nodes)
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
        except BadPositionError:
            pass

    def move(self, domino, dx, dy):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @return: the new board state
        @raise BadPositionError: if the move is illegal
        """
        domino.move(dx, dy)
        try:
            board = domino.head.board
            if not board.isConnected():
                raise BadPositionError('Board is not connected.')
            if board.hasLoner():
                raise BadPositionError('Board has a lonely domino.')
            return board.display(cropped=True)
        finally:
            domino.move(-dx, -dy)

    def get_solution(self, partial=False):
        """ Find a solution from the graph of moves.

        @param partial: If True, a partial solution will be returned if no
        solution exists.
        @return: a list of strings describing each move. Each string is two
        digits describing the domino that moved plus a letter to show the
        direction.
        """
        solution = []
        goal = self.closest if partial else self.last or ''
        solution_nodes = shortest_path(self.graph, self.start, goal)
        for i in range(len(solution_nodes)-1):
            source, target = solution_nodes[i:i+2]
            solution.append(self.graph[source][target]['move'])
        return solution

    def get_choice_counts(self):
        solution_nodes = shortest_path(self.graph, self.start, self.last)
        return [len(self.graph[node]) for node in solution_nodes[:-1]]

    def get_average_choices(self):
        choices = self.get_choice_counts()
        return sum(choices) / float(len(choices))

    def get_max_choices(self):
        choices = self.get_choice_counts()
        return max(choices)


class CaptureBoardGraph(BoardGraph):
    def __init__(self):
        super(CaptureBoardGraph, self).__init__()
        self.closest = None

    def walk(self, board, size_limit=maxsize):
        states = super(CaptureBoardGraph, self).walk(board, size_limit)
        self.closest = self.last
        if self.last != '':
            self.last = None
        return states

    def move(self, domino, dx, dy, offset=None):
        """ Move a domino and calculate the new board state.

        Afterward, put the board back in its original state.
        @param domino: the domino to move
        @param dx: the direction to move horizontally
        @param dy: the direction to move vertically
        @param offset: [x, y] position to update after the move, or None.
            The input position is updated to show where that position would
            be on the new board. The numbers are reduced if the border gets
            cropped away.
        @return: the new board state
        @raise BadPositionError: if the move is illegal
        """
        matching_dominoes = set()
        complement_found = False
        domino.move(dx, dy)
        try:
            board = domino.head.board
            if not board.isConnected():
                raise BadPositionError('Board is not connected after move.')
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
                raise BadPositionError(
                    'A legal move must have captures or complements.')
            for matching_domino, _, _ in matching_dominoes:
                board.remove(matching_domino)
            if not board.isConnected():
                raise BadPositionError('Board is not connected after capture.')
            cropping_bounds = [] if offset is not None else None
            new_state = board.display(cropped=True,
                                      cropping_bounds=cropping_bounds)
            if offset is not None:
                offset[0] -= cropping_bounds[0]
                offset[1] -= cropping_bounds[1]
            if self.closest is None or len(new_state) < len(self.closest):
                self.closest = new_state
            return new_state
        finally:
            for matching_domino, x, y in matching_dominoes:
                board.add(matching_domino, x, y)
            domino.move(-dx, -dy)


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

    def __init__(self, board, size_limit=maxsize):
        self.board = board
        self.start = board.display()
        try:
            graph = CaptureBoardGraph()
            states = graph.walk(board, size_limit)
        except GraphLimitExceeded:
            raise
        except Exception:
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


def createRandomBoard(boardType, random, width, height):
    is_successful = False
    while not is_successful:
        board = boardType(width, height, max_pips=6)
        is_successful = board.fill(random, matches_allowed=False)
    return board


def mutateBoard(boardType, random, board):
    return board.mutate(random, boardType=boardType, matches_allowed=False),

SLOW_BOARD_SIZE = 2000
MAX_BOARD_SIZE = 10000  # 140000 Bad, 70000 Mostly Good


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


class LoggingHallOfFame(HallOfFame):
    def __init__(self, maxsize, similar=eq, filename="leader.log"):
        super(LoggingHallOfFame, self).__init__(maxsize, similar)
        self.filename = filename
        with open(self.filename, 'w'):
            pass  # erase file

    def update(self, population):
        old_leader = self and self[0]
        HallOfFame.update(self, population)
        new_leader = self and self[0]
        if new_leader is not old_leader:
            display = new_leader.display()
            assert len(new_leader.dominoes) == (new_leader.width *
                                                new_leader.height)/2, display
            assert 'x' not in display, display
            with open(self.filename, 'a') as f:
                f.write(display)

    def display(self):
        for board in self:
            print()
            print(board.display())
            score = board.fitness.values[0]
            if score < 0:
                print('{} score.'.format(score))
            else:
                analysis = BoardAnalysis(board)
                print(analysis.display())


def monitor(hall_of_fame):
    while True:
        cmd = input("Enter 'p' to print report.\n")
        if cmd == 'p':
            hall_of_fame.display()


def findCaptureBoardsWithDeap():
    print('Starting.')
    random = Random()
    manager = Manager()
    slow_queue = manager.Queue()
    results_queue = manager.Queue()
    creator.create("FitnessMax", base.Fitness, weights=BoardAnalysis.WEIGHTS)
    creator.create("Individual",
                   Board,
                   fitness=creator.FitnessMax)  # @UndefinedVariable

    CXPB, MUTPB, NPOP, NGEN, WIDTH, HEIGHT = 0.0, 0.5, 1000, 300, 4, 3
    toolbox = base.Toolbox()
    pool = Pool()
    halloffame = LoggingHallOfFame(10)
    pool.apply_async(evaluateSlowBoards, [slow_queue, results_queue])
    toolbox.register("map", loggedMap, pool)
    toolbox.register("individual",
                     createRandomBoard,
                     creator.Individual,  # @UndefinedVariable
                     random,
                     WIDTH,
                     HEIGHT)
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

    pop = toolbox.population(n=NPOP)
    stats = Statistics()
    stats.register("best", BoardAnalysis.best_score)
    verbose = True
    bg = Thread(target=monitor, args=(halloffame, ))
    bg.daemon = True
    bg.start()
    eaSimple(pop, toolbox, CXPB, MUTPB, NGEN, stats, halloffame, verbose)
    halloffame.display()


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
    print(analysis.display())


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
