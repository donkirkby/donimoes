from networkx import DiGraph

from domino_puzzle import Board
from dominosa import find_unique_pairs, join_pairs, find_one_neighbour_pairs, \
    find_unjoined_pairs, find_solutions, DominosaBoard, PairState, DominosaGraph, DominosaProblem, calculate_fitness


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
    expected_moves = [('6:00j01', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
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

    expected_moves = [('6:02j12', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))

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
    expected_moves = [('1:00j10', expected_display1, {}),
                      ('1:02j12', expected_display2, {})]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
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
    expected_moves = [('1:02j12', expected_display, {})]
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
    expected_moves = [('1:01j11', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

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
    expected_moves = [('2:00|01,00s10,01s11', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
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
    expected_moves = [('2:02|12,12s22,21s22', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
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
    expected_moves = [('3:01S02,02S12,03S13,40j41', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
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
    expected_moves = [('4:02,00s01', expected_display, {})]
    graph = DominosaGraph(DominosaBoard)

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
                                                       6: 10})

    graph.walk(board)
    graph_x: DiGraph = graph.graph
    newly_joined_state = """\
1j1 0

0 0 1
"""
    joined_state = """\
1|1s0
s s
0 0 1
"""
    weight6 = graph_x.get_edge_data(start_state,
                                    newly_joined_state)['weight']
    weight2 = graph_x.get_edge_data(newly_joined_state,
                                    joined_state)['weight']

    assert weight6 == 10
    assert weight2 == 3


def test_unique_pairs_check_joined():
    board = Board.create("""\
2|2 2 0

0|0 2 1

1|1 0 1
""")
    expected_pairs = [(2, 1, 3, 1)]
    expected_display = """\
2|2 2 0

0|0 2|1

1|1 0 1
"""

    pairs = find_unique_pairs(board)

    assert pairs == expected_pairs

    join_pairs(board, pairs)
    display = board.display()

    assert display == expected_display


def test_unique_pairs_conflict():
    board = Board.create("""\
1 1 0 1
-
0 0|2 1

0 2|2 2
""")
    expected_display = """\
1 1 0 1
-
0 0|2 1
      -
0 2|2 2
"""

    pairs = find_unique_pairs(board)
    join_pairs(board, pairs)
    display = board.display()

    assert display == expected_display


def test_place_only_neighbours_conflict():
    board = Board.create("""\
2 3 2|2 3

0 1|2 2 3

1 1 0 3 3
    - - -
0 1 0 0 1
""")

    expected_display = """\
2|3 2|2 3
        -
0 1|2 2 3

1 1 0 3 3
    - - -
0 1 0 0 1
"""

    pairs = find_one_neighbour_pairs(board)
    join_pairs(board, pairs)
    display = board.display()

    assert display == expected_display


def test_place_only_neighbours_existing_duplicate():
    board = Board.create("""\
0|0 0 1
    -
0 2 2 1

1|1 2|2
""")

    expected_display = """\
0|0 0 1
    -
0 2 2 1

1|1 2|2
"""

    pairs = find_one_neighbour_pairs(board)
    join_pairs(board, pairs)
    display = board.display()

    assert display == expected_display


def test_place_only_neighbours_new_duplicate():
    board = Board.create("""\
0 0 0 1
-   -
0 2 2 1

1 1 2|2
""")

    expected_display = """\
0 0 0 1
-   -
0 2 2 1

1|1 2|2
"""

    pairs = find_one_neighbour_pairs(board)
    join_pairs(board, pairs)
    display = board.display()

    assert display == expected_display


def test_find_unjoined_pairs():
    board = Board.create("""\
1 0 1
-
1 0 0
""")
    expected_pairs = [(1, 0, 1, 1), (1, 0, 2, 0), (1, 1, 2, 1), (2, 0, 2, 1)]

    pairs = find_unjoined_pairs(board)

    assert pairs == expected_pairs


def test_find_solutions():
    board = Board.create("""\
1 0 1
-
1 0 0
""")
    expected_solutions = set("""\
1 0 1
- - -
1 0 0
=====
1 0|1
-
1 0|0
""".split('=====\n'))

    solutions = find_solutions(board)

    assert solutions == expected_solutions


def test_find_solutions_no_duplicates():
    board = Board.create("""\
2|2 1 2

1|1 0 2

0|0 0 1
""")
    expected_solutions = {"""\
2|2 1|2

1|1 0|2

0|0 0|1
"""}

    solutions = find_solutions(board)

    assert solutions == expected_solutions


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
    expected_fitness = -10000 * expected_dominoes_unused

    fitness = calculate_fitness(problem)

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
    unique_pair_move_count = 1
    other_move_count = 8
    expected_fitness = -(10*unique_pair_move_count + other_move_count)

    fitness = calculate_fitness(problem, move_weights={1: 1,
                                                       2: 1,
                                                       3: 1,
                                                       6: 10})

    assert fitness == expected_fitness
