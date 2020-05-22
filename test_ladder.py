from ladder import LadderBoard, LadderMoveType, LadderGraph


def test_create():
    start_state = '''\
x x x x x x x

x N 0|1 2 B x
        - -
x x P|5 6 R x

x x x x x x x
---
P4R0NxB3
---
M5
'''

    board = LadderBoard.create(start_state)

    assert board.display() == start_state
    assert board.target == 5
    assert board.move_type == LadderMoveType.MARKER


def test_generate_domino_moves():
    start_state = '''\
x x x x x x x

x N 0|1 2 B x
        - -
x x P|5 6 R x

x x x x x x x
---
P4R0NxB3
---
D5
'''
    board = LadderBoard.create(start_state)
    graph = LadderGraph()
    expected_moves = {
        ('D...', '''\
N 0|1 2 B
      - -
x P|5 6 R
---
P4R0NxB3
---
M5
'''),
        ('DPL', '''\
N 0|1 2 B
      - -
P|5 x 6 R
---
P4R0NxB3
---
M5
'''),
        ('DRU', '''\
x x x x B
        -
N 0|1 2 R
      -
x P|5 6 x
---
P4NxR0B3
---
M5
'''),
        ('DRD', '''\
N 0|1 2 x
      -
x P|5 6 B
        -
x x x x R
---
R0P4B3Nx
---
M5
''')}

    moves = set(graph.generate_moves(board))

    assert moves == expected_moves
