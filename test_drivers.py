from drivers import DriversBoard, DriversGraph
from domino_puzzle import MoveDescription


def test_create_with_dice():
    start_state = """\
1|0 1|2

4|3 2|3
---
dice:(0,1)1,(2,1)2,(3,0)3,(0,0)4
"""
    board = DriversBoard.create(start_state, max_pips=4)

    final_state = board.display()

    assert final_state == start_state


def test_create_and_place_dice():
    start_state = """\
1|0 1|2

4|3 2|3
"""
    board = DriversBoard.create(start_state, max_pips=4)
    expected_display = """\
1|0 1|2

4|3 2|3
---
dice:(0,1)1,(3,1)2,(3,0)3,(0,0)4
"""

    final_state = board.display()

    assert final_state == expected_display


def test_create_with_duplicate():
    start_state = """\
1|0 2|1

4|3 2|3
"""
    board = DriversBoard.create(start_state, max_pips=4)
    expected_display = """\
1|0 2|1

4|3 2|3
---
dice:(0,1)1,(3,0)3,(0,0)4
"""

    final_state = board.display()

    assert final_state == expected_display


def test_create_with_blank():
    start_state = """\
1|0 2|0

4|3 2|3
"""
    board = DriversBoard.create(start_state, max_pips=4)
    expected_display = """\
1|0 2|0

4|3 2|3
---
dice:(0,1)1,(3,0)3,(0,0)4
"""

    final_state = board.display()

    assert final_state == expected_display


def test_move_unforced():
    start_state = """\
1|0 2 2
    - -
2|2 0 3
---
dice:(0,1)1,(3,1)2
"""
    board = DriversBoard.create(start_state, max_pips=3, border=1)
    expected_display1 = """\
1|0 2 2
    - -
2|2 0 3
---
dice:(1,1)1,(3,1)2
"""
    expected_display2 = """\
1|0 x 2 2
      - -
x 2|2 0 3
---
dice:(0,1)1,(4,1)2
"""
    expected_display3 = """\
1|0 2 2
    - -
2|2 0 3
---
dice:(0,1)1,(2,1)2
"""
    expected_display4 = """\
x x x 2
      -
1|0 2 3
    -
2|2 0 x
---
dice:(0,1)1,(3,2)2
"""
    expected_display5 = """\
1|0 2 x
    -
2|2 0 2
      -
x x x 3
---
dice:(0,2)1,(3,1)2
"""
    expected_moves = [MoveDescription('1R', expected_display1, remaining=1),
                      MoveDescription('1dL', expected_display2, remaining=2),
                      MoveDescription('2L', expected_display3, remaining=1),
                      MoveDescription('2dU', expected_display4, remaining=1),
                      MoveDescription('2dD', expected_display5, remaining=1)]
    graph = DriversGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display(cropped=True) == start_state


def test_move_forced():
    """ If a die is on a different number, it must move. """
    start_state = """\
1|0 2 2
    - -
2|2 0 3
---
dice:(1,1)1,(3,1)2
"""
    board = DriversBoard.create(start_state, max_pips=3, border=1)
    expected_display1 = """\
1|0 2 2
    - -
2|2 0 3
---
dice:(0,1)1,(3,1)2
"""
    expected_moves = [MoveDescription('1L', expected_display1, remaining=1)]
    graph = DriversGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display(cropped=True) == start_state


def test_move_two_dice():
    start_state = """\
1|2 3 0
    - -
3|3 0 2
---
dice:(0,1)1,(1,1)2
"""
    board = DriversBoard.create(start_state, max_pips=3, border=1)
    expected_display = """\
1|2 x 3 0
      - -
x 3|3 0 2
---
dice:(0,1)1,(1,1)2
"""
    expected_moves = [MoveDescription('1dL', expected_display, remaining=1)]
    graph = DriversGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display(cropped=True) == start_state


def test_move_stays_connected():
    """ If a die is on a different number, it must move. """
    start_state = """\
1|0 x 2 2
      - -
x 2|2 0 3
---
dice:(0,1)1
"""
    board = DriversBoard.create(start_state, max_pips=3, border=1)
    expected_display1 = """\
1|0 x 2 2
      - -
x 2|2 0 3
---
dice:(1,1)1
"""
    expected_display2 = """\
1|0 2 2
    - -
2|2 0 3
---
dice:(0,1)1
"""
    expected_moves = [MoveDescription('1R', expected_display1, remaining=2),
                      MoveDescription('1dR', expected_display2, remaining=1)]
    graph = DriversGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display(cropped=True) == start_state


def test_solution():
    start_state = """\
1|0 2 2
    - -
2|2 0 3
"""
    board = DriversBoard.create(start_state, max_pips=3)
    expected_solution = ['2L', '2dU']
    graph = DriversGraph(process_count=0)

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


# def test_solution_zero_length():
#     start_state = """\
# 0|0 1|2
#
# 0|1 1|3
#
# 0|2 2|2
#
# 0|3 2|3
#
# 1|1 3|3
# """
#     board = DriversBoard.create(start_state, max_pips=3)
#     expected_solution = []
#     graph = DriversGraph()
#
#     graph.walk(board)
#     solution = graph.get_solution()
#
#     assert solution == expected_solution
#
#
# def test_solution_uses_direct():
#     start_state = """\
# 4 3 0|3
# - -
# 0 1 0|2
#
# 0|1 0|0
# ---
# dice:(0,2)4,(0,1)2,(1,0)1,(1,2)3
# """
#     board = DriversBoard.create(start_state, max_pips=4)
#     expected_solution = ['1U1']
#     graph = DriversGraph()
#
#     graph.walk(board)
#     solution = graph.get_solution()
#
#     assert solution == expected_solution
#
#
# def test_place_dice():
#     start_state = """\
# 1|0 3|3
#
# 2|2 2|0
#
# 3|0 1|1
# ---
# dice:
# """
#     board = DriversBoard.create(start_state, max_pips=3)
#     expected_display0 = start_state
#     expected_display2 = """\
# 1|0 3|3
#
# 2|2 2|0
#
# 3|0 1|1
# ---
# dice:(0,2)1,(2,1)2
# """
#     expected_display3 = """\
# 1|0 3|3
#
# 2|2 2|0
#
# 3|0 1|1
# ---
# dice:(0,2)1,(2,1)2,(0,0)3
# """
#
#     display0 = board.display()
#     queen_pips0 = board.queen_pips
#     board.place_dice(2)
#     display2 = board.display()
#     queen_pips2 = board.queen_pips
#     board.place_dice()
#     display3 = board.display()
#     queen_pips3 = board.queen_pips
#
#     assert display0 == expected_display0
#     assert queen_pips0 == 0
#     assert display2 == expected_display2
#     assert queen_pips2 == 2
#     assert display3 == expected_display3
#     assert queen_pips3 == 3
#
#
# def test_check_progress_min_gaps():
#     start_state = """\
# 1|0 2|2
#
# 1|3 2|0
# """
#     expected_gap = 2
#     board = DriversBoard.create(start_state, max_pips=3)
#     graph = DriversGraph()
#
#     gap = graph.check_progress(board)
#
#     assert gap == expected_gap
#
#
# def test_check_progress_win():
#     start_state = """\
# 3|5 5|5 4|4 2
#             -
# 0|1 4|3 2|2 0
#
# 1|2 3 2|5 5 4
#     -     - -
# 1|3 0 2|4 4 1
#
# 1|1 3|3 0|4 0
#             -
# 2|3 0|5 1|5 0
# ---
# dice:(2,3)3,(3,2)2,(2,2)1
# """
#     expected_gap = 0
#     board = DriversBoard.create(start_state, max_pips=5)
#     graph = DriversGraph()
#
#     gap = graph.check_progress(board)
#
#     assert gap == expected_gap
#
#
# def test_has_touching_blanks():
#     start_state = """\
# 1|0 2|2
#
# 0|2 1|3
# """
#     board = DriversBoard.create(start_state, max_pips=3)
#
#     assert board.has_touching_blanks
