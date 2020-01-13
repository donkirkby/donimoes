from domino_puzzle import Board
from dominosa import place_unique_pairs


def test_place_unique_pairs_vertical():
    board = Board.create("""\
1 0 1

1 0 0
""")
    expected_display = """\
1 0 1
-
1 0 0
"""

    place_unique_pairs(board)

    display = board.display()

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

    place_unique_pairs(board)  # Place doubles.
    place_unique_pairs(board)  # Place 0|1.

    display = board.display()

    assert display == expected_display
