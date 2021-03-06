from bees import BeesBoard, BeesGraph


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
dice:(2,0)2,(0,1)1
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 1|2

2|3 2|0
---
dice:(2,0)2,(2,1)1
"""
    expected_moves = [('1R2', expected_display)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_move_vertical():
    start_state = """\
1|0 2|2

1|3 2|0
---
dice:(2,0)2,(0,1)1
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 2|2

1|3 2|0
---
dice:(2,0)2,(0,0)1
"""
    expected_moves = [('1D1', expected_display)]
    graph = BeesGraph()

    moves = list(graph.generate_moves(board))

    assert moves == expected_moves
    assert board.display() == start_state


def test_move_to_wild():
    start_state = """\
1|0 2|0

3|3 2|1
---
dice:(2,1)2,(0,1)1
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 2|0

3|3 2|1
---
dice:(2,1)2,(3,1)1
"""
    expected_moves = [('1R3', expected_display)]
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
dice:(2,1)3,(3,1)2,(3,2)1
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 3|1

0|0 3|0

2|0 3|3
---
dice:(2,1)3,(3,1)2,(0,2)1
"""
    expected_moves = [('1L3', expected_display)]
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
dice:(0,0)2,(2,1)3,(0,2)1
"""
    board = BeesBoard.create(start_state, max_pips=3)
    expected_display = """\
1|0 3|3

3|2 3|0

2|0 3|1
---
dice:(0,0)2,(2,1)3,(3,0)1
"""
    expected_moves = [('1D2R3', expected_display)]
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
    graph = BeesGraph()

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
dice:(0,0)3,(0,2)1,(2,1)2
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
