from domino_puzzle import Board, GraphLimitExceeded
from mirror import MirrorGraph, MirrorProblem, MirrorFitnessCalculator


def test_generate_moves():
    start_state = '''\
0|0 1|2

B|1 0|P

2|2 0|1
---
B1P2
'''
    board = Board.create(start_state, border=1)
    graph = MirrorGraph()
    expected_moves = {
        ('PdR', '''\
0|0 1|2 x

B|1 x 0|P

2|2 0|1 x
---
B1P2
''', None, 2),
        ('BdL', '''\
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
        ('PU', '''\
0|0 1|P

B|1 0|2

2|2 0|1
---
B1P2
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
    graph = MirrorGraph()
    expected_moves = {
        ('NdR', '''\
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
0|0 1|0

B|1 0|P

2|2 1|N
---
N2B1P2
'''
    board = Board.create(start_state, border=1)
    graph = MirrorGraph()
    expected_moves = {
        ('PdR', '''\
0|0 1|0 x

B|1 x 0|P

2|2 1|N x
---
N2B1P2
''', None, 4),
        ('BdL', '''\
x 0|0 1|0

B|1 x 0|P

x 2|2 1|N
---
N2B1P2
''', None, 5),
        ('NdR', '''\
0|0 1|0 x

B|1 0|P x

2|2 x 1|N
---
N2B1P2
''', None, 4),
        ('BR', '''\
0|0 1|0

1|B 0|P

2|2 1|N
---
N2B1P2
''', None, 2),
        ('PL', '''\
0|0 1|0

B|1 P|2

2|2 1|N
---
N2B1P0
''', None, 3),
        ('NL', '''\
0|0 1|0

B|1 0|P

2|2 N|2
---
N1B1P2
''', None, 3)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_domino_moves_both_markers():
    start_state = '''\
2 0|1 B
-     -
2 P|1 R

2|0 1|2
---
P1R0B0
'''
    board = Board.create(start_state, border=1)
    graph = MirrorGraph()
    expected_moves = {
        ('RdU', '''\
x x x B
      -
2 0|1 R
-
2 P|1 x

2|0 1|2
---
P1R0B0
''', None, 2),
        ('PR', '''\
2 0|1 B
-     -
2 1|P R

2|0 1|2
---
P1R0B0
''', None, 0)}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves


def test_walk():
    start_state = '''\
P 1 B
- - -
N 1 R
---
N0R0P1B0
'''
    expected_solution = ['PR', 'PD']
    board = Board.create(start_state)
    graph = MirrorGraph()

    graph.walk(board)

    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_adds_markers():
    start_state = '''\
1 1 0
- - -
0 1 0
'''
    expected_solution = ['PR', 'PD']
    board = Board.create(start_state)
    graph = MirrorGraph()

    graph.walk(board)
    solution = graph.get_solution()

    assert solution == expected_solution


def test_walk_sets_min_heuristic():
    start_state = '''\
1 1 0 2 2
- - - - -
0 1 0 2 0
'''
    board = Board.create(start_state)
    graph = MirrorGraph()

    try:
        graph.walk(board, size_limit=1000)
    except GraphLimitExceeded:
        pass

    assert graph.last is None
    assert graph.min_heuristic == 2


def test_calculate_heuristic():
    board = Board.create('''\
0|1 0|B 0|3

N|2 1|3 R|4

2|P 2|4 2|5
---
P3N1R1B2
''')
    expected_heuristic = 4
    graph = MirrorGraph()

    heuristic = graph.calculate_heuristic(board)

    assert heuristic == expected_heuristic


def test_fitness_calculator():
    start_state = '''\
1 1 0
- - -
0 1 0
'''
    problem = MirrorProblem(dict(start=start_state, max_pips=1))
    calculator = MirrorFitnessCalculator()
    calculator.calculate(problem)

    summaries = calculator.format_summaries()
    details = calculator.format_details()
    assert summaries == 'PR, PD'
    assert details == '3x2: 2 moves, max 9, avg 5.0, 15 states'


def test_repeated_moves_in_summary():
    start_state = '''\
2|2 0 2
    - -
1|0 0 1
'''
    problem = MirrorProblem(dict(start=start_state, max_pips=2))
    calculator = MirrorFitnessCalculator()
    calculator.calculate(problem)

    assert calculator.format_summaries() == 'PR, NR2, RdU, NdU'
