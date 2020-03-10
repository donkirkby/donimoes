from functools import partial
import math
from turtle import done, Turtle

from domino_puzzle import Board, CaptureBoardGraph, Domino, Cell

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


def draw_pips(turtle, pips, cell_size=DEFAULT_CELL_SIZE):
    turtle.fillcolor('black')
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


def draw_domino(turtle, domino, cell_size=DEFAULT_CELL_SIZE):
    turtle.up()
    turtle.back(cell_size * 0.45)
    turtle.left(90)
    turtle.forward(cell_size * 0.45)
    turtle.right(90)
    turtle.down()
    draw_domino_outline(cell_size, turtle)

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


def draw_domino_outline(cell_size, turtle):
    turtle.fillcolor('white')
    turtle.up()
    r = cell_size * 0.05
    turtle.forward(r)
    turtle.down()
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(cell_size * 1.8)
        turtle.circle(-r, 90)
        turtle.forward(cell_size * .8)
        turtle.circle(-r, 90)
    turtle.end_fill()

    turtle.up()
    turtle.back(r)


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
    pos = turtle.pos()
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
    offset = (num_dominoes // 2 - 0.95) * cell_size
    turtle.forward(offset)
    turtle.right(90)
    turtle.forward(cell_size*0.05)
    turtle.left(90)
    turtle.down()
    for _ in range(3):
        draw_domino_outline(cell_size, turtle)
        turtle.up()
        turtle.right(90)
        turtle.forward(cell_size)
        turtle.left(90)
        turtle.down()
    turtle.up()
    turtle.back(offset)
    turtle.right(90)
    turtle.back(2.55*cell_size)
    turtle.left(90)


def draw_diagram(turtle,
                 state,
                 cell_size=DEFAULT_CELL_SIZE,
                 solution=False,
                 show_path=False):
    marks = {'>': partial(draw_arrow, turtle, cell_size),
             '^': partial(draw_arrow, turtle, cell_size, 90),
             '<': partial(draw_arrow, turtle, cell_size, 180),
             'v': partial(draw_arrow, turtle, cell_size, 270),
             '+': partial(draw_cross, turtle, cell_size, 0),
             '*': partial(draw_cross, turtle, cell_size, 45)}
    pos = turtle.pos()
    lines = state.splitlines()
    turtle.up()
    turtle.forward(cell_size*0.5)
    turtle.right(90)
    turtle.forward(cell_size*len(lines)*0.5)
    turtle.left(90)
    origin = turtle.pos()
    board = Board.create(state)
    draw_board(turtle, board, cell_size)
    turtle.up()
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


def draw_blocks(turtle: Turtle, state: str, cell_size: float):
    turtle.up()
    margin = cell_size / 20
    old_pos = turtle.pos()
    old_colour = turtle.color()
    turtle.color('black')
    turtle.forward(margin)
    turtle.right(90)
    turtle.forward(margin)
    turtle.left(90)
    lines = state.splitlines()
    lines.append('')
    for i, line in enumerate(lines[:-1]):
        below_line = lines[i + 1]
        for j, c in enumerate(line):
            right_neighbour = line[j+1:j+2]
            below_neighbour = below_line[j:j+1]
            diagonal_neighbour = below_line[j+1:j+2]
            if c == '#' and right_neighbour == '#':
                draw_joined_block(turtle,
                                  2 * (cell_size-margin),
                                  cell_size - 2*margin)
            if c == '#' and below_neighbour == '#':
                draw_joined_block(turtle,
                                  cell_size - 2 * margin,
                                  2 * (cell_size - margin))
            if ''.join((c,
                        right_neighbour,
                        below_neighbour,
                        diagonal_neighbour)) == '####':
                draw_joined_block(turtle,
                                  2 * (cell_size - margin),
                                  2 * (cell_size - margin))
            turtle.forward(cell_size)
        turtle.back(cell_size*len(line))
        turtle.right(90)
        turtle.forward(cell_size)
        turtle.left(90)

    turtle.color(old_colour)
    turtle.setpos(old_pos)


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


def draw_demo(turtle):
    width = turtle.screen.window_width()
    height = turtle.screen.window_height()
    cell_size = min(width/8.2, height/7.2)
    turtle.up()
    turtle.back(cell_size*4)
    turtle.left(90)
    turtle.forward(cell_size*3.5)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor('white')
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(cell_size*8)
        turtle.right(90)
        turtle.forward(cell_size*7)
        turtle.right(90)
    turtle.end_fill()

    demo_state = """\
5 5 5 5 6 6 6 6
- - - - - - - -
1 2 3 4 4 3 2 1

1|2 3     0
    v     *
    4 5+6 6

2|2
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
    blocks_state = """\
### ###
  #  #

##  ##
 ## ##
"""
    dominosa_state = """\
0 1 2 3
  -
4 5 6 0

1|2 3 4
"""

    demo_type = 'dominosa'
    if demo_type == 'mountains':
        draw_diagram(turtle, mountain_state, cell_size, show_path=True)
    elif demo_type == 'blocks':
        draw_blocks(turtle, blocks_state, cell_size)
    elif demo_type == 'dominosa':
        draw_diagram(turtle, dominosa_state, cell_size)
    else:
        draw_fuji(turtle, 8, cell_size)
        draw_diagram(turtle, demo_state, cell_size, solution=False)


if __name__ in ('__main__', '__live_coding__'):
    t = Turtle()
    try:
        t.screen.tracer(0)
    except AttributeError:
        pass
    draw_demo(t)
    try:
        t.screen.update()
    except AttributeError:
        pass
    done()
