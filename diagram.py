from functools import partial


def draw_pips(turtle, pips, cell_size):
    PIP_PATTERNS = """\
---+
   |
   |
   |
---+
   |
 O |
   |
---+
O  |
   |
  O|
---+
O  |
 O |
  O|
---+
O O|
   |
O O|
---+
O O|
 O |
O O|
---+
OOO|
   |
OOO|
---+
"""
    pip_pattern = PIP_PATTERNS.splitlines()[pips*4+1:pips*4+4]
    pip_radius = cell_size*0.09
    turtle.up()
    pos = turtle.pos()
    turtle.back(pip_radius*5)
    turtle.left(90)
    turtle.forward(pip_radius*5)
    turtle.right(90)
    for i in range(3):
        turtle.forward(pip_radius*2)
        turtle.right(90)
        turtle.forward(pip_radius)
        turtle.left(90)
        for j in range(3):
            if pip_pattern[i][j] == 'O':
                turtle.down()
                turtle.begin_fill()
                turtle.circle(-pip_radius)
                turtle.end_fill()
                turtle.up()
            turtle.forward(pip_radius*3)
        turtle.back(pip_radius*11)
        turtle.right(90)
        turtle.forward(pip_radius*2)
        turtle.left(90)
    turtle.setpos(pos)


def draw_domino(turtle, domino, cell_size=50.0):
    turtle.up()
    turtle.back(cell_size*0.45)
    turtle.left(90)
    turtle.forward(cell_size*0.45)
    turtle.right(90)
    turtle.down()
    for _ in range(2):
        turtle.forward(cell_size*1.9)
        turtle.right(90)
        turtle.forward(cell_size*.9)
        turtle.right(90)

    turtle.up()
    turtle.forward(cell_size*.95)
    turtle.right(90)
    turtle.forward(cell_size*.1)
    turtle.down()
    turtle.forward(cell_size*.7)
    turtle.up()
    turtle.back(cell_size*.35)
    turtle.left(90)
    turtle.back(cell_size*.5)
    draw_pips(turtle, domino.head.pips, cell_size)
    turtle.forward(cell_size)
    draw_pips(turtle, domino.tail.pips, cell_size)
    turtle.back(cell_size)


def draw_board(turtle, board, cell_size=50.0):
    pos = turtle.pos()
    for y in range(board.height):
        for x in range(board.width):
            cell = board[x][y]
            if cell is not None:
                domino = cell.domino
                if cell is domino.head:
                    turtle.left(domino.degrees)
                    draw_domino(turtle, domino, cell_size)
                    turtle.right(domino.degrees)
            turtle.forward(cell_size)
        turtle.up()
        turtle.back(cell_size*board.width)
        turtle.left(90)
        turtle.forward(cell_size)
        turtle.right(90)
    turtle.setpos(pos)


def draw_arrow(turtle, cell_size, rotation=0):
    pos = turtle.pos()
    turtle.left(rotation)
    turtle.back(cell_size*.2)
    turtle.down()
    turtle.left(90)
    turtle.begin_fill()
    turtle.forward(cell_size*.05)
    turtle.right(90)
    turtle.forward(cell_size*.3)
    turtle.left(90)
    turtle.forward(cell_size*.1)
    turtle.right(120)
    turtle.forward(cell_size*.3)
    turtle.right(120)
    turtle.forward(cell_size*.3)
    turtle.right(120)
    turtle.forward(cell_size*.1)
    turtle.left(90)
    turtle.forward(cell_size*.3)
    turtle.right(90)
    turtle.forward(cell_size*.05)
    turtle.right(90)
    turtle.forward(cell_size*.2)
    turtle.end_fill()
    turtle.up()
    turtle.setpos(pos)
    turtle.right(rotation)


def draw_diagram(turtle, state, cell_size):
    marks = {'>': partial(draw_arrow, turtle, cell_size),
             '^': partial(draw_arrow, turtle, cell_size, 90),
             '<': partial(draw_arrow, turtle, cell_size, 180),
             'v': partial(draw_arrow, turtle, cell_size, 270)}
    pos = turtle.pos()
    board = Board.create(state)
    draw_board(turtle, board, cell_size)
    lines = state.splitlines()
    for y, line in enumerate(reversed(lines)):
        for x, c in enumerate(line.strip()):
            if (x+y) % 2:
                mark = marks.get(c)
                if mark is not None:
                    mark()
            turtle.forward(cell_size*.5)
        turtle.back(cell_size*len(line)*.5)
        turtle.left(90)
        turtle.forward(cell_size*.5)
        turtle.right(90)
    turtle.setpos(pos)


def draw_position(turtle, size=10, color='red'):
    old_pen = turtle.pen()
    old_pos = turtle.pos()
    old_heading = turtle.heading()
    turtle.color(color)
    turtle.begin_fill()

    turtle.left(90)

    turtle.forward(size*0.5)
    turtle.right(120)
    turtle.forward(size)
    turtle.right(120)
    turtle.forward(size)
    turtle.right(120)
    turtle.forward(size*0.5)

    turtle.right(90)

    turtle.end_fill()
    turtle.setheading(old_heading)
    turtle.setpos(old_pos)
    turtle.pen(old_pen)

if __name__ == '__live_coding__':
    from domino_puzzle import Board
    turtle = __live_turtle__  # @UndefinedVariable
    cell_size = 60
    turtle.up()
    turtle.back(cell_size)
    turtle.right(90)
    turtle.forward(cell_size*3)
    turtle.left(90)
    turtle.down()

    state1 = """\
2 0|4
-
5 1|6
"""
    draw_diagram(turtle, state1, cell_size)
    turtle.left(90)
    turtle.forward(cell_size*2)
    turtle.right(90)

    state2 = """\
2 0<4
^
5   1>6
"""
    draw_diagram(turtle, state2, cell_size)