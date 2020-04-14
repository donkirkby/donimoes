from domino_puzzle import Board
from dominosa import find_unique_pairs, join_pairs, find_one_neighbour_pairs, \
    find_unjoined_pairs, find_solutions, DominosaBoard, PairState, DominosaGraph


def test_find_unique_pairs_vertical():
    start_state = """\
1 0 1

1 0 0
"""
    board = DominosaBoard.create(start_state)
    expected_display = """\
1 0 1
j
1 0 0
"""
    expected_moves = [('6:00j01', expected_display)]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


def test_place_unique_pairs_horizontal():
    board = DominosaBoard.create("""\
1 1

0 0

1 0
""")
    expected_display = """\
1j1

0 0

1 0
"""

    expected_moves = [('6:02j12', expected_display)]
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
    board = DominosaBoard.create(start_state)
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
    board = DominosaBoard.create(start_state)
    expected_display = """\
1j1 0 1
s
0s0 2 0
-
1s2 2 2
"""
    expected_moves = [('1:02j12', expected_display)]
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
    board = DominosaBoard.create(start_state)
    expected_display = """\
1s0 1
-
1s0 0
"""
    expected_moves = [('2:00|01,00s10,01s11', expected_display)]
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
    board = DominosaBoard.create(start_state)
    expected_display = """\
2|2s2 0
~ ~ s
0|0 2 1

1|1 0 1
"""
    expected_moves = [('2:02|12,12s22,21s22', expected_display)]
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
    board = DominosaBoard.create(start_state)
    expected_display1 = """\
1s1 2 3 1
-
0s2 2 2 3
~
0 2 0 3 1

3 0 0 3 1
"""
    expected_display2 = """\
1s1 2 3 1
-
0S2 2 2 3
s
0 2 0 3 1

3 0 0 3 1
"""
    expected_display3 = """\
1S1 2 3 1
-
0s2 2 2 3
s
0 2 0 3 1
        j
3 0 0 3 1
"""
    expected_moves = [('3:01S02', expected_display1),
                      ('3:02S12', expected_display2),
                      ('3:03S13,40j41', expected_display3)]
    graph = DominosaGraph(DominosaBoard)

    moves = list(graph.generate_moves(board))
    final_state = board.display()

    assert moves == expected_moves
    assert final_state == start_state


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


def test_walk():
    board = DominosaBoard.create("""\
1|2 0|1

0 0|2 2
-     -
0 1|1 2
""")

    graph = DominosaGraph()
    states = graph.walk(board)
    print(*states, sep='\n\n')
    assert graph.has_solution


def test_display_pair_state():
    expected_state = """\
1s0|1
-
1S0j0
"""
    board = DominosaBoard.create(expected_state)

    state = board.display()

    assert state == expected_state
