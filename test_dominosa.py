from domino_puzzle import Board
from dominosa import place_unique_pairs, find_unique_pairs, join_pairs, find_one_neighbour_pairs, find_unjoined_pairs, \
    find_solutions


def test_find_unique_pairs_vertical():
    board = Board.create("""\
1 0 1

1 0 0
""")
    expected_pairs = [(0, 0, 0, 1)]
    expected_display = """\
1 0 1
-
1 0 0
"""

    pairs = find_unique_pairs(board)
    join_pairs(board, pairs)
    display = board.display()

    assert pairs == expected_pairs
    assert display == expected_display


def test_place_unique_pairs_horizontal():
    board = Board.create("""\
1 1

0 0

1 0
""")
    expected_display = """\
1|1

0 0

1 0
"""

    place_unique_pairs(board)

    display = board.display()

    assert display == expected_display


def test_unique_pairs_solution():
    board = Board.create("""\
1 1 0

0 0 1
""")
    expected_display = """\
1|1 0
    -
0|0 1
"""

    num_placed = place_unique_pairs(board)  # Place doubles.
    place_unique_pairs(board)  # Place 0|1.

    display = board.display()

    assert display == expected_display
    assert num_placed == 2  # Two doubles placed in first call.


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


def test_place_only_neighbours():
    board = Board.create("""\
1 1 0 1

0|0 2 0

1 2 2 2
""")

    expected_display = """\
1|1 0 1

0|0 2 0

1|2 2 2
"""

    pairs = find_one_neighbour_pairs(board)
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
