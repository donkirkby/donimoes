import random
import typing
from collections import defaultdict, Counter
from enum import Enum
from functools import partial
from itertools import chain
from sys import maxsize

from networkx import shortest_path

from domino_puzzle import Board, Cell, Domino, BoardGraph, GraphLimitExceeded
from evo import Individual, Evolution

PairState = Enum('PairState', 'UNDECIDED NEWLY_JOINED JOINED NEWLY_SPLIT SPLIT')
PairState.state_codes = {' ': PairState.UNDECIDED,
                         'j': PairState.NEWLY_JOINED,
                         '|': PairState.JOINED,
                         '-': PairState.JOINED,
                         's': PairState.NEWLY_SPLIT,
                         'S': PairState.SPLIT,
                         '~': PairState.SPLIT}
PairState.horizontal_displays = {PairState.UNDECIDED: ' ',
                                 PairState.NEWLY_JOINED: 'j',
                                 PairState.JOINED: '|',
                                 PairState.NEWLY_SPLIT: 's',
                                 PairState.SPLIT: 'S'}
PairState.vertical_displays = {PairState.UNDECIDED: ' ',
                               PairState.NEWLY_JOINED: 'j',
                               PairState.JOINED: '-',
                               PairState.NEWLY_SPLIT: 's',
                               PairState.SPLIT: '~'}


class DominosaProblem(Individual):
    def __repr__(self):
        return f'DominosaProblem({self.value!r}'

    def pair(self, other, pair_params):
        # self_head = self.value[:int(len(self.value) * pair_params['alpha'])].copy()
        # self_tail = self.value[int(len(self.value) * pair_params['alpha']):].copy()
        # other_tail = other.value[int(len(other.value) * pair_params['alpha']):].copy()
        #
        # mapping = {other_tail[i]: self_tail[i] for i in range(len(self_tail))}
        #
        # for i in range(len(self_head)):
        #     while self_head[i] in other_tail:
        #         self_head[i] = mapping[self_head[i]]

        # return DominosaProblem(np.hstack([self_head, other_tail]))
        return DominosaProblem(self.value)

    def mutate(self, mutate_params):
        max_pips = self.value['max_pips']
        board = DominosaBoard.create(self.value['solution'],
                                     max_pips=max_pips)
        new_board = board.mutate(random, DominosaBoard)
        self.value = dict(solution=new_board.display(),
                          max_pips=max_pips)

    def _random_init(self, init_params):
        max_pips = init_params['max_pips']
        board = DominosaBoard(**init_params)
        while True:
            if board.fill(random):
                break

        return dict(solution=board.display(),
                    max_pips=max_pips)


def calculate_fitness(problem, move_weights=None):
    value = problem.value
    fitness = value.get('fitness')
    if fitness is not None:
        return fitness
    board = DominosaBoard.create(value['solution'], max_pips=value['max_pips'])
    graph = DominosaGraph(move_weights=move_weights)
    try:
        graph.walk(board, size_limit=10_000)
    except GraphLimitExceeded:
        pass
    dominoes_unused = graph.min_domino_count
    if graph.last is None:
        fitness = -10000 * dominoes_unused
    else:
        fitness = 0
        solution_nodes = shortest_path(graph.graph,
                                       graph.start,
                                       graph.last,
                                       'weight')
        for i in range(len(solution_nodes)-1):
            source, target = solution_nodes[i:i+2]
            edge = graph.graph[source][target]
            fitness -= edge.get('weight', 1)
    value['fitness'] = fitness
    return fitness


def place_unique_pairs(board: Board):
    pairs = find_unique_pairs(board)
    join_pairs(board, pairs)
    return len(pairs)


def join_pairs(board: Board, pairs: typing.List[typing.Tuple[int]]):
    for pair in pairs:
        join_pair(board, *pair)


def find_unique_pairs(board: Board) -> typing.List[typing.Tuple[int]]:
    pair_locations = find_pair_locations(board)
    used_cells = set()

    all_locations = []  # [(x1, x2, y1, y2)]
    for location_list in pair_locations.values():
        if location_list is not None and len(location_list) == 1:
            x1, y1, x2, y2 = location_list[0]
            cell1 = board[x1][y1]
            cell2 = board[x2][y2]
            if cell1 not in used_cells and cell2 not in used_cells:
                all_locations.extend(location_list)
                used_cells.add(cell1)
                used_cells.add(cell2)

    return all_locations


def find_pair_locations(board: Board) -> dict:
    """ Find how many times each pair of numbers appears in the unjoined cells.

    :param board: board to search
    :return: {(small_pips, large_pips): [(x1, y1, x2, y2)]}, but values are
        None if a matching domino has already been placed.
    """
    pair_locations = defaultdict(list)
    for x in range(board.width):
        for y in range(board.height):
            cell = board[x][y]
            if 0 < x:
                record_pair(board[x - 1][y], cell, pair_locations)
            if 0 < y:
                record_pair(board[x][y - 1], cell, pair_locations)
    return pair_locations


def find_matching_pairs(board: Board, x1: int, y1: int, x2: int, y2: int):
    """ Find all pairs that match the pips on the given pair.

    :return: generator of (x1, y1, x2, y2) pairs with the same pips
    """
    yield from find_pairs_by_pips(board, board[x1][y1].pips, board[x2][y2].pips)


def find_pairs_by_pips(board, head_pips, tail_pips):
    """ Find all pairs that match the given pips.

    :return: generator of (x1, y1, x2, y2) pairs with the same pips
    """
    target_pips = {head_pips, tail_pips}
    for x in range(board.width):
        for y in range(board.height):
            head_pips = board[x][y].pips
            pairs = []
            if 0 < x:
                pairs.append((x-1, y, x, y))
            if 0 < y:
                pairs.append((x, y-1, x, y))
            for x1dup, y1dup, x2dup, y2dup in pairs:
                dup_pips = {head_pips, board[x1dup][y1dup].pips}
                if target_pips == dup_pips:
                    yield x1dup, y1dup, x2dup, y2dup


def join_pair(board: Board, x1: int, y1: int, x2: int, y2: int):
    cell1 = board[x1][y1]
    cell2 = board[x2][y2]
    board.join(cell1, cell2)


def record_pair(cell1: Cell, cell2: Cell, pair_locations: dict):
    domino = None
    if cell1.domino is not None:
        # Cell is already assigned to a domino, don't count it.
        domino = cell1.domino
        pair_locations[get_pair_key(domino.head, domino.tail)] = None
    if cell2.domino is not None:
        # Cell is already assigned to a domino, don't count it.
        domino = cell2.domino
        pair_locations[get_pair_key(domino.head, domino.tail)] = None
    if domino is not None:
        return

    key = get_pair_key(cell1, cell2)

    location_list = pair_locations[key]
    if location_list is None:
        # This pair is already joined.
        return

    location = (cell1.x, cell1.y, cell2.x, cell2.y)
    location_list.append(location)


def get_pair_key(cell1, cell2):
    values = [cell1.pips, cell2.pips]
    values.sort()
    key = tuple(values)
    return key


def find_one_neighbour_pairs(board: Board) -> typing.List[typing.Tuple[int]]:
    used_keys = {get_pair_key(domino.head, domino.tail)
                 for domino in board.dominoes}
    pairs = set()
    used_cells = set()
    for cell in find_unjoined_cells(board):
        x = cell.x
        y = cell.y
        if cell in used_cells:
            continue
        neighbours = []
        for dx, dy in Domino.directions:
            x2 = x+dx
            y2 = y+dy
            if 0 <= x2 < board.width and 0 <= y2 < board.height:
                cell2 = board[x2][y2]
                pair_key = get_pair_key(cell, cell2)
                if (cell2.domino is None and
                        cell2 not in used_cells and
                        pair_key not in used_keys):
                    neighbours.append(sorted(((x, y), (x2, y2))))
        if len(neighbours) == 1:
            (x1, y1), (x2, y2) = neighbours[0]
            pairs.add((x1, y1, x2, y2))
            used_cell1 = board[x1][y1]
            used_cells.add(used_cell1)
            used_cell2 = board[x2][y2]
            used_cells.add(used_cell2)
            used_key = get_pair_key(used_cell1, used_cell2)
            used_keys.add(used_key)
    # noinspection PyTypeChecker
    return sorted(pairs)


def find_unjoined_pairs(board: Board) -> typing.List[typing.Tuple[int]]:
    pairs = set()
    for cell in find_unjoined_cells(board):
        x = cell.x
        y = cell.y
        for dx, dy in Domino.directions:
            x2 = x+dx
            y2 = y+dy
            if 0 <= x2 < board.width and 0 <= y2 < board.height:
                cell2 = board[x2][y2]
                if cell2.domino is None:
                    sorted_pair = sorted(((x, y), (x2, y2)))
                    (x1, y1), (x2, y2) = sorted_pair
                    pairs.add((x1, y1, x2, y2))
    # noinspection PyTypeChecker
    return sorted(pairs)


def find_unjoined_cells(board: Board) -> typing.Iterator[Cell]:
    for x in range(board.width):
        for y in range(board.height):
            cell = board[x][y]
            if cell.domino is None:
                yield cell


def check_for_duplicates(board: Board):
    domino_counts = Counter()
    for x in range(board.width):
        for y in range(board.height):
            cell = board[x][y]
            domino = cell.domino
            if domino is not None:
                domino_counts[get_pair_key(domino.head, domino.tail)] += 1
    for key, count in domino_counts.items():
        assert count == 2, (key, count)


class DominosaBoard(Board):
    @classmethod
    def create(cls, state, border=0, max_pips=None):
        # We never want borders for Dominosa boards, because nothing moves.
        return super().create(state, border=0, max_pips=max_pips)

    def __init__(self, width, height, max_pips=None):
        super().__init__(width, height, max_pips)
        self.pair_states = {}

    def get_pair_state(self, x1: int, y1: int, x2: int, y2: int):
        if x2 < x1 or y2 < y1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        return self.pair_states[(x1, y1, x2, y2)]

    def set_pair_state(self,
                       x1: int,
                       y1: int,
                       x2: int,
                       y2: int,
                       pair_state: PairState):
        if x2 < x1 or y2 < y1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        self.pair_states[(x1, y1, x2, y2)] = pair_state

    def add_joint(self, joint: str, x1: int, y1: int, x2: int, y2: int) -> str:
        if not self.is_in_bounds(x1, y1, x2, y2):
            assert joint == ' ', joint
            return joint
        pair_state = PairState.state_codes[joint]
        self.pair_states[(x1, y1, x2, y2)] = pair_state
        if pair_state in (PairState.SPLIT, PairState.NEWLY_SPLIT):
            return ' '
        if pair_state == PairState.NEWLY_JOINED:
            if x1 != x2:
                return '|'
            return '-'
        return joint

    def is_in_bounds(self, x1, y1, x2, y2):
        for value, limit in ((x1, self.width),
                             (x2, self.width),
                             (y1, self.height),
                             (y2, self.height)):
            if value < 0 or limit <= value:
                return False
        return True

    def display(self, cropped=False, cropping_bounds=None):
        cropped = False
        return super().display(cropped, cropping_bounds)

    def split(self, domino):
        x1, y1 = domino.head.x, domino.head.y
        x2, y2 = domino.tail.x, domino.tail.y
        super().split(domino)
        self.set_pair_state(x1, y1, x2, y2, PairState.UNDECIDED)

    def adjust_display(self, display: typing.List[typing.List[str]]):
        if not self.pair_states:
            return
        for x1 in range(self.width):
            for y1 in range(self.height):
                for x2 in (x1, x1+1):
                    for y2 in (y1, y1+1):
                        if x2 >= self.width or y2 >= self.height:
                            # Off the board.
                            continue
                        if (x1 == x2) == (y1 == y2):
                            # Not a neighbour.
                            continue
                        pair_state = self.pair_states[(x1, y1, x2, y2)]
                        if x1 == x2:
                            pair_display = PairState.vertical_displays[pair_state]
                        else:
                            pair_display = PairState.horizontal_displays[pair_state]
                        i = self.height*2 - y1 - y2 - 2
                        j = x1 + x2
                        display[i][j] = pair_display

    def find_neighbours(self, x1, y1, x2, y2):
        """ Yield all neighbouring pairs of this pair, regardless of state. """
        for x_start, y_start in ((x1, y1), (x2, y2)):
            for x1n, y1n, x2n, y2n in ((x_start, y_start, x_start+1, y_start),
                                       (x_start, y_start, x_start, y_start+1),
                                       (x_start-1, y_start, x_start, y_start),
                                       (x_start, y_start-1, x_start, y_start)):
                if (x1n, y1n, x2n, y2n) == (x1, y1, x2, y2):
                    continue
                if self.is_in_bounds(x1n, y1n, x2n, y2n):
                    yield x1n, y1n, x2n, y2n


def generate_moves_from_single_neighbours(board):
    used_cells = set()
    undecided_neighbours = defaultdict(list)  # {(x1, y1): [x2, y2]}
    for (x1, y1, x2, y2), pair_state in board.pair_states.items():
        if pair_state in (PairState.NEWLY_JOINED, PairState.JOINED):
            used_cells.add((x1, y1))
            used_cells.add((x2, y2))
        elif pair_state == PairState.UNDECIDED:
            undecided_neighbours[(x1, y1)].append((x2, y2))
            undecided_neighbours[(x2, y2)].append((x1, y1))
    isolated_cells = {cell
                      for cell, neighbours in undecided_neighbours.items()
                      if len(neighbours) == 1} - used_cells
    for x1, y1 in isolated_cells:
        x2, y2 = undecided_neighbours[(x1, y1)][0]
        board.set_pair_state(x1, y1, x2, y2, PairState.NEWLY_JOINED)
        move = f'1:{x1}{y1}j{x2}{y2}'
        yield move, board.display()
        board.set_pair_state(x1, y1, x2, y2, PairState.UNDECIDED)


def generate_moves_from_newly_joined(board):
    for (x1, y1, x2, y2), pair_state in board.pair_states.items():
        if pair_state != PairState.NEWLY_JOINED:
            continue
        board.set_pair_state(x1, y1, x2, y2, PairState.JOINED)
        move = f'2:{x1}{y1}|{x2}{y2}'
        split_pairs = []
        for x1n, y1n, x2n, y2n in chain(board.find_neighbours(x1, y1, x2, y2),
                                        find_matching_pairs(
                                            board, x1, y1, x2, y2)):
            pair_state2 = board.get_pair_state(x1n, y1n, x2n, y2n)
            if pair_state2 == PairState.UNDECIDED:
                split_pairs.append((x1n, y1n, x2n, y2n))
                board.set_pair_state(x1n, y1n, x2n, y2n, PairState.NEWLY_SPLIT)
                move += f',{x1n}{y1n}s{x2n}{y2n}'

        yield move, board.display()
        board.set_pair_state(x1, y1, x2, y2, PairState.NEWLY_JOINED)
        for x1n, y1n, x2n, y2n in split_pairs:
            board.set_pair_state(x1n, y1n, x2n, y2n, PairState.UNDECIDED)


def generate_moves_from_newly_split(board):
    pair_groups = []  # [[(x1, y1, x2, y2, new_state)]]
    pair_group = []
    for (x1, y1, x2, y2), pair_state in board.pair_states.items():
        if pair_state != PairState.NEWLY_SPLIT:
            continue
        matching_pairs = []
        for x1dup, y1dup, x2dup, y2dup in find_matching_pairs(
                board, x1, y1, x2, y2):
            pair_state2 = board.get_pair_state(x1dup, y1dup, x2dup, y2dup)
            if pair_state2 == PairState.UNDECIDED:
                matching_pairs.append((x1dup, y1dup, x2dup, y2dup))
        pair_group.append((x1, y1, x2, y2, PairState.SPLIT))
        if len(matching_pairs) == 1:
            x1dup, y1dup, x2dup, y2dup = matching_pairs[0]
            has_joined_neighbour = False
            for x1n, y1n, x2n, y2n in board.find_neighbours(x1dup, y1dup,
                                                            x2dup, y2dup):
                neighbour_state = board.get_pair_state(x1n, y1n, x2n, y2n)
                if neighbour_state in (PairState.JOINED, PairState.NEWLY_JOINED):
                    has_joined_neighbour = True
                    break
            if not has_joined_neighbour:
                pair_group.append((x1dup, y1dup, x2dup, y2dup, PairState.NEWLY_JOINED))
                pair_groups.append(pair_group)
                pair_group = []
    for pair_group in pair_groups:
        move = None
        for x1, y1, x2, y2, new_state in pair_group:
            if move:
                move += ','
            else:
                move = '3:'
            state_display = PairState.horizontal_displays[new_state]
            move += f'{x1}{y1}{state_display}{x2}{y2}'
            board.set_pair_state(x1, y1, x2, y2, new_state)
        yield move, board.display()
        for x1, y1, x2, y2, new_state in pair_group:
            if new_state == PairState.SPLIT:
                old_state = PairState.NEWLY_SPLIT
            else:
                old_state = PairState.UNDECIDED
            board.set_pair_state(x1, y1, x2, y2, old_state)


def generate_moves_from_duplicate_neighbours(board):
    """ Generate moves according to rule 4.

    If all of a cell's neighbours are the same, then you know that pair can't
    be linked anywhere else on the board.
    """
    used_cells = set()
    undecided_neighbour_pips = defaultdict(set)  # {(x1, y1): {pips}}
    for (x1, y1, x2, y2), pair_state in board.pair_states.items():
        if pair_state in (PairState.NEWLY_JOINED, PairState.JOINED):
            used_cells.add((x1, y1))
            used_cells.add((x2, y2))
        elif pair_state == PairState.UNDECIDED:
            pip_set1 = undecided_neighbour_pips[(x1, y1)]
            pip_set1.add(board[x2][y2].pips)
            pip_set2 = undecided_neighbour_pips[(x2, y2)]
            pip_set2.add(board[x1][y1].pips)
    surrounded_cells = {cell
                        for cell, pips in undecided_neighbour_pips.items()
                        if len(pips) == 1} - used_cells
    for x1, y1 in surrounded_cells:
        head_pips = board[x1][y1].pips
        tail_pips, = undecided_neighbour_pips[(x1, y1)]
        split_pairs = []  # [(x1dup, y1dup, x2dup, y2dup)]
        move = f'4:{x1}{y1}'
        for x1dup, y1dup, x2dup, y2dup in find_pairs_by_pips(board,
                                                             head_pips,
                                                             tail_pips):
            if (x1, y1) in ((x1dup, y1dup), (x2dup, y2dup)):
                continue
            pair_state = board.get_pair_state(x1dup, y1dup, x2dup, y2dup)
            if pair_state == PairState.UNDECIDED:
                board.set_pair_state(x1dup, y1dup,
                                     x2dup, y2dup,
                                     PairState.NEWLY_SPLIT)
                move += f',{x1dup}{y1dup}s{x2dup}{y2dup}'
                split_pairs.append((x1dup, y1dup, x2dup, y2dup))
        if split_pairs:
            yield move, board.display()
        for x1dup, y1dup, x2dup, y2dup in split_pairs:
            board.set_pair_state(x1dup, y1dup,
                                 x2dup, y2dup,
                                 PairState.UNDECIDED)


def generate_moves_from_shared_spaces(board):
    pair_locations = find_pair_locations(board)
    for (head_pips, tail_pips), pairs in pair_locations.items():
        if pairs is None or len(pairs) == 1:
            continue
        common_cells = set()
        for i, (x1, y1, x2, y2) in enumerate(pairs):
            cells = {(x1, y1), (x2, y2)}
            if i == 0:
                common_cells.update(cells)
            else:
                common_cells.intersection_update(cells)
        if not common_cells:
            continue
        ((x1, y1), ) = common_cells
        common_pips = board[x1][y1].pips
        if common_pips == head_pips:
            needed_pips = tail_pips
        else:
            needed_pips = head_pips
        to_split = []  # [(x2, y2)]
        for x2 in range(x1-1, x1+2):
            if x2 < 0 or board.width <= x2:
                # out of bounds
                continue
            for y2 in range(y1-1, y1+2):
                if y2 < 0 or board.height <= y2:
                    # out of bounds
                    continue
                if (x2 == x1) == (y2 == y1):
                    # on x1, y1 or diagonal
                    continue
                pair_state = board.get_pair_state(x1, y1, x2, y2)
                if pair_state != PairState.UNDECIDED:
                    continue
                neighbour_pips = board[x2][y2].pips
                if neighbour_pips != needed_pips:
                    to_split.append((x2, y2))
        if not to_split:
            continue
        move = f'5:{x1}{y1}'
        for x2, y2 in to_split:
            board.set_pair_state(x1, y1, x2, y2, PairState.NEWLY_SPLIT)
            move += f',{x1}{y1}s{x2}{y2}'
        yield move, board.display()
        for x2, y2 in to_split:
            board.set_pair_state(x1, y1, x2, y2, PairState.UNDECIDED)


def generate_moves_from_unique_pairs(board):
    for x1, y1, x2, y2 in find_unique_pairs(board):
        board.set_pair_state(x1, y1, x2, y2, PairState.NEWLY_JOINED)
        move = f'6:{x1}{y1}j{x2}{y2}'
        yield move, board.display()
        board.set_pair_state(x1, y1, x2, y2, PairState.UNDECIDED)


class DominosaGraph(BoardGraph):
    def __init__(self,
                 board_class=DominosaBoard,
                 move_weights=None,
                 debug=False):
        super().__init__(board_class)
        move_generators = {1: generate_moves_from_single_neighbours,
                           2: generate_moves_from_newly_joined,
                           3: generate_moves_from_newly_split,
                           4: generate_moves_from_duplicate_neighbours,
                           5: generate_moves_from_shared_spaces,
                           6: generate_moves_from_unique_pairs}
        if move_weights is None:
            move_weights = {6: 1}
        self.debug = debug
        selected_rules = sorted(move_weights)
        self.move_generators = [move_generators[rule]
                                for rule in selected_rules]
        self.solution_states = set()
        self.last = None
        self.min_domino_count = None
        self.move_weights = move_weights

    def walk(self, board, size_limit=maxsize):
        board.split_all()
        self.min_domino_count = None
        self.check_progress(board)
        self.solution_states.clear()
        self.last = None
        states = super().walk(board, size_limit)
        return states

    def generate_moves(self, board: DominosaBoard):
        """ Generate all moves from the board's current state.

        :param Board board: the current state
        :return: a generator of (move_description, state) tuples
        """

        for rule in (generator(board)
                     for generator in self.move_generators):
            has_yielded = False
            for move, state in rule:
                if self.debug:
                    print()
                    print(move)
                    print(state)
                new_board: DominosaBoard = self.board_class.create(
                    state,
                    max_pips=board.max_pips)
                self.check_progress(new_board)
                if not new_board.extra_dominoes:
                    state = clean_solution(board)
                    self.solution_states.add(state)
                    if self.last is None:
                        self.last = state
                move_attrs = {}
                if self.move_weights:
                    move_label = move.split(':')[0]
                    move_num = int(move_label)
                    move_attrs['weight'] = self.move_weights[move_num]
                yield move, state, move_attrs
                has_yielded = True
            if has_yielded:
                return

    def check_progress(self, board):
        """ Keep track of which board state was the closest to a solution. """
        if board.max_pips is None:
            raise ValueError('Board does not have max_pips set.')
        domino_count = len(board.extra_dominoes)
        if self.min_domino_count is None or domino_count < self.min_domino_count:
            self.min_domino_count = domino_count


def clean_solution(board: DominosaBoard) -> str:
    old_pair_states = {pair: pair_state
                       for pair, pair_state in board.pair_states.items()
                       if pair_state in (PairState.NEWLY_JOINED,
                                         PairState.NEWLY_SPLIT,
                                         PairState.SPLIT)}
    for pair, pair_state in old_pair_states.items():
        if pair_state == PairState.NEWLY_JOINED:
            board.set_pair_state(*pair, PairState.JOINED)
        else:
            board.set_pair_state(*pair, PairState.UNDECIDED)
    clean_state = board.display()
    for pair, pair_state in old_pair_states.items():
        board.set_pair_state(*pair, pair_state)
    return clean_state


def find_solutions(board: Board,
                   depth: int = 1,
                   verbose: bool = False,
                   max_solutions: typing.Optional[int] = None) -> typing.Set[str]:
    while True:
        rule = 'one neighbour'
        pairs = find_one_neighbour_pairs(board)
        if not pairs:
            rule = 'unique pair'
            pairs = find_unique_pairs(board)
        if not pairs:
            unjoined_cells = list(find_unjoined_cells(board))
            is_solved = not unjoined_cells
            if is_solved:
                if verbose:
                    print('Solved!')
                return {board.display()}
            break
        join_pairs(board, pairs)
        if verbose:
            print(rule)
            print(board.display())
        check_for_duplicates(board)
    solutions = set()
    pairs = list(chain(*(location_list
                         for location_list in find_pair_locations(board).values()
                         if location_list is not None)))
    start_state = board.display()
    if not pairs:
        for _ in find_unjoined_cells(board):
            break
        else:
            # No unjoined cells, it's a solution!
            solutions.add(start_state)
    while pairs:
        board = Board.create(start_state)
        pair = pairs.pop()
        join_pair(board, *pair)
        if verbose:
            print('pick level', depth)
            if depth <= 3:
                print(start_state)
                new_state = board.display()
                print('pick ->')
                print(new_state)
        check_for_duplicates(board)
        solutions.update(find_solutions(board, depth+1, verbose, max_solutions))
        if max_solutions is not None and len(solutions) > max_solutions:
            return solutions

    return solutions


def main1():
    while True:
        board = Board(4, 3, max_pips=2)
        board.fill(random)
        board.split_all()
        solutions = find_solutions(board, verbose=False, max_solutions=1)
        if len(solutions) == 1:
            break
        else:
            print(f'Found multiple solutions.')
    print(f'Find the solution.')
    board.split_all()
    print(board.display())


def main():
    level_weights = dict(tricky={1: 1,  # single neighbour
                                 2: 0,  # newly joined
                                 3: 3,  # newly split
                                 4: 3,  # duplicate neighbours
                                 5: 1,  # shared spaces
                                 6: 10},  # unique pairs
                         hard={1: 1,
                               2: 0,
                               3: 3,
                               4: 1,
                               6: 10},
                         medium={1: 1,
                                 2: 0,
                                 3: 3,
                                 6: 10},
                         easy={1: 1,
                               2: 0,
                               6: 10})
    move_weights = level_weights['tricky']
    # 18 -24 -24 '0 1 0 2 0 3\n\n3 3 1 4 2 4\n\n1 1 0 0 1 3\n\n2 0 4 2 2 4\n           \n1 2 3 4 4 3\n'
    max_pips = 6
    init_params = dict(max_pips=max_pips, width=max_pips+2, height=max_pips+1)
    evo = Evolution(
        pool_size=100,
        fitness=partial(calculate_fitness, move_weights=move_weights),
        individual_class=DominosaProblem,
        n_offsprings=30,
        pair_params=None,
        mutate_params=None,
        init_params=init_params)
    n_epochs = 1000

    hist = []
    for i in range(n_epochs):
        top_individual = evo.pool.individuals[-1]
        top_fitness = evo.pool.fitness(top_individual)
        mid_fitness = evo.pool.fitness(evo.pool.individuals[-len(evo.pool.individuals)//5])
        print(i, top_fitness, mid_fitness, repr(strip_solution(top_individual.value['solution'])))
        hist.append(top_fitness)
        evo.step()

    best = evo.pool.individuals[-1]
    for problem in evo.pool.individuals:
        print(evo.pool.fitness(problem))
    # plt.plot(hist)
    # plt.show()
    solution = best.value['solution']
    print(strip_solution(solution))


def strip_solution(solution):
    return solution.replace('|', ' ').replace('-', ' ')


if __name__ == '__main__':
    main()
