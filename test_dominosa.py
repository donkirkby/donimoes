from networkx import DiGraph

from dominosa import DominosaBoard, PairState, DominosaGraph, DominosaProblem, \
    generate_moves_from_unique_pairs, generate_moves_from_single_neighbours, \
    generate_moves_from_newly_joined, generate_moves_from_newly_split, \
    generate_moves_from_duplicate_neighbours, FitnessCalculator, strip_solution


def test_rule6_unique_pairs_vertical():
    start_state = """\
1 0 1

1 0 0
"""
    board = DominosaBoard.create(start_state, max_pips=1)
    expected_display = """\
1 0 1
j
1 0 0
"""
    expected_moves = [('6:00j01', expected_display)]

    moves = list(generate_moves_from_unique_pairs(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule6_unique_pairs_horizontal():
    board = DominosaBoard.create("""\
1 1

0 0

1 0
""", max_pips=1)
    expected_display = """\
1j1

0 0

1 0
"""

    expected_moves = [('6:02j12', expected_display)]

    moves = list(generate_moves_from_unique_pairs(board))

    assert moves == expected_moves


def test_rule1_single_neighbour():
    start_state = """\
1 1 0 1
s s
0|0s2 0
s s
1 2 2 2
"""
    board = DominosaBoard.create(start_state, max_pips=2)
    expected_display1 = """\
1 1 0 1
s s
0|0s2 0
s s
1j2 2 2
"""
    expected_display2 = """\
1j1 0 1
s s
0|0s2 0
s s
1 2 2 2
"""
    expected_moves = [('1:00j10', expected_display1),
                      ('1:02j12', expected_display2)]

    moves = list(generate_moves_from_single_neighbours(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule1_single_neighbour_for_cell():
    start_state = """\
1 1 0 1
s
0s0 2 0
-
1s2 2 2
"""
    board = DominosaBoard.create(start_state, max_pips=2)
    expected_display = """\
1j1 0 1
s
0s0 2 0
-
1s2 2 2
"""
    expected_moves = [('1:02j12', expected_display)]

    moves = list(generate_moves_from_single_neighbours(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule6_big_head():
    start_state = """\
2 2s1|1s0
    s s -
2 1s0|0s2
s s s s s
3 3 3 2 3
  s
0 1 0 3 1
"""
    board = DominosaBoard.create(start_state, max_pips=2)
    expected_moves = []
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule1_to_solution():
    start_state = """\
0 0 1
s s j
1|1s0
"""
    board = DominosaBoard.create(start_state, max_pips=1)
    expected_display = """\
0|0 1
    -
1|1 0
"""
    expected_moves = [('1:01j11', expected_display, {'weight': 1,
                                                     'move_num': 1})]
    graph = DominosaGraph(DominosaBoard, move_weights={1: 1})

    moves = list(graph.generate_moves(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule2_split_neighbours():
    start_state = """\
1 0 1
j
1 0 0
"""
    board = DominosaBoard.create(start_state, max_pips=1)
    expected_display = """\
1s0 1
-
1s0 0
"""
    expected_moves = [('2:00|01,00s10,01s11', expected_display)]

    moves = list(generate_moves_from_newly_joined(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule2_split_duplicate():
    start_state = """\
2j2 2 0
~ ~
0|0 2 1

1|1 0 1
"""
    board = DominosaBoard.create(start_state, max_pips=2)
    expected_display = """\
2|2s2 0
~ ~ s
0|0 2 1

1|1 0 1
"""
    expected_moves = [('2:02|12,12s22,21s22', expected_display)]

    moves = list(generate_moves_from_newly_joined(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule3_newly_split():
    start_state = """\
1s1 2 3 1
-
0s2 2 2 3
s
0 2 0 3 1

3 0 0 3 1
"""
    board = DominosaBoard.create(start_state, max_pips=3)
    expected_display = """\
1S1 2 3 1
-
0S2 2 2 3
~
0 2 0 3 1
        j
3 0 0 3 1
"""
    expected_moves = [('3:01S02,02S12,03S13,40j41', expected_display)]

    moves = list(generate_moves_from_newly_split(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule4_duplicate_neighours():
    start_state = """\
2 2 0 1

2 1 0 1

2 0 0 1
"""
    board = DominosaBoard.create(start_state, max_pips=3)
    expected_display = """\
2 2 0 1

2 1 0 1
s
2 0 0 1
"""
    expected_moves = [('4:02,00s01', expected_display)]

    moves = list(generate_moves_from_duplicate_neighbours(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_rule5_shared_space():
    start_state = """\
2 3 3 1 3

0 1 2 0 3

0 0 2 2 3
~ ~
1|1S2 1 0
"""
    board = DominosaBoard.create(start_state, max_pips=3)
    expected_display = """\
2 3 3 1 3

0 1 2 0 3

0 0s2 2 3
~ ~
1|1S2 1 0
"""
    expected_moves = [('5:21,21s11', expected_display, {'weight': 1,
                                                        'move_num': 5})]
    graph = DominosaGraph(DominosaBoard, move_weights={5: 1, 6: 10})

    moves = list(graph.generate_moves(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_move_weights():
    start_state = """\
1 1 0

0 0 1
"""
    board = DominosaBoard.create(start_state, max_pips=1)

    graph = DominosaGraph(DominosaBoard, move_weights={1: 2,
                                                       2: 3,
                                                       3: 4,
                                                       4: 5,
                                                       5: 10,
                                                       6: 7})

    graph.walk(board)
    graph_x: DiGraph = graph.graph
    dup_state = """\
1 1s0
s s
0 0 1
"""
    joined_state = """\
1j1s0
s s
0 0 1
"""
    weight4 = graph_x.get_edge_data(start_state, dup_state)['weight']
    weight1 = graph_x.get_edge_data(dup_state, joined_state)['weight']

    assert weight4 == 5
    assert weight1 == 2


def test_get_pair_state_default():
    board = DominosaBoard.create("""\
1 0 1

1 0 0
""")

    pair_state = board.get_pair_state(0, 0, 0, 1)

    assert pair_state == PairState.UNDECIDED


def test_get_pair_state_vertical():
    board = DominosaBoard.create("""\
1 0 1
j
1 0 0
""")

    pair_state1 = board.get_pair_state(0, 0, 0, 1)
    pair_state2 = board.get_pair_state(0, 1, 0, 0)

    assert pair_state1 == PairState.NEWLY_JOINED
    assert pair_state2 == PairState.NEWLY_JOINED


def test_get_pair_state_horizontal():
    board = DominosaBoard.create("""\
1s0 1
-
1S0 0
""")

    pair_state1 = board.get_pair_state(0, 1, 1, 1)
    pair_state2 = board.get_pair_state(1, 1, 0, 1)

    assert pair_state1 == PairState.NEWLY_SPLIT
    assert pair_state2 == PairState.NEWLY_SPLIT


def test_display_pair_state():
    expected_state = """\
1s0|1
-
1S0j0
"""
    board = DominosaBoard.create(expected_state)

    state = board.display()

    assert state == expected_state


def test_random_init():
    expected_keys = {'solution', 'max_pips'}

    problem = DominosaProblem(init_params=dict(width=4, height=5, max_pips=3))

    assert problem.value.keys() == expected_keys
    lines = problem.value['solution'].splitlines(keepends=False)
    assert len(lines) == 9
    assert len(lines[0]) == 7
    assert 'x' not in problem.value['solution']


def test_fitness_counts_unplaced_dominoes():
    value = dict(solution="""\
0 1 1
- - -
0 1 0
""",
                 max_pips=1)
    problem = DominosaProblem(value)
    expected_dominoes_unused = 2
    expected_move_types_unused = 2
    expected_fitness = (-1_000_000 * expected_dominoes_unused +
                        -10_000 * expected_move_types_unused)

    calculator = FitnessCalculator()
    fitness = calculator.calculate(problem)

    assert fitness == expected_fitness


def test_fitness_counts_solution_moves():
    value = dict(solution="""\
1|2 0|1

0 0|2 2
-     -
0 1|1 2
""",
                 max_pips=2)
    problem = DominosaProblem(value)
    rule5_move_count = 1
    other_move_count = 9
    unused_move_types = 3
    expected_fitness = -(10*rule5_move_count +
                         other_move_count +
                         10_000*unused_move_types)

    calculator = FitnessCalculator(move_weights={1: 1,
                                                 2: 1,
                                                 3: 1,
                                                 4: 1,
                                                 5: 10,
                                                 6: 100})
    fitness = calculator.calculate(problem)

    assert fitness == expected_fitness


def test_strip_solution():
    solution = """\
1|2 3
    -
4|5 6
"""
    expected_stripped = """\
    1 2 3
    
    4 5 6"""

    stripped = strip_solution(solution)

    assert stripped == expected_stripped
