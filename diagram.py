from functools import partial
import math
from turtle import Turtle

from domino_puzzle import Board, CaptureBoardGraph, Domino, Cell
from dominosa import PairState

DEFAULT_CELL_SIZE = 100
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


def draw_pips(turtle, pips, cell_size: float = DEFAULT_CELL_SIZE):
    pip_pattern = PIP_PATTERNS.splitlines()[pips*4+1:pips*4+4]
    pip_radius = cell_size*0.09
    turtle.up()
    pos = turtle.pos()
    turtle.back(pip_radius*5)
    turtle.left(90)
    turtle.forward(pip_radius*4)
    turtle.right(90)
    for i in range(3):
        turtle.forward(pip_radius*2)
        turtle.right(90)
        turtle.forward(pip_radius)
        turtle.left(90)
        for j in range(3):
            if pip_pattern[i][j] == 'O':
                turtle.dot(pip_radius*2)
            turtle.forward(pip_radius*3)
        turtle.back(pip_radius*11)
        turtle.right(90)
        turtle.forward(pip_radius*2)
        turtle.left(90)
    turtle.setpos(pos)


def draw_domino(turtle, domino, cell_size=DEFAULT_CELL_SIZE):
    start_fill = turtle.fillcolor()
    try:
        if domino.head.pips == '#':
            draw_domino_outline(turtle, cell_size, fill='black', margin=0)
            return
        draw_domino_outline(turtle, cell_size)
    finally:
        turtle.fillcolor(start_fill)

    turtle.up()
    turtle.forward(cell_size * 0.5)
    turtle.right(90)
    turtle.back(cell_size * 0.35)
    turtle.down()
    turtle.forward(cell_size*.7)
    turtle.up()
    turtle.back(cell_size*.35)
    turtle.left(90)
    turtle.forward(cell_size*.5)
    draw_pips(turtle, domino.tail.pips, cell_size)
    turtle.back(cell_size)
    draw_pips(turtle, domino.head.pips, cell_size)


def draw_cell(turtle, cell, cell_size=DEFAULT_CELL_SIZE):
    turtle.up()
    turtle.back(cell_size * 0.45)
    turtle.left(90)
    turtle.forward(cell_size * 0.45)
    turtle.right(90)
    r = cell_size * 0.1
    turtle.forward(r)
    turtle.down()
    turtle.fillcolor('white')
    old_colour = turtle.pencolor()
    turtle.pencolor('light grey')
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(cell_size * 0.7)
        turtle.up()
        turtle.circle(-r, 90)
        turtle.down()

    turtle.end_fill()
    turtle.pencolor(old_colour)

    turtle.up()
    turtle.back(r)
    turtle.forward(cell_size * 0.45)
    turtle.right(90)
    turtle.forward(cell_size * 0.45)
    turtle.left(90)
    draw_pips(turtle, cell.pips, cell_size)


def draw_domino_outline(turtle,
                        cell_size=DEFAULT_CELL_SIZE,
                        fill='white',
                        margin=0.05):
    start_colour = turtle.color()
    turtle.up()
    r = cell_size * 0.05
    margin_size = cell_size * margin
    turtle.back(cell_size/2-r-margin_size)
    turtle.left(90)
    turtle.forward(cell_size/2-margin_size)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor(fill)

    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(2*cell_size - 2*(margin_size + r))
        turtle.circle(-r, 90)
        turtle.forward(cell_size - 2*(margin_size + r))
        turtle.circle(-r, 90)
    turtle.end_fill()

    turtle.up()
    turtle.right(90)
    turtle.forward(cell_size/2-margin_size)
    turtle.left(90)
    turtle.forward(cell_size/2-r-margin_size)
    turtle.color(*start_colour)


def draw_die_outline(turtle,
                     die_size: float = DEFAULT_CELL_SIZE,
                     fill='white'):
    turtle.up()
    r = die_size / 12
    turtle.back(die_size / 2 - r)
    turtle.left(90)
    turtle.forward(die_size / 2)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor(fill)

    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(die_size - 2 * r)
        turtle.circle(-r, 90)
    turtle.end_fill()

    turtle.up()
    turtle.right(90)
    turtle.forward(die_size / 2)
    turtle.left(90)
    turtle.forward(die_size / 2 - r)


def draw_paths(turtle, board: Board, cell_size=DEFAULT_CELL_SIZE):
    pos = turtle.pos()
    old_colour = turtle.color()
    old_width = turtle.width()
    turtle.width(2)
    turtle.color('grey')
    turtle.up()
    turtle.forward(cell_size/2)
    turtle.left(90)
    turtle.back(cell_size*(board.height-0.5))
    for y in range(board.height):
        for x in range(board.width):
            cell: Cell = board[x][y]
            if y < board.height-1:
                lower_neighbour = board[x][y + 1]
                draw_neighbour_path(turtle, cell, lower_neighbour, cell_size)
            turtle.right(90)
            if x < board.width-1:
                draw_neighbour_path(turtle, cell, board[x+1][y], cell_size)
            turtle.forward(cell_size)
            turtle.left(90)
        turtle.forward(cell_size)
        turtle.left(90)
        turtle.forward(cell_size*board.width)
        turtle.right(90)
    turtle.setpos(pos)
    turtle.color(old_colour)
    turtle.width(old_width)


def draw_neighbour_path(turtle, cell, neighbour, cell_size):
    if abs(neighbour.pips - cell.pips) <= 1:
        turtle.down()
        turtle.forward(cell_size)
        turtle.up()
        turtle.back(cell_size)


def draw_board(turtle, board, cell_size=DEFAULT_CELL_SIZE):
    start_x, start_y = turtle.pos()
    start_colour = turtle.color()
    start_heading = turtle.heading()
    for y in range(board.height):
        for x in range(board.width):
            cell = board[x][y]
            if cell is not None:
                domino = cell.domino
                if domino is None:
                    draw_cell(turtle, cell, cell_size)
                elif cell is domino.head:
                    turtle.left(domino.degrees)
                    draw_domino(turtle, domino, cell_size)
                    turtle.right(domino.degrees)
            turtle.forward(cell_size)
        turtle.up()
        turtle.back(cell_size*board.width)
        turtle.left(90)
        turtle.forward(cell_size)
        turtle.right(90)
    for domino, x, y in board.offset_dominoes:
        turtle.setpos(start_x + x*cell_size, start_y + y*cell_size)
        turtle.left(domino.degrees)
        draw_domino(turtle, domino, cell_size)
        turtle.right(domino.degrees)
    for (x, y), marker in board.markers.items():
        turtle.setheading(start_heading+90)
        turtle.setpos(start_x + x*cell_size, start_y + y*cell_size)
        turtle.color(*start_colour)
        turtle.dot(0.75*cell_size)
        turtle.color('white')
        if marker == 'w':
            turtle.dot(0.7*cell_size)
            turtle.color(*start_colour)
            turtle.back(0.05*cell_size)
        elif marker == 'b':
            turtle.back(0.05*cell_size)
        else:
            turtle.back(0.05*cell_size)
            turtle.write(marker,
                         align='center',
                         font=('Arial', 0.20*cell_size, 'normal'))
        turtle.back(0.10*cell_size)
        cell = board[x][y]
        domino = cell.domino
        turtle.setheading(domino.degrees)
        draw_pips(turtle, cell.pips, int(0.30*cell_size))
    turtle.color(*start_colour)
    turtle.setpos((start_x, start_y))
    turtle.setheading(start_heading)


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
    turtle.end_fill()

    turtle.up()
    turtle.right(90)
    turtle.forward(cell_size*.2)
    turtle.setpos(pos)
    turtle.right(rotation)


def draw_cross(turtle, cell_size, rotation=0):
    pos = turtle.pos()

    thickness = cell_size*.1
    length = cell_size*.15
    turtle.up()
    turtle.right(rotation-45)
    turtle.right(45)
    turtle.forward(thickness*.5)
    turtle.left(90)
    turtle.forward(thickness*.5)
    turtle.down()
    turtle.begin_fill()
    for _ in range(4):
        turtle.forward(length)
        turtle.left(90)
        turtle.forward(thickness)
        turtle.left(90)
        turtle.forward(length)
        turtle.right(90)
    turtle.end_fill()
    turtle.right(45)
    turtle.left(rotation-45)
    turtle.up()

    turtle.setpos(pos)


def draw_move(turtle, cell_size, offset, domino, dx, dy, move_num, step_count):
    shade = (move_num-1) * 1.0/step_count
    rgb = (0, 1-shade, shade)
    turtle.forward((domino.head.x-offset[0]) * cell_size)
    turtle.left(90)
    turtle.forward((domino.head.y-offset[1]) * cell_size)
    turtle.right(90)
    turtle.setheading(domino.degrees)
    turtle.forward(cell_size*.5)
    turtle.setheading(math.atan2(dy, dx) * 180/math.pi)
    pen = turtle.pen()
    turtle.pencolor(rgb)
    circle_pos = turtle.pos()
    turtle.width(4)
    turtle.forward(cell_size*0.05)
    turtle.down()
    turtle.forward(cell_size*0.4)
    turtle.up()
    turtle.pen(pen)
    turtle.setpos(circle_pos)
    turtle.forward(8)
    turtle.setheading(270)
    turtle.forward(8)
    turtle.left(90)
    turtle.down()
    turtle.pencolor(rgb)
    turtle.fillcolor('white')
    turtle.begin_fill()
    turtle.circle(8)
    turtle.end_fill()
    turtle.pen(pen)
    turtle.write(move_num, align='center')
    turtle.up()


def draw_match(turtle, cell_size, offset, cell):
    turtle.forward((cell.x-offset[0]) * cell_size)
    turtle.left(90)
    turtle.forward((cell.y-offset[1]) * cell_size)
    turtle.right(90)
    pen = turtle.pen()
    turtle.color('red')
    turtle.up()
    turtle.back(10)
    turtle.right(90)
    turtle.begin_fill()
    turtle.circle(10)
    turtle.left(90)
    turtle.forward(5)
    turtle.right(90)
    turtle.circle(5)
    turtle.left(90)
    turtle.end_fill()
    turtle.pen(pen)


def draw_capture_circle(turtle,
                        cell_size,
                        offset,
                        domino,
                        move_num=None):
    x = (domino.head.x + domino.tail.x) * 0.5 - offset[0]
    y = (domino.head.y + domino.tail.y) * 0.5 - offset[1]
    pen = turtle.pen()
    turtle.forward(x*cell_size)
    turtle.left(90)
    turtle.forward(y*cell_size)
    turtle.right(90)
    turtle.setheading(270)
    turtle.forward(8)
    turtle.left(90)
    turtle.down()
    turtle.pencolor('red')
    turtle.fillcolor('red' if move_num is None else 'white')
    turtle.begin_fill()
    turtle.circle(8)
    turtle.end_fill()
    turtle.pen(pen)
    if move_num is not None:
        turtle.write(move_num, align='center')


def draw_fuji(turtle, num_dominoes, cell_size=DEFAULT_CELL_SIZE):
    turtle.up()
    offset = (num_dominoes // 2 - 0.5) * cell_size
    turtle.forward(offset)
    turtle.right(90)
    turtle.forward(cell_size*0.5)
    turtle.left(90)
    turtle.down()
    for _ in range(3):
        draw_domino_outline(turtle, cell_size)
        turtle.up()
        turtle.right(90)
        turtle.forward(cell_size)
        turtle.left(90)
        turtle.down()
    turtle.up()
    turtle.back(offset)
    turtle.right(90)
    turtle.back(3*cell_size)
    turtle.left(90)


def draw_diagram(turtle,
                 state,
                 cell_size=DEFAULT_CELL_SIZE,
                 solution=False,
                 show_path=False,
                 board_class=Board):
    marks = {'>': partial(draw_arrow, turtle, cell_size),
             '^': partial(draw_arrow, turtle, cell_size, 90),
             '<': partial(draw_arrow, turtle, cell_size, 180),
             'v': partial(draw_arrow, turtle, cell_size, 270),
             '+': partial(draw_cross, turtle, cell_size, 0),
             '*': partial(draw_cross, turtle, cell_size, 45)}
    pos = turtle.pos()
    sections = state.split('\n---\n')
    lines = sections[0].splitlines()
    turtle.up()
    turtle.forward(cell_size*0.5)
    turtle.right(90)
    turtle.forward(cell_size*len(lines)*0.5)
    turtle.left(90)
    origin = turtle.pos()
    board = board_class.create(state)
    draw_board(turtle, board, cell_size)
    turtle.up()
    turtle.pencolor('white')
    for y, line in enumerate(reversed(lines)):
        for x, c in enumerate(line):
            if (x+y) % 2:
                mark = marks.get(c)
                if mark is not None:
                    mark()
                    turtle.up()
            turtle.forward(cell_size*.5)
        turtle.back(cell_size*len(line)*.5)
        turtle.left(90)
        turtle.forward(cell_size*.5)
        turtle.right(90)
    turtle.setpos(pos)
    draw_dominosa_hints(turtle, board, cell_size)
    draw_dice(turtle, board, cell_size)
    draw_arrows(turtle, board, cell_size)
    if show_path:
        draw_paths(turtle, board, cell_size)
    if solution:
        border = 1
        offset = [border, border]
        board = Board.create(state, border=border)
        for cell in board.findMatches():
            turtle.setpos(origin)
            draw_match(turtle,
                       cell_size,
                       offset,
                       cell)
        graph = CaptureBoardGraph()
        graph.walk(board)
        solution = graph.get_solution(return_partial=True)
        step_count = max(len(solution)-1, 1)
        for move_num, move in enumerate(solution, 1):
            domino_name = move[:2]
            for domino in board.dominoes:
                if domino.get_name() == domino_name:
                    dx, dy = Domino.get_direction(move[-1])
                    turtle.setpos(origin)
                    draw_move(turtle,
                              cell_size,
                              offset,
                              domino,
                              dx,
                              dy,
                              move_num,
                              step_count)
                    old_offset = offset[:]
                    state = graph.move(domino, dx, dy, offset)
                    new_board = Board.create(state, border=border)
                    captures = set(board.dominoes)
                    captures.difference_update(new_board.dominoes)
                    captures.discard(domino)
                    for capture in captures:
                        turtle.setpos(origin)
                        draw_capture_circle(turtle,
                                            cell_size,
                                            old_offset,
                                            capture,
                                            move_num)
                    offset[0] += border
                    offset[1] += border
                    board = new_board
                    break
        # Mark uncaptured dominoes
        for domino in board.dominoes:
            turtle.setpos(origin)
            draw_capture_circle(turtle, cell_size, offset, domino)
        turtle.setpos(pos)


def draw_dominosa_hints(turtle, board, cell_size):
    if not hasattr(board, 'get_pair_state'):
        return
    old_color = turtle.pencolor()
    old_size = turtle.pensize()
    turtle.pencolor('black')
    turtle.pensize(cell_size*0.05)
    turtle.up()

    # Draw splits between cells in the same row.
    for x in range(1, board.width):
        turtle.forward(cell_size)
        turtle.right(90)
        for y in reversed(range(board.height)):
            pair_state = board.get_pair_state(x-1, y, x, y)
            if pair_state != PairState.SPLIT:
                turtle.forward(cell_size)
            else:
                draw_split(turtle, cell_size)
        turtle.back(cell_size*board.height)
        turtle.left(90)
    turtle.back(cell_size*(board.width-1))

    # Draw splits between cells in the same column.
    turtle.right(90)
    for y in reversed(range(1, board.height)):
        turtle.forward(cell_size)
        turtle.left(90)
        for x in range(board.width):
            try:
                pair_state = board.get_pair_state(x, y-1, x, y)
            except KeyError:
                pair_state = PairState.UNDECIDED
            if pair_state != PairState.SPLIT:
                turtle.forward(cell_size)
            else:
                draw_split(turtle, cell_size)
        turtle.back(cell_size * board.width)
        turtle.right(90)
    turtle.back(cell_size*board.width)

    turtle.pencolor(old_color)
    turtle.pensize(old_size)


def draw_split(turtle, cell_size):
    turtle.forward(0.15 * cell_size)
    turtle.down()
    turtle.forward(0.7 * cell_size)
    turtle.up()
    turtle.forward(0.15 * cell_size)


def draw_joined_block(turtle, width, height):
    turtle.down()
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(height)
        turtle.right(90)
    turtle.end_fill()
    turtle.up()


def draw_dice(turtle: Turtle, board: Board, cell_size: int):
    dice_set = board.dice_set
    if dice_set is None:
        return
    turtle.color('black', 'white')
    turtle.right(90)
    turtle.forward(int(cell_size * (board.height-0.5)))
    turtle.left(90)
    turtle.forward(cell_size/2)
    die_size = cell_size * 0.6
    for y in range(board.height):
        for x in range(board.width):
            die_pips = dice_set[x, y]
            if die_pips is not None:
                draw_die_outline(turtle, die_size)
                cell = board[x][y]
                if cell is None or cell.domino is None:
                    dy = 0
                else:
                    dx, dy = cell.domino.direction
                if dy:
                    turtle.left(90)
                draw_pips(turtle, die_pips, die_size)
                if dy:
                    turtle.right(90)
            turtle.forward(cell_size)
        turtle.back(cell_size*board.width)
        turtle.left(90)
        turtle.forward(cell_size)
        turtle.right(90)
    turtle.right(90)
    turtle.forward(cell_size / 2)
    turtle.left(90)
    turtle.back(cell_size / 2)


def draw_arrows(turtle: Turtle, board: Board, cell_size: int):
    arrows = board.arrows
    if arrows is None:
        return
    start_pos = turtle.pos()
    turtle.up()
    line_width = cell_size * 0.05
    outline_width = cell_size * 0.07
    turtle.right(90)
    turtle.forward(cell_size * (board.height - 0.5))
    turtle.left(90)
    turtle.forward(cell_size / 2)
    x0, y0 = turtle.pos()

    for arrow in arrows.positions:
        for colour, width in (('white', outline_width),
                              ('grey50', line_width)):
            turtle.color(colour)
            x2, y2 = arrow[0]
            x = x0 + x2*cell_size
            y = y0 + y2*cell_size
            turtle.goto(x, y)
            turtle.down()
            # noinspection PyTypeChecker
            turtle.width(width)
            for x2, y2 in arrow[1:-1]:
                x = x0 + x2*cell_size
                y = y0 + y2*cell_size
                turtle.goto(x, y)
            x2, y2 = arrow[-1]
            x = x0 + x2*cell_size
            y = y0 + y2*cell_size
            turtle.setheading(turtle.towards(x, y))
            distance = max(abs(x - turtle.xcor()), abs(y - turtle.ycor()))
            turtle.forward(distance - line_width)
            turtle.up()
            turtle.forward(width + (width-line_width)/2)
            turtle.right(150)
            turtle.width(cell_size//100)
            turtle.down()
            turtle.begin_fill()
            for _ in range(3):
                turtle.forward(width*3)
                turtle.right(120)
            turtle.end_fill()
            turtle.up()
            turtle.goto(x0, y0)
            turtle.setheading(0)
    turtle.goto(start_pos)


def draw_demo(turtle):
    width = turtle.getscreen().window_width()
    height = turtle.getscreen().window_height()
    cell_size = min(width/8.2, height/7.2)
    turtle.up()
    turtle.back(cell_size*4)
    turtle.left(90)
    turtle.forward(cell_size*3.5)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor('ivory')
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(cell_size*8)
        turtle.right(90)
        turtle.forward(cell_size*7)
        turtle.right(90)
    turtle.end_fill()
    turtle.fillcolor('black')

    demo_state = """\
5 5 5 5 6 6 6 6
- - - - - - - -
1 2 3 4 4 3 2 1

1|2 3     0
    v     *
    4 5+6 6

2|2
---
(0,4)F,(4,1)G
"""
    mountain_state = """\
0|1 2|1 0|4

2 1|5 4|1 4
-         -
0 0|6 4|2 4

0|3 3|3 4|5

1 2 3|6 5|5
- -
3 2 1|6 5|6
"""
    dominosa_state = """\
0 1 2 3
  -
4 5 6 0

1|2 3 4
"""

    demo_type = 'demo'
    if demo_type == 'mountains':
        draw_diagram(turtle, mountain_state, cell_size, show_path=True)
    elif demo_type == 'dominosa':
        draw_diagram(turtle, dominosa_state, cell_size)
    else:
        draw_fuji(turtle, 8, cell_size)
        draw_diagram(turtle, demo_state, cell_size, solution=False)


if __name__ == '__live_coding__':
    from turtle import Turtle
    t = Turtle()
    draw_demo(t)
