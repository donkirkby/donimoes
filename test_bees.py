from bees import BeesBoard, BeesGraph
from domino_puzzle import MoveDescription


def test_create_with_dice():
    start_state = """\
1|0 1|2

2|3 2|0
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 1|2

2|3 2|0
---
dice:(0,1)1,(2,0)2
"""

    final_state = board.display()
    queen_pips = board.queen_pips

    assert final_state == expected_display
    assert queen_pips == 2


def test_move_horizontal():
    start_state = """\
1|0 1|2

2|3 2|0
---
dice:(0,1)1,(2,0)2
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 1|2

2|3 2|0
---
dice:(2,1)1,(2,0)2
"""
    expected_moves = [MoveDescription('1R2', expected_display)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_move_vertical():
    start_state = """\
1|0 2|2

1|3 2|0
---
dice:(0,1)1,(2,0)2
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 2|2

1|3 2|0
---
dice:(0,0)1,(2,0)2
"""
    expected_moves = [MoveDescription('1D1', expected_display, remaining=1)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_move_to_wild():
    start_state = """\
1|0 2|0

3|3 2|1
---
dice:(0,1)1,(2,1)2
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 2|0

3|3 2|1
---
dice:(3,1)1,(2,1)2
"""
    expected_moves = [MoveDescription('1R3', expected_display)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_wild_occupied():
    """ The 1 die can't move onto the wild space, because it's occupied. """
    start_state = """\
1|0 3|1

0|0 3|0

2|0 3|3
---
dice:(3,2)1,(3,1)2,(2,1)3
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 3|1

0|0 3|0

2|0 3|3
---
dice:(0,2)1,(3,1)2,(2,1)3
"""
    expected_moves = [MoveDescription('1L3', expected_display, remaining=2)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_turn_on_die():
    start_state = """\
1|0 3|3

3|2 3|0

2|0 3|1
---
dice:(0,2)1,(0,0)2,(2,1)3
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 3|3

3|2 3|0

2|0 3|1
---
dice:(3,0)1,(0,0)2,(2,1)3
"""
    expected_moves = [MoveDescription('1D2R3', expected_display, remaining=3)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_solution():
    start_state = """\
1|0 1|2

3|1 3|3

2|3 2|0
---
dice:(2,0)2,(0,2)1
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_solution = ['1R2', '1D2R1']
    graph = BeesGraph(process_count=2)

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_solution_uses_direct():
    start_state = """\
4 3 0|3
- -
0 1 0|2

0|1 0|0
---
dice:(0,2)4,(0,1)2,(1,0)1,(1,2)3
"""
    board = BeesBoard.create(start_state, max_pips=4)
    expected_solution = ['1U1']
    graph = BeesGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_place_dice():
    start_state = """\
1|0 3|3

2|2 2|0

3|0 1|1
---
dice:
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display0 = start_state
    expected_display2 = """\
1|0 3|3

2|2 2|0

3|0 1|1
---
dice:(0,2)1,(2,1)2
"""
    expected_display3 = """\
1|0 3|3

2|2 2|0

3|0 1|1
---
dice:(0,2)1,(2,1)2,(0,0)3
"""

    display0 = board.display()
    queen_pips0 = board.queen_pips
    board.place_dice(2)
    display2 = board.display()
    queen_pips2 = board.queen_pips
    board.place_dice()
    display3 = board.display()
    queen_pips3 = board.queen_pips

    assert display0 == expected_display0
    assert queen_pips0 == 0
    assert display2 == expected_display2
    assert queen_pips2 == 2
    assert display3 == expected_display3
    assert queen_pips3 == 3


def test_check_progress_min_gaps():
    start_state = """\
1|0 2|2

1|3 2|0
"""
    expected_gap = 2
    board = BeesBoard.create(start_state, max_pips=3)
    graph = BeesGraph()

    gap = graph.check_progress(board)

    assert gap == expected_gap


def test_check_progress_win():
    start_state = """\
3|5 5|5 4|4 2
            -
0|1 4|3 2|2 0

1|2 3 2|5 5 4
    -     - -
1|3 0 2|4 4 1

1|1 3|3 0|4 0
            -
2|3 0|5 1|5 0
---
dice:(2,3)3,(3,2)2,(2,2)1
"""
    expected_gap = 0
    board = BeesBoard.create(start_state, max_pips=5)
    graph = BeesGraph()

    gap = graph.check_progress(board)

    assert gap == expected_gap
