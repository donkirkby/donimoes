import random
import typing
from collections import defaultdict, Counter
from enum import Enum
from itertools import chain

from domino_puzzle import Board, Cell, Domino, BoardGraph


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
    def __init__(self, width, height, max_pips=None):
        super().__init__(width, height, max_pips)
        self.pair_states = {}

    def get_pair_state(self, x1: int, y1: int, x2: int, y2: int):
        if x2 < x1 or y2 < y1:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        return self.pair_states[(x1, y1, x2, y2)]

    def add_joint(self, joint: str, x1: int, y1: int, x2: int, y2: int) -> str:
        pair_state = PairState.state_codes[joint]
        self.pair_states[(x1, y1, x2, y2)] = pair_state
        if pair_state in (PairState.SPLIT, PairState.NEWLY_SPLIT):
            return ' '
        if pair_state == PairState.NEWLY_JOINED:
            if x1 != x2:
                return '|'
            return '-'
        return joint

    def adjust_display(self, display: typing.List[typing.List[str]]):
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


class DominosaGraph(BoardGraph):
    def generate_moves(self, board):
        pass


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


def main():
    while True:
        board = Board(6, 5, max_pips=4)
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


if __name__ == '__main__':
    main()
