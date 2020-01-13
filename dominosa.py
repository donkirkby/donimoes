import typing
from collections import defaultdict

from domino_puzzle import Board, Cell, Domino


def place_unique_pairs(board: Board):
    pairs = find_unique_pairs(board)
    join_pairs(board, pairs)
    return len(pairs)


def join_pairs(board: Board, pairs: typing.List[typing.Tuple[int]]):
    for pair in pairs:
        join_pair(board, *pair)


def find_unique_pairs(board: Board) -> typing.List[typing.Tuple[int]]:
    pair_locations = defaultdict(list)
    for x in range(board.width):
        for y in range(board.height):
            cell = board[x][y]
            if 0 < x:
                record_pair(board[x - 1][y], cell, pair_locations)
            if 0 < y:
                record_pair(board[x][y - 1], cell, pair_locations)

    return [location_list[0]
            for location_list in pair_locations.values()
            if location_list is not None and len(location_list) == 1]


def join_pair(board: Board, x1: int, y1: int, x2: int, y2: int):
    pips1 = board[x1][y1].pips
    pips2 = board[x2][y2].pips
    domino = Domino(pips1, pips2)
    if x1 == x2:
        domino.rotate(90)
    board[x1][y1] = domino.head
    board[x2][y2] = domino.tail


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
    pairs = set()
    for x in range(board.width):
        for y in range(board.height):
            cell = board[x][y]
            if cell.domino is not None:
                continue
            neighbours = []
            for dx, dy in Domino.directions:
                x2 = x+dx
                y2 = y+dy
                if 0 <= x2 < board.width and 0 <= y2 < board.height:
                    cell2 = board[x2][y2]
                    if cell2.domino is None:
                        neighbours.append(sorted(((x, y), (x2, y2))))
            if len(neighbours) == 1:
                (x1, y1), (x2, y2) = neighbours[0]
                pairs.add((x1, y1, x2, y2))
    # noinspection PyTypeChecker
    return sorted(pairs)


def main():
    board = Board.create('''\
2 2 2 0

0 0 2 1

1 1 0 1
''')
    while True:
        rule = 'one neighbour'
        pairs = find_one_neighbour_pairs(board)
        if not pairs:
            rule = 'unique pair'
            pairs = find_unique_pairs(board)
        if not pairs:
            break
        join_pairs(board, pairs)
        print(rule)
        print(board.display())


if __name__ == '__main__':
    main()
