from functools import partial
import math
from turtle import done, Turtle

from domino_puzzle import Board, CaptureBoardGraph, Domino

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


def draw_pips(turtle, pips, cell_size):
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


def draw_domino(turtle, domino, cell_size=50.0):
    turtle.up()
    turtle.back(cell_size*0.45)
    turtle.left(90)
    turtle.forward(cell_size*0.45)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor('white')
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(cell_size*1.9)
        turtle.right(90)
        turtle.forward(cell_size*.9)
        turtle.right(90)
    turtle.end_fill()

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


def draw_capture(turtle, cell_size):
    pos = turtle.pos()

    thickness = cell_size*.1
    length = cell_size*.15
    turtle.up()
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


def draw_diagram(turtle, state, cell_size, solution=False):
    marks = {'>': partial(draw_arrow, turtle, cell_size),
             '^': partial(draw_arrow, turtle, cell_size, 90),
             '<': partial(draw_arrow, turtle, cell_size, 180),
             'v': partial(draw_arrow, turtle, cell_size, 270),
             '*': partial(draw_capture, turtle, cell_size)}
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


def draw_demo(turtle):
    width = turtle.screen.window_width()
    height = turtle.screen.window_height()
    cell_size = min(width/8.5, height/7)
    turtle.up()
    turtle.back(width*.475)
    turtle.left(90)
    turtle.forward(height*0.4)
    turtle.right(90)
    turtle.down()
    turtle.fillcolor('ivory')
    turtle.begin_fill()
    for _ in range(2):
        turtle.forward(width*0.95)
        turtle.right(90)
        turtle.forward(height*0.8)
        turtle.right(90)
    turtle.end_fill()

    state1 = """\
3|6 2|0 2
        -
5 3 1|2 3
- -
3 1 4|3 6
        -
5|5 6|6 1
"""
    draw_diagram(turtle, state1, cell_size, solution=True)

    turtle.right(90)
    turtle.forward(cell_size*7)
    turtle.left(90)


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
