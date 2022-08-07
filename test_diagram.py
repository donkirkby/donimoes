from diagram import draw_pips, draw_domino, draw_cell, draw_board, draw_paths, \
    draw_diagram, draw_fuji, draw_domino_outline, draw_arrow, draw_die_outline
from domino_puzzle import Domino, Cell, Board
from svg_diagram import SvgDiagram

# noinspection PyUnresolvedReferences
from diagram_differ import drawing_differ, session_drawing_differ


def test_draw_one_pip(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.dot(18)

    draw_pips(actual.turtle, 1)

    drawing_differ.assert_equal(actual, expected, 'draw_one_pip')


def test_two_pips(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.back(27)
    t.left(90)
    t.forward(27)
    t.right(90)
    draw_pips(t, 1)
    t.forward(54)
    t.right(90)
    t.forward(54)
    t.left(90)
    draw_pips(t, 1)

    draw_pips(actual.turtle, 2)

    drawing_differ.assert_equal(actual, expected, 'two_pips')


def test_draw_domino(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    start_pos = t.pos()

    # Outline
    t.up()
    t.back(40)
    t.left(90)
    t.forward(45)
    t.right(90)
    t.fillcolor('white')
    t.begin_fill()
    t.down()
    for _ in range(2):
        t.forward(180)
        t.circle(-5, 90)
        t.forward(80)
        t.circle(-5, 90)
    t.end_fill()

    # Pips
    t.up()
    t.goto(start_pos)
    draw_pips(t, 1)
    t.forward(100)
    draw_pips(t, 2)

    # Divider
    t.back(50)
    t.right(90)
    t.back(35)
    t.down()
    t.forward(70)

    draw_domino(actual.turtle, Domino(1, 2))

    drawing_differ.assert_equal(actual, expected, 'draw_domino')


def test_draw_cell(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.back(45)
    t.left(90)
    t.forward(45)
    t.right(90)
    t.fillcolor('white')
    t.pencolor('light grey')
    t.begin_fill()
    for _ in range(4):
        t.forward(10)
        t.down()
        t.forward(70)
        t.up()
        t.forward(10)
        t.right(90)
    t.end_fill()
    t.forward(45)
    t.right(90)
    t.forward(45)
    t.left(90)
    t.pencolor('black')
    draw_pips(t, 2)

    draw_cell(actual.turtle, Cell(2))

    drawing_differ.assert_equal(actual, expected, 'draw_cell')


def test_draw_board(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(0, 50)
    draw_domino(t, Domino(1, 2))
    t.goto(0, -50)
    draw_domino(t, Domino(3, 4))

    board = Board.create("""\
1|2

3|4
""")
    actual.turtle.up()
    actual.turtle.goto(0, -50)
    draw_board(actual.turtle, board)

    drawing_differ.assert_equal(actual, expected, 'draw_board')


def test_draw_paths(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(0, -50)
    draw_domino(t, Domino(3, 0))
    t.left(90)
    t.forward(100)
    t.right(90)
    draw_domino(t, Domino(2, 2))
    t.right(90)
    t.forward(100)
    t.left(90)
    t.down()
    t.left(90)
    t.pencolor('grey')
    t.width(2)
    t.down()
    t.forward(100)
    t.right(90)
    t.forward(100)

    board = Board.create("""\
2|2

3|0
""")
    actual.turtle.up()
    actual.turtle.goto(0, -50)
    draw_board(actual.turtle, board)
    actual.turtle.goto(-50, 100)
    draw_paths(actual.turtle, board)

    drawing_differ.assert_equal(actual, expected, 'draw_paths')


# noinspection DuplicatedCode
def test_draw_arrow(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(50, -50)
    draw_domino(t, Domino(1, 2))
    t.forward(30)
    t.left(90)
    t.down()
    t.pencolor('white')
    t.begin_fill()
    t.forward(5)
    t.right(90)
    t.forward(30)
    t.left(90)
    t.forward(10)
    t.right(120)
    t.forward(30)
    t.right(120)
    t.forward(30)
    t.right(120)
    t.forward(10)
    t.left(90)
    t.forward(30)
    t.right(90)
    t.forward(5)
    t.end_fill()

    draw_diagram(actual.turtle, "1>2")

    drawing_differ.assert_equal(actual, expected, 'draw_arrow')


# noinspection DuplicatedCode
def test_draw_cross(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(50, -50)
    draw_domino(t, Domino(1, 2))
    t.forward(30)
    t.left(90)
    t.back(5)
    t.down()
    t.pencolor('white')
    t.begin_fill()
    for _ in range(4):
        t.forward(10)
        t.right(90)
        t.forward(15)
        t.left(90)
        t.forward(15)
        t.right(90)
    t.end_fill()

    draw_diagram(actual.turtle, "1+2")

    drawing_differ.assert_equal(actual, expected, 'draw_cross')


# noinspection DuplicatedCode
def test_draw_marker(drawing_differ):
    state = """\
1|P
---
P2
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(50, -50)
    draw_domino(t, Domino(1, 2))
    t.forward(100)
    t.left(90)
    t.down()
    t.dot(75)

    t.up()
    t.back(5)
    t.color('white')
    t.write('P', align='center', font=('Arial', 20, 'normal'))
    t.fillcolor('white')
    t.back(10)
    t.right(90)
    draw_pips(t, 2, 30)
    t.forward(25)

    draw_diagram(actual.turtle, state)

    drawing_differ.assert_equal(actual, expected, 'draw_marker')


# noinspection DuplicatedCode
def test_draw_black_marker(drawing_differ):
    state = """\
1|b
---
b2
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(50, -50)
    draw_domino(t, Domino(1, 2))
    t.forward(100)
    t.left(90)
    t.down()
    t.dot(75)

    t.up()
    t.back(5)
    t.color('white')
    t.fillcolor('white')
    t.back(10)
    t.right(90)
    draw_pips(t, 2, 30)
    t.forward(25)

    draw_diagram(actual.turtle, state)

    drawing_differ.assert_equal(actual, expected, 'draw_black_marker')


# noinspection DuplicatedCode
def test_draw_white_marker(drawing_differ):
    state = """\
1|w
---
w2
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(50, -50)
    draw_domino(t, Domino(1, 2))
    t.forward(100)
    t.left(90)
    t.down()
    t.dot(75)
    t.color('white')
    t.dot(70)

    t.up()
    t.back(5)
    t.color('black')
    t.back(10)
    t.right(90)
    draw_pips(t, 2, 30)
    t.forward(25)

    draw_diagram(actual.turtle, state)

    drawing_differ.assert_equal(actual, expected, 'draw_white_marker')


# noinspection DuplicatedCode
def test_draw_marker_with_arrow(drawing_differ):
    state = """\
1>P
---
P2
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(50, -50)
    draw_domino(t, Domino(1, 2))
    t.forward(100)
    t.left(90)
    t.down()
    t.dot(75)
    t.color('black')

    t.up()
    t.back(5)
    t.color('white')
    t.write('P', align='center', font=('Arial', 20, 'normal'))
    t.fillcolor('white')
    t.back(10)
    t.right(90)
    draw_pips(t, 2, 30)
    t.back(50)
    t.left(90)
    t.forward(15)
    t.right(90)
    t.fillcolor('black')
    draw_arrow(t, 100)

    draw_diagram(actual.turtle, state)

    drawing_differ.assert_equal(actual, expected, 'draw_marker_with_arrow')


# noinspection DuplicatedCode
def test_draw_marker_beside_domino(drawing_differ):
    state = """\
1|2

x x

---
(0,0)A
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(-50, 50)
    draw_domino(t, Domino(1, 2))
    t.right(90)
    t.forward(100)
    t.down()
    t.dot(75)

    t.up()
    t.forward(5)
    t.color('white')
    t.write('A', align='center', font=('Arial', 20, 'normal'))

    actual.turtle.up()
    actual.turtle.goto(-100, 100)
    draw_diagram(actual.turtle, state)

    drawing_differ.assert_equal(actual, expected, 'draw_marker_beside_domino')


def test_draw_fuji(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(75, 75)
    draw_domino_outline(t, 50)
    t.right(90)
    t.forward(50),
    t.left(90)
    draw_domino_outline(t, 50)
    t.right(90)
    t.forward(50),
    t.left(90)
    draw_domino_outline(t, 50)

    actual.turtle.up()
    actual.turtle.goto(0, 100)
    draw_fuji(actual.turtle, 4, 50)

    drawing_differ.assert_equal(actual, expected, 'draw_fuji')


def test_draw_sniff(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(150, -50)
    t.left(90)
    draw_domino(t, Domino(2, 2))
    t.forward(50)
    t.right(90)
    t.back(200)
    draw_domino(t, Domino(5, 2))

    actual.turtle.up()
    actual.turtle.goto(-100, 100)
    draw_diagram(actual.turtle, """\
    2
5|2 -
    2
""")

    drawing_differ.assert_equal(actual, expected, 'draw_sniff')


def test_draw_tetromino(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(0, -50)
    draw_domino_outline(t, fill='black', margin=0)
    t.left(90)
    draw_domino_outline(t, fill='black', margin=0)
    t.forward(100)
    t.left(90)
    draw_domino_outline(t, fill='black', margin=0)

    actual.turtle.up()
    actual.turtle.goto(-150, 100)
    draw_diagram(actual.turtle, """\
#|#
  -
  #|#
""")

    drawing_differ.assert_equal(actual, expected, 'draw_tetromino')


# noinspection DuplicatedCode
def test_dice_diagram(drawing_differ):
    state = """\
1|2 3
    -
6|5 4
---
dice:(2,1)3,(0,0)6
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(-50, -50)
    draw_domino(t, Domino(6, 5))

    t.back(30)
    t.left(90)
    t.forward(25)
    t.down()
    t.fillcolor('white')
    t.begin_fill()
    for _ in range(4):
        t.circle(-5, 90)
        t.forward(50)
    t.end_fill()

    t.up()
    t.back(25)
    t.right(90)
    t.forward(30)
    draw_pips(t, 6, 60)

    t.forward(200)
    t.left(90)
    draw_domino(t, Domino(4, 3))

    t.forward(100)
    t.back(30)
    t.left(90)
    t.forward(25)
    t.down()
    t.fillcolor('white')
    t.begin_fill()
    for _ in range(4):
        t.circle(-5, 90)
        t.forward(50)
    t.end_fill()

    t.up()
    t.back(25)
    t.right(90)
    t.forward(30)
    draw_pips(t, 3, 60)

    t.left(90)
    t.forward(100)
    draw_domino(t, Domino(2, 1))

    t = actual.turtle
    t.up()
    t.goto(-100, 100)
    draw_diagram(actual.turtle, state)

    drawing_differ.tolerance = 10
    drawing_differ.assert_equal(actual, expected, 'draw_dice')


# noinspection DuplicatedCode
def test_arrows_diagram(drawing_differ):
    state = """\
4|2 3
    -
6|5 4
---
dice:(2,0)4,(2,1)3
arrows:(0,1)R2D1
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(-50, -50)
    draw_domino(t, Domino(6, 5))

    t.forward(200)
    t.left(90)
    draw_domino(t, Domino(4, 3))

    draw_die_outline(t, 60)
    draw_pips(t, 4, 60)

    t.forward(100)
    draw_die_outline(t, 60)
    draw_pips(t, 3, 60)

    t.left(90)
    t.forward(100)
    draw_domino(t, Domino(2, 4))
    t.forward(100)
    t.right(180)

    pos = t.pos()
    heading = t.heading()
    t.width(7)
    t.color('white')
    t.down()
    t.forward(200)
    t.right(90)
    t.forward(95)
    t.up()
    t.width(1)
    t.forward(8)
    t.right(150)
    t.down()
    t.begin_fill()
    for _ in range(3):
        t.forward(21)
        t.right(120)
    t.end_fill()

    t.up()
    t.goto(pos)
    t.setheading(heading)
    t.width(5)
    t.color('grey50')
    t.down()
    t.forward(200)
    t.right(90)
    t.forward(95)
    t.up()
    t.width(1)
    t.forward(5)
    t.right(150)
    t.down()
    t.begin_fill()
    for _ in range(3):
        t.forward(15)
        t.right(120)
    t.end_fill()

    t = actual.turtle
    t.up()
    t.goto(-100, 100)
    draw_diagram(actual.turtle, state)

    drawing_differ.tolerance = 10
    drawing_differ.assert_equal(actual, expected, 'draw_arrows')


# noinspection DuplicatedCode
def test_arrows_and_marker(drawing_differ):
    state = """\
4|2 3
    -
6|5 4
---
(2,0)B,(2,1)W
arrows:(0,1)R2D1
"""
    expected = SvgDiagram(500, 250)
    actual = SvgDiagram(500, 250)

    t = expected.turtle
    t.up()
    t.goto(-50, -50)
    draw_domino(t, Domino(6, 5))

    t.forward(200)
    t.left(90)
    draw_domino(t, Domino(4, 3))

    t.dot(75)
    t.color('white')
    t.back(5)
    t.write('B',
            align='center',
            font=('Arial', 20, 'normal'))
    t.back(10)
    draw_pips(t, 4, 30)
    t.forward(15)
    t.color('black')

    t.forward(100)
    t.dot(75)
    t.color('white')
    t.back(5)
    t.write('W',
            align='center',
            font=('Arial', 20, 'normal'))
    t.back(10)
    draw_pips(t, 3, 30)
    t.forward(15)
    t.color('black')

    t.left(90)
    t.forward(100)
    draw_domino(t, Domino(2, 4))
    t.forward(100)
    t.right(180)

    pos = t.pos()
    heading = t.heading()
    t.width(7)
    t.color('white')
    t.down()
    t.forward(200)
    t.right(90)
    t.forward(95)
    t.up()
    t.width(1)
    t.forward(8)
    t.right(150)
    t.down()
    t.begin_fill()
    for _ in range(3):
        t.forward(21)
        t.right(120)
    t.end_fill()

    t.up()
    t.goto(pos)
    t.setheading(heading)

    t.width(5)
    t.color('grey50')
    t.down()
    t.forward(200)
    t.right(90)
    t.forward(95)
    t.up()
    t.width(1)
    t.forward(5)
    t.right(150)
    t.down()
    t.begin_fill()
    for _ in range(3):
        t.forward(15)
        t.right(120)
    t.end_fill()

    t = actual.turtle
    t.up()
    t.goto(-100, 100)
    draw_diagram(actual.turtle, state)

    drawing_differ.tolerance = 10
    drawing_differ.assert_equal(actual, expected, 'draw_arrows_and_marker')
