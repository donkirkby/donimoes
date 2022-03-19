from textwrap import dedent

from domino_puzzle import Board
from mountains import mountain_score


def test_simple():
    board = Board.create(dedent('''\
        0 1
        - -
        1 2'''))

    score = mountain_score(board)

    assert score == 0


def test_step():
    board = Board.create(dedent('''\
        0 0
        - -
        1 3'''))

    score = mountain_score(board)

    assert score == 2
