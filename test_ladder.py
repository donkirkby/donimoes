from domino_puzzle import GraphLimitExceeded
from ladder import LadderBoard, LadderGraph


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
5
'''

    board = LadderBoard.create(start_state)

    assert board.display() == start_state
    assert board.target == 5


def test_generate_moves():
    start_state = '''\
x x x x x x

x 0|2 2 B x
      - -
x P|5 R 0 x

x x x x x x
---
P4R6B3
---
2
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('RDU2', '''\
x x 2 x
    -
0|2 R B
      -
P|5 x 0
---
P4R6B3
---
3
''', None, 3),
        ('RDD2', '''\
0|2 x B
      -
P|5 2 0
    -
x x R x
---
R6P4B3
---
3
''', None, 3),
        ('BL2', '''\
0|2 B 3
    - -
P|5 R 0
---
P4R6B2
---
3
''', None, 1),
        ('RU2', '''\
0|2 R B
    - -
P|5 6 0
---
P4R2B3
---
3
''', None, 3)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_board_stays_connected():
    start_state = '''\
x x x x x x x

x 1|N x x x x

x x 3|4 5|P x

x x x x x x x
---
P6N2
---
1
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('NDR1', '''\
1|N x x

3|4 5|P
---
P6N2
---
2
''', None, 1),
        ('NL1', '''\
N|2 x x x

x 3|4 5|P
---
P6N1
---
2
''', None, 3)
    }

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_two_markers_stop_move():
    start_state = '''\
x x x x x x x

x 2|0 2|3 x x

x 3|0 0|1 x x

x N|P x B|R x

x x x x x x x
---
N3P3B2R2
---
3
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('NU3', '''\
2|0 2|3 x

N|0 0|1 x

3|P x B|R
---
P3B2R2N3
---
4
''', None, 3)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_markers_not_lost():
    start_state = '''\
P|3 2|R
---
P3R2
---
3
'''
    board = LadderBoard.create(start_state, border=1)
    graph = LadderGraph()
    expected_moves = {
        ('PR3', '''\
3|P 2|R
---
P3R2
---
4
''', None, 0)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_walk():
    start_state = '''\
N 1|3 B
-     -
P 0|0 R
---
P0R0N2B4
---
1
'''
    expected_solution = ['NR1', 'PDU2', 'BL3', 'RDU4', 'SOLVED']
    board = LadderBoard.create(start_state)
    graph = LadderGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_adds_markers():
    start_state = '''\
2 1|3 4
-     -
0 0|0 0
'''
    expected_solution = ['NR1', 'PDU2', 'BL3', 'RDU4', 'SOLVED']
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


def test_calculate_heuristic():
    board = LadderBoard.create('''\
0|1 0|B 0|3

N|2 1|3 R|4

2|P 2|4 2|5
---
P3N1R1B2
---
1
''')
    expected_heuristic = 4
    graph = LadderGraph()

    heuristic = graph.calculate_heuristic(board)

    assert heuristic == expected_heuristic


def test_fast_walker():
    board = LadderBoard.create('''\
2 2|3 2
-     -
1 0|0 2

0|3 3|3
''', max_pips=3)
    graph = LadderGraph()

    try:
        graph.walk(board, size_limit=1000)
    except GraphLimitExceeded:
        pass

    solution = graph.get_solution()

    assert len(solution) == 13
