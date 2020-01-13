from collections import defaultdict

from domino_puzzle import Board, Cell, Domino


def place_unique_pairs(board: Board):
    pair_locations = defaultdict(list)
    for x in range(board.width):
        for y in range(board.height):
            cell = board[x][y]
            if 0 < x:
                record_pair(board[x - 1][y], cell, pair_locations)
            if 0 < y:
                record_pair(board[x][y - 1], cell, pair_locations)
    for values, location_list in pair_locations.items():
        location_count = len(location_list)
        if location_count == 1:
            x1, y1, x2, y2 = location_list[0]
            pips1 = board[x1][y1].pips
            pips2 = board[x2][y2].pips
            domino = Domino(pips1, pips2)
            if x1 == x2:
                domino.rotate(90)
            board[x1][y1] = domino.head
            board[x2][y2] = domino.tail


def record_pair(cell1: Cell, cell2: Cell, pair_locations: dict):
    if cell1.domino is not None or cell2.domino is not None:
        # Cell is already assigned to a domino, don't count it.
        return

    values = [cell1.pips, cell2.pips]
    values.sort()
    location = (cell1.x, cell1.y, cell2.x, cell2.y)
    location_list = pair_locations[tuple(values)]
    location_list.append(location)
