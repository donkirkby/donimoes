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

x 0|1 2 B x
      - -
x P|5 6 R x

x x x x x x
---
P4R0B3
---
2
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('62U2', '''\
x x 2 x
    -
0|1 6 B
      -
P|5 x R
---
P4R0B3
---
3
''', None, 2),
        ('62D2', '''\
0|1 x B
      -
P|5 2 R
    -
x x 6 x
---
P4R0B3
---
3
''', None, 2),
        ('BL2', '''\
0|1 B 3
    - -
P|5 6 R
---
P4R0B2
---
3
''', None, 2)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_board_stays_connected():
    start_state = '''\
x x x x x x x

x 1|2 x x x x

x x N|4 5|P x

x x x x x x x
---
N3P6
---
1
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('12R1', '''\
1|2 x x

N|4 5|P
---
N3P6
---
2
''', None, 1)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_only_empty_dominoes_move():
    start_state = '''\
x x x x x x x

x 1|N x x x x

x x 3|4 5|P x

x x x x x x x
---
N2P6
---
1
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('NL1', '''\
N|2 x x x

x 3|4 5|P
---
P6N1
---
2
''', None, 3)}
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
    expected_solution = ['NR1', 'PU2', 'BL3', 'RU4', 'SOLVED']
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
    expected_solution = ['NR1', 'PU2', 'BL3', 'RU4', 'SOLVED']
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

    assert len(solution) == 36
