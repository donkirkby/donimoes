from domino_puzzle import Board, GraphLimitExceeded
from partners import PartnerGraph


def test_generate_moves():
    start_state = '''\
0|0 1|2

B|1 0|P

2|2 0|1
---
B1P2
'''
    board = Board.create(start_state, border=1)
    graph = PartnerGraph()
    expected_moves = {
        ('PDR', '''\
0|0 1|2 x

B|1 x 0|P

2|2 0|1 x
---
B1P2
''', None, 2),
        ('BDL', '''\
x 0|0 1|2

B|1 x 0|P

x 2|2 0|1
---
B1P2
''', None, 2),
        ('BR', '''\
0|0 1|2

1|B 0|P

2|2 0|1
---
B1P2
''', None, 0),
        ('PD', '''\
0|0 1|2

B|1 0|2

2|2 0|P
---
P1B1
''', None, 2),
        ('PL', '''\
0|0 1|2

B|1 P|2

2|2 0|1
---
B1P0
''', None, 0)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_board_stays_connected():
    start_state = '''\
1|N x x x

x 3|4 5|P
---
P6N2
'''
    board = Board.create(start_state, border=1)
    graph = PartnerGraph()
    expected_moves = {
        ('NDR', '''\
1|N x x

3|4 5|P
---
P6N2
''', None, 1),
        ('NL', '''\
N|2 x x x

x 3|4 5|P
---
P6N1
''', None, 3),
        ('PL', '''\
1|N x x x

x 3|4 P|6
---
P5N2
''', None, 1)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_markers_block_each_other():
    start_state = '''\
0|0 1|2

B|1 0|P

2|2 0|N
---
N1B1P2
'''
    board = Board.create(start_state, border=1)
    graph = PartnerGraph()
    expected_moves = {
        ('PDR', '''\
0|0 1|2 x

B|1 x 0|P

2|2 0|N x
---
N1B1P2
''', None, 4),
        ('BDL', '''\
x 0|0 1|2

B|1 x 0|P

x 2|2 0|N
---
N1B1P2
''', None, 5),
        ('NDR', '''\
0|0 1|2 x

B|1 0|P x

2|2 x 0|N
---
N1B1P2
''', None, 4),
        ('BR', '''\
0|0 1|2

1|B 0|P

2|2 0|N
---
N1B1P2
''', None, 2),
        ('PL', '''\
0|0 1|2

B|1 P|2

2|2 0|N
---
N1B1P0
''', None, 3),
        ('NL', '''\
0|0 1|2

B|1 0|P

2|2 N|1
---
N0B1P2
''', None, 3)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_one_marker_per_domino():
    start_state = '''\
0|0 1|2

B|1 0|P

2|2 N|1
---
N0B1P2
'''
    board = Board.create(start_state, border=1)
    graph = PartnerGraph()
    expected_moves = {
        ('PDR', '''\
0|0 1|2 x

B|1 x 0|P

2|2 N|1 x
---
N0B1P2
''', None, 3),
        ('BDL', '''\
x 0|0 1|2

B|1 x 0|P

x 2|2 N|1
---
N0B1P2
''', None, 4),
        ('NDR', '''\
0|0 1|2 x

B|1 0|P x

2|2 x N|1
---
N0B1P2
''', None, 3),
        ('NR', '''\
0|0 1|2

B|1 0|P

2|2 0|N
---
N1B1P2
''', None, 3),
        ('BR', '''\
0|0 1|2

1|B 0|P

2|2 N|1
---
N0B1P2
''', None, 1),
        ('PL', '''\
0|0 1|2

B|1 P|2

2|2 N|1
---
N0B1P0
''', None, 2)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_walk():
    start_state = '''\
N|0 2|B

1 0 1|2
- -
P 1 0|R
---
P1R2N0B2
'''
    expected_solution = ['PU', 'PR', 'NR', 'RL', 'RU', 'BL']
    board = Board.create(start_state)
    graph = PartnerGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_adds_markers():
    start_state = '''\
0|0 2|2

1 0 1|2
- -
1 1 0|2
'''
    expected_solution = ['PU', 'PR', 'NR', 'RL', 'RU', 'BL']
    board = Board.create(start_state)
    graph = PartnerGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_sets_smallest_area():
    start_state = '''\
6 4 1 2 3
- - - - -
6 6 1 3 3

5 4 0 2 4
- - - - -
5 5 0 4 4
'''
    board = Board.create(start_state)
    graph = PartnerGraph()

    try:
        graph.walk(board, size_limit=1000)
    except GraphLimitExceeded:
        pass

    assert graph.last is None
    assert graph.min_marker_area == 6


def test_calculate_heuristic():
    board = Board.create('''\
0|1 0|B 0|3

N|2 1|3 R|4

2|P 2|4 2|5
---
P3N1R1B2
---
1
''')
    expected_heuristic = 4
    graph = PartnerGraph()

    heuristic = graph.calculate_heuristic(board)

    assert heuristic == expected_heuristic
