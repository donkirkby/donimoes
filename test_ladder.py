from ladder import LadderBoard, LadderMoveType, LadderGraph


def test_create():
    start_state = '''\
x x x x x x

x N|1 2 B x
      - -
x P|5 6 R x

x x x x x x
---
P4R0N0B3
---
M5
'''

    board = LadderBoard.create(start_state)

    assert board.display() == start_state
    assert board.target == 5
    assert board.move_type == LadderMoveType.MARKER


def test_generate_any_moves():
    start_state = '''\
x x x x x x

x 0|1 2 B x
      - -
x P|5 6 R x

x x x x x x
---
P4R0B3
---
A5
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('DPL', '''\
x 0|1 2 B
      - -
P|5 x 6 R
---
P4R0B3
---
M5
'''),
        ('DRU', '''\
x x x B
      -
0|1 2 R
    -
P|5 6 x
---
P4R0B3
---
M5
'''),
        ('DRD', '''\
0|1 2 x
    -
P|5 6 B
      -
x x x R
---
R0P4B3
---
M5
'''),
        ('MPR5', '''\
0|1 2 B
    - -
4|P 6 R
---
P5R0B3
---
A6
''')}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_generate_marker_moves():
    start_state = '''\
x x x x x x

x 0|1 2 B x
      - -
x P|5 6 R x

x x x x x x
---
P4R0B3
---
M5
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('MPR5', '''\
0|1 2 B
    - -
4|P 6 R
---
P5R0B3
---
A6
''')}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_board_stays_connected():
    start_state = '''\
x x x x x x x

x N|2 x x x x

x x 3|4 5|P x

x x x x x x x
---
P6N1
---
A1
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('DNR', '''\
N|2 x x

3|4 5|P
---
P6N1
---
M1
''')}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_walk():
    start_state = '''\
N 1|2 B
-     -
P 3|4 R
---
P0R5N0B3
---
M1
'''
    expected_solution = ['MNR1', 'DPU', 'MBL2', 'DRU', 'SOLVED']
    board = LadderBoard.create(start_state)
    graph = LadderGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_adds_markers():
    start_state = '''\
0 1|2 3
-     -
0 3|4 5
'''
    expected_solution = ['MNR1', 'DPU', 'MBL2', 'DRU', 'SOLVED']
    board = LadderBoard.create(start_state)
    graph = LadderGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_sets_smallest_area():
    start_state = '''\
6 1 0 3 0
- - - - -
6 2 0 4 6
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()

    graph.walk(board)

    assert graph.last is None
    assert graph.min_marker_area == 5