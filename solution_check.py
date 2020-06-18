import re

from domino_puzzle import Board
from mirror import add_start_markers, MirrorGraph, group_moves


def main():
    start_state = """\
1 0 2
- - -
1 2 1
"""
    solution = """\
RdD, BL, RdU
"""
    start_moves = re.split(r',\s*', solution.strip())
    moves = start_moves[:]
    graph = MirrorGraph()
    board = Board.create(start_state)
    add_start_markers(board)
    board = Board.create(board.display(), border=1)
    while moves:
        next_move = moves.pop(0)
        for move, state, move_attrs, heuristic in graph.generate_moves(board):
            if move == next_move:
                board = Board.create(state, border=1)
                break
        else:
            print(board.display(cropped=True))
            completed_moves = len(start_moves) - len(moves) - 1
            raise ValueError(f'Move {next_move} is not valid after '
                             f'{completed_moves} moves.')
    print(board.display(cropped=True))
    if not board.are_markers_connected:
        raise ValueError(f'Not solved after all {len(start_moves)} moves.')
    print(f'Solved after {len(start_moves)} moves.')
    print(group_moves(start_moves))


main()
