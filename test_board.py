from random import Random
from unittest.mock import patch

import pytest

from domino_puzzle import Board, Cell, Domino, BoardError
from test_domino_puzzle import DummyRandom


def test_repr():
    board = Board(4, 3)

    s = repr(board)

    assert s == "Board(4, 3)"


def test_add_cell():
    board = Board(4, 3)

    board.add(Cell(4), 1, 2)
    cell = board[1][2]

    assert cell.pips == 4


def test_add_domino():
    board = Board(4, 3)
    board.add(Domino(5, 6), 1, 2)

    pips = board[1][2].pips

    assert pips == 5


def test_display():
    board = Board(4, 3)
    board.add(Domino(5, 6), 1, 2)
    expected_display = """\
x 5|6 x

x x x x

x x x x
"""

    display = board.display()

    assert display == expected_display


def test_display_cropped():
    board = Board.create("""\
3 x x x
-
2 0|2 x

x x x x
""")
    expected_display = """\
3 x x
-
2 0|2
"""

    assert board.display(cropped=True) == expected_display


def test_display_cropping_bounds():
    board = Board.create("""\
3 x x x
-
2 0|2 x

x x x x
""")
    expected_display = """\
3 x x
-
2 0|2
"""
    bounds = ['garbage', 'to', 'be', 'removed']
    expected_bounds = [0, 1, 2, 2]

    display = board.display(cropped=True, cropping_bounds=bounds)

    assert display == expected_display
    assert bounds == expected_bounds


def test_create_with_spaces():
    board = Board.create("""\
            4
            -
3|1   4|6 4 1
          -
  2 4     4 2|5
  - -
  3 2   4|0 5
            -
  5 0|0 1|1 4
  -
  6 5|5 3|3 6|3
""")
    expected_display = """\
x x x x x x 4 x
            -
3|1 x 4|6 4 1 x
          -
x 2 4 x x 4 2|5
  - -
x 3 2 x 4|0 5 x
            -
x 5 0|0 1|1 4 x
  -
x 6 5|5 3|3 6|3
"""

    display = board.display()

    assert display == expected_display


def test_rotate():
    board = Board(4, 3)
    domino1 = Domino(5, 6)
    board.add(domino1, 1, 2)
    domino1.rotate(-90)
    expected_display = """\
x 5 x x
  -
x 6 x x

x x x x
"""

    display = board.display()

    assert display == expected_display


def test_move_right():
    board = Board(4, 3)
    domino1 = Domino(5, 6)
    board.add(domino1, 1, 2)
    domino1.move(1, 0)
    expected_display = """\
x x 5|6

x x x x

x x x x
"""

    display = board.display()

    assert display == expected_display


def test_move_left():
    board = Board(4, 3)
    domino1 = Domino(5, 6)
    board.add(domino1, 1, 2)
    domino1.move(-1, 0)
    expected_display = """\
5|6 x x

x x x x

x x x x
"""

    display = board.display()

    assert display == expected_display


def test_get_direction():
    dx, dy = Domino.get_direction('l')

    assert (dx, dy) == (-1, 0)


def test_rotate_without_board():
    domino1 = Domino(5, 6)
    domino1.rotate(90)

    assert domino1.degrees == 90


def test_remove():
    board = Board(3, 4)
    domino1 = Domino(1, 5)
    board.add(domino1, 0, 0)

    board.remove(domino1)

    assert board.dominoes == []


def test_remove_and_rotate():
    board = Board(3, 4)
    domino1 = Domino(1, 5)
    board.add(domino1, 0, 0)

    board.remove(domino1)
    domino1.rotate(270)

    assert domino1.degrees == 270


def test_rotate_and_add():
    board = Board(4, 3)
    domino1 = Domino(5, 6)
    domino1.rotate(-90)
    board.add(domino1, 1, 2)
    expected_display = """\
x 5 x x
  -
x 6 x x

x x x x
"""

    display = board.display()

    assert display == expected_display


def test_occupied():
    board = Board(4, 3)
    board.add(Domino(2, 3), 1, 0)

    with pytest.raises(BoardError, match='Position 1, 0 is occupied.'):
        board.add(Domino(1, 2), 0, 0)


def test_off_board():
    board = Board(4, 3)

    with pytest.raises(BoardError, match='Position 4, 0 is off the board.'):
        board.add(Domino(1, 2), 3, 0)


def test_bad_move():
    start_state = """\
0|2 x

0|1 x
"""
    board = Board.create(start_state)
    domino1 = board[0][0].domino

    with pytest.raises(BoardError):
        domino1.move(-1, 0)

    assert board.display() == start_state


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill(mock_choose):
    mock_choose.side_effect = [[Domino(0, 0)],
                               [Domino(0, 1)]]
    dummy_random = DummyRandom(randints={(0, 3): [1, 1]})  # directions
    board = Board(2, 2, max_pips=6)
    expected_display = """\
0 1
- -
0 0
"""

    board.fill(dummy_random)
    display = board.display()

    assert display == expected_display


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill_with_random_domino(mock_choose):
    mock_choose.side_effect = [[Domino(0, 5)],
                               [Domino(0, 2)]]
    dummy_random = DummyRandom(randints={(0, 3): [1, 1]})  # directions
    board = Board(2, 2, max_pips=6)
    expected_display = """\
5 2
- -
0 0
"""

    board.fill(dummy_random)
    display = board.display()

    assert display == expected_display


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill_with_no_matches_flip(mock_choose):
    mock_choose.side_effect = [[Domino(0, 5)],
                               [Domino(0, 2)]]
    dummy_random = DummyRandom(randints={(0, 3): [1, 1],  # directions
                                         (0, 1): [0, 0]})
    board = Board(2, 2, max_pips=6)
    expected_display = """\
5 0
- -
0 2
"""

    board.fill(dummy_random, matches_allowed=False)
    display = board.display()

    assert display == expected_display


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill_with_no_matches_next(mock_choose):
    mock_choose.side_effect = [[Domino(0, 5)],
                               [Domino(0, 0), Domino(0, 1)]]
    dummy_random = DummyRandom(randints={(0, 3): [1, 1]})  # directions
    board = Board(2, 2, max_pips=6)
    expected_display = """\
5 0
- -
0 1
"""

    board.fill(dummy_random, matches_allowed=False)
    display = board.display()

    assert display == expected_display


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill_with_flip(mock_choose):
    mock_choose.side_effect = [[Domino(0, 0)],
                               [Domino(0, 1)]]
    dummy_random = DummyRandom(randints={(0, 3): [1, 1],   # directions
                                         (0, 1): [1, 1]})  # flips
    board = Board(2, 2, max_pips=6)
    expected_display = """\
0 0
- -
0 1
"""

    board.fill(dummy_random)
    display = board.display()

    assert display == expected_display


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill_with_more_rotation(mock_choose):
    mock_choose.side_effect = [[Domino(0, 0)],
                               [Domino(0, 1)],
                               [Domino(0, 2)],
                               [Domino(0, 2)],
                               [Domino(0, 2)],
                               [Domino(0, 2)]]
    dummy_random = DummyRandom(randints={(0, 3): [1, 1, 1]})  # directions
    board = Board(2, 3, max_pips=6)
    expected_display = """\
0|2

0 1
- -
0 0
"""

    board.fill(dummy_random)
    display = board.display()

    assert display == expected_display


@patch('domino_puzzle.Board.choose_extra_dominoes')
def test_fill_with_backtrack(mock_choose):
    """ Force a backtrack.

    This scenario will get to the following grid and then be forced to
    backtrack, because the gaps are size 1 and 3: odd.
    x 3 x x
      -
    0 0 x 2
    -     -
    0 0|1 0
    """
    mock_choose.side_effect = [[Domino(0, 0)],
                               [Domino(0, 1)],
                               [Domino(0, 2)],
                               [Domino(0, 3)],
                               [Domino(0, 3)],
                               [Domino(0, 3)],
                               [Domino(0, 3)],
                               [Domino(0, 4)],
                               [Domino(0, 5)]]
    dummy_random = DummyRandom(
        randints={(0, 3): [1, 0, 1, 1]})  # directions
    board = Board(4, 3, max_pips=6)
    expected_display = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""

    board.fill(dummy_random)
    display = board.display()

    assert display == expected_display


def test_fill_fail_for_matching():
    """ Fail because all of the remaining dominoes have matches.
    """
    random = Random()
    start = """\
0 x x
-
0 1|1
"""
    board = Board.create(start, max_pips=1)

    result = board.fill(random, matches_allowed=False)

    assert not result
    assert board.display() == start


def test_fill_fail_for_bad_fit():
    """ Fail because a domino won't fit in the hole.

    Don't bother trying other dominoes.
    """
    random = Random()
    start = """\
x 3 4 x
  - -
0 1 0 2
-     -
5 0|1 0
"""
    board = Board.create(start, max_pips=6)

    result = board.fill(random, matches_allowed=False)

    assert not result
    assert board.display() == start


def test_extra_dominoes():
    state = """\
0|0 x

1|1 x
"""
    max_pips = 2
    expected_extra_dominoes = [Domino(0, 1),
                               Domino(0, 2),
                               Domino(1, 2),
                               Domino(2, 2)]

    board = Board.create(state, max_pips=max_pips)

    assert board.extra_dominoes == expected_extra_dominoes


def test_flip():
    board = Board(3, 2, max_pips=6)
    domino1 = Domino(1, 5)
    expected_display = """\
x x x

5|1 x
"""

    board.add(domino1, 0, 0)
    domino1.flip()

    assert board.display() == expected_display


def test_create():
    state = """\
0|2 x

0|1 x
"""

    board = Board.create(state)
    display = board.display()

    assert display == state


def test_create_right_edge():
    state = """\
x 0|2

0|1 x
"""

    board = Board.create(state)

    assert board.display() == state


def test_create_vertical():
    state = """\
1 0|2
-
0 x x
"""

    board = Board.create(state)

    assert board.display() == state


def test_create_with_other_markers():
    state = """\
1 0?2
*
0 x x
"""
    expected_display = """\
1 0|2
-
0 x x
"""

    board = Board.create(state)

    assert board.display() == expected_display


def test_create_with_border():
    state = """\
3 x x
-
2 0|2
"""
    board = Board.create(state, border=1)
    expected_display = """\
x x x x x

x 3 x x x
  -
x 2 0|2 x

x x x x x
"""

    assert board.display() == expected_display


def test_is_connected():
    state = """\
1 0|2 x x
-
0 0|4 0|3
"""
    board = Board.create(state)

    assert board.is_connected()


def test_is_not_connected():
    state = """\
1 0|2 x x
-
0 x x 0|3
"""
    board = Board.create(state)

    assert not board.is_connected()


def test_has_no_loner():
    state = """\
1 0 x 1|3
- -
0 2 x 0|3
"""
    board = Board.create(state)

    assert not board.hasLoner()


def test_has_loner():
    state = """\
1 0 x 1|2
- -
0 2 x 0|3
"""
    board = Board.create(state)

    assert board.hasLoner()


def test_has_no_match():
    state = """\
1 0
- -
0 2
"""
    board = Board.create(state)

    assert not board.hasMatch()


def test_has_match():
    state = """\
1 2
- -
0 0
"""
    board = Board.create(state)

    assert board.hasMatch()


def test_find_no_match():
    state = """\
1 0
- -
0 2
"""
    board = Board.create(state)
    matches = board.findMatches()
    expected_matches = []

    assert matches == expected_matches


def test_find_match():
    state = """\
1 2
- -
0 0
"""
    board = Board.create(state)
    matches = board.findMatches()
    coordinates = [(cell.x, cell.y) for cell in matches]
    expected_coordinates = [(0, 0), (1, 0)]

    assert coordinates == expected_coordinates


def test_has_even_gaps_no_gaps():
    state = """\
4|5 6 0
    - -
1 2 1 5
- -
0 3 2|4
"""
    board = Board.create(state)
    has_even_gaps = board.hasEvenGaps()

    assert has_even_gaps


def test_has_even_gaps_two_uneven_gaps():
    state = """\
4|5 x 0
      -
1 2 6 5
- - -
0 3 1 x
"""
    board = Board.create(state)
    has_even_gaps = board.hasEvenGaps()

    assert not has_even_gaps


def test_has_even_gaps_one_even_gap():
    state = """\
4|5 6 0
    - -
1 2 1 5
- -
0 3 x x
"""
    board = Board.create(state)
    has_even_gaps = board.hasEvenGaps()

    assert has_even_gaps


def test_equal():
    state = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
    board1 = Board.create(state)
    board2 = Board.create(state)

    eq_result = (board1 == board2)
    neq_result = (board1 != board2)
    assert eq_result
    assert not neq_result


def test_equal_with_gap():
    state = """\
0|4 0|5

0 x x 2
-     -
0 0|1 0
"""
    board1 = Board.create(state)
    board2 = Board.create(state)

    eq_result = (board1 == board2)
    neq_result = (board1 != board2)
    assert eq_result
    assert not neq_result


def test_different_gap():
    state1 = """\
0|4 0|5

0 x x 2
-     -
0 0|1 0
"""
    state2 = """\
0|4 0|5

0 x 0 2
-   - -
0 x 1 0
"""
    board1 = Board.create(state1)
    board2 = Board.create(state2)

    eq_result = (board1 == board2)
    neq_result = (board1 != board2)
    assert not eq_result
    assert neq_result


def test_different_pips():
    state1 = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
    state2 = """\
6|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
    board1 = Board.create(state1)
    board2 = Board.create(state2)

    eq_result = (board1 == board2)
    neq_result = (board1 != board2)
    assert not eq_result
    assert neq_result


def test_different_alignment():
    state1 = """\
0|4 0|5

0 0|3 2
-     -
0 0|1 0
"""
    state2 = """\
0|4 0|5

0 0 3 2
- - - -
0 0 1 0
"""
    board1 = Board.create(state1)
    board2 = Board.create(state2)

    assert board1 != board2


def test_parse_cells_and_dominoes():
    state = """\
0 1
-
2 3
"""
    board = Board.create(state)

    assert isinstance(board[0][1].domino, Domino)
    assert board[1][0].domino is None


def test_display_cells_and_dominoes():
    state = """\
0 1
-
2 3
"""
    board = Board.create(state)
    display = board.display()

    assert display == state


def test_join_cells_right():
    state = """\
0 1 1
-
2 3 2
"""
    expected_state = """\
0 1|1
-
2 3 2
"""
    board = Board.create(state)
    cell1 = board[1][1]
    cell2 = board[2][1]

    board.join(cell1, cell2)

    display = board.display()

    assert display == expected_state
    assert cell1.domino.degrees == 0
    assert len(board.dominoes) == 2


def test_join_cells_up():
    state = """\
0 1 1
-
2 3 2
"""
    expected_state = """\
0 1 1
- -
2 3 2
"""
    board = Board.create(state)
    cell1 = board[1][0]
    cell2 = board[1][1]

    board.join(cell1, cell2)

    display = board.display()

    assert display == expected_state
    assert cell1.domino.degrees == 90


def test_join_cells_left():
    state = """\
0 1 1
-
2 3 2
"""
    expected_state = """\
0 1|1
-
2 3 2
"""
    board = Board.create(state)
    cell1 = board[2][1]
    cell2 = board[1][1]

    board.join(cell1, cell2)

    display = board.display()

    assert display == expected_state
    assert cell1.domino.degrees == 180


def test_join_cells_down():
    state = """\
0 1 1
-
2 3 2
"""
    expected_state = """\
0 1 1
- -
2 3 2
"""
    board = Board.create(state)
    cell1 = board[1][1]
    cell2 = board[1][0]

    board.join(cell1, cell2)

    display = board.display()

    assert display == expected_state
    assert cell1.domino.degrees == 270


def test_join_cells_not_neighbours():
    state = """\
0 1 1
-
2 3 2
"""
    board = Board.create(state)
    cell1 = board[2][1]
    cell2 = board[1][0]

    with pytest.raises(ValueError,
                       match=r"Cells are not neighbours: 2,1 and 1,0."):
        board.join(cell1, cell2)


def test_join_cells_not_available():
    state = """\
0 1 1
-
2 3 2
"""
    board = Board.create(state)
    cell1 = board[0][0]
    cell2 = board[1][0]

    with pytest.raises(ValueError, match=r"Cell is not available: 0,0."):
        board.join(cell1, cell2)


def test_split_domino():
    state = """\
0 1|1
-
2 3 2
"""
    expected_display = """\
0 1|1

2 3 2
"""
    board = Board.create(state)
    domino = board[0][0].domino

    board.split(domino)

    display = board.display()
    assert display == expected_display
    assert board.dominoes == [Domino(1, 1)]


def test_split_all():
    state = """\
0 1|1
-
2 3 2
"""
    expected_display = """\
0 1 1

2 3 2
"""
    board = Board.create(state)

    board.split_all()

    display = board.display()
    assert display == expected_display
    assert board.dominoes == []


def test_markers():
    start_state = '''\
P|1 2 N
    - -
4|R 6 0
---
R5P0N3
'''
    expected_markers = {(1, 0): 'R', (0, 1): 'P', (3, 1): 'N'}

    board = Board.create(start_state)

    assert board.markers == expected_markers
    assert board.display() == start_state


def test_markers_off_board():
    start_state = '''\
R x x x

0|1 2 N
    - -
4|P 6 0
---
P5N3Rx
'''
    expected_markers = {(1, 0): 'P', (3, 1): 'N', (0, 2): 'R'}

    board = Board.create(start_state)

    assert board.markers == expected_markers
    assert board.display() == start_state


def test_markers_border():
    start_state = '''\
P|1 2 N
    - -
4|R 6 0
---
R5P0N3
'''

    board = Board.create(start_state, border=1)

    assert board.display(cropped=True) == start_state


def test_markers_off_board_cropped():
    start_state = '''\
R x x x

0|1 2 N
    - -
4|P 6 0
---
P5N3Rx
'''
    board = Board.create(start_state, border=1)

    assert board.display(cropped=True) == start_state


def test_markers_not_connected():
    start_state = '''\
0|R 2 N
    - -
4|P 6 0
---
P5R1N3
'''
    board = Board.create(start_state, border=1)

    assert not board.are_markers_connected


def test_markers_are_connected():
    start_state = '''\
0|R N 3
    - -
4|P 6 0
---
P5R1N2
'''
    board = Board.create(start_state, border=1)

    assert board.are_markers_connected
