import re

from domino_puzzle import Board
from mirror import add_start_markers, MirrorGraph


def main():
    start_state = """\
1 0 2
- - -
1 2 1
"""
    solution = """\
RDD, BL, RDU
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


main()

"""
19. 
20. NU, NR, NR, NR, NR, NR, NR, RL, RL, RL, RL, RL, RL, RL, RU, RR, RR, RR, RR,
    NDR, RDR, NL, RDL, RL, RL, NDR, RDR, NL, NL, RDL, RL, RL, NDR, RDR, RD, RR,
    RR, RR, RR, RR, NL, NL, NL, ND, NR, NR, NR, RDR, RDR, NDR, NDR, RL, NDL,
    NDL, NL, NL, RDR, RDR, NDR, NDR, NDR, RL, NDL, NDL, NL, NL, RDR, RDR, NDR,
    NDR, RL, RL, NDL, NDL, NL, NL, RDR, RDR, NDR, NDR, RL, RL, NDL, NU, NR, NR,
    NR, NR, NR, NR, RL, RU, RR, RR, RR, RR, NDR, NDR, RDR, RDR, NL, RDL, RDL,
    RL, RL, NDR, NDR, RDR, RDR, NL, NL, RDL, RDL, RL, RL, NDR, NDR, RDR, RD,
    RDR, RL, RU, RDR, RD, RR, RR, RR, RR, RR, NL, NL, NL, ND, NR, NR, NR, RDR,
    RDR, NDR, NDR, RL, NDL, NDL, NL, NL, RDR, RDR, NDL, NDL, RL, RL, NDL, NDL,
    NL, NL, RDR, RDR, NDR, NDR, RL, RL, NDL, NU, NR, NR, NR, NR, NR, NR, RL, RU,
    RR, RR, RR, RR, NDR, NDR, RDR, RDR, NL, RDL, RDL, RL, RL, NDR, NDR, RDR,
    RDR, NL, NL, RDL, RDL, RL, RL, NDR, NDR, RDR, RD, RDR, RL, RU, RDR, RD, RR,
    RR, RR, RR, RR, NL, NL, NL, ND, NR, NR, NR, RDR, NDR, RL, NDL, NL, NL, RDR,
    NDR, RL, RL, NDL, NL, NL, RDR, NDR, NU, NR, NR, NR, NR, NR, NR, RL, RL, RL,
    RU, RR, RR, RR, RR, NDR, RDR, NL, RDL, RL, RL, NDR, RDR, NL, NL, RDL, RL,
    RL, NDR, RDR, RD, RR, RR, RR, RR, RR, NL, NL, NL, ND, NR, NR, NR, RDR, NDR,
    RL, NDL, NL, NL, RDR, NDR, RL, RL, NDL, NL, NL, RDR, NDR, NU, NR, NR, NR,
    NR, NR, NR, RL, RL, RL, RU, RR, RR, RR, RR, NDR, RDR, NL, RDL, RL, RL, NDR,
    RDR, NL, NL, RDL, RL, RL, NDR, RDR, RU, RL, RL, RL, RL, RL, RU, RU, NL, NL,
    NL, NU, NL, NL, NL, NL, NL, NU, NU, RDU, NDU, NR, ND, RD, RR, RDU, RDU, NDU,
    NDU, NL, ND, RD, RL, RDU, RDU, NDU, NDU, PR, PR, PDD, PDD, PDD, RDD, RDD,
    RDD, PD, PR, PR, PR, PU, PR, PR, PU, PL, ND, ND, NR, NR, NR, NU, NR, NR, NU,
    PDR, PU, NL, RD, RD, RD, RL, RL, RL, RU, RR, RR!
"""