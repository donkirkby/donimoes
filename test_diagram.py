from diagram import draw_pips, draw_domino, draw_cell, draw_board, draw_paths, \
    draw_diagram, draw_fuji, draw_domino_outline
from domino_puzzle import Domino, Cell, Board
from svg_diagram import SvgDiagram

# noinspection PyUnresolvedReferences
from diagram_differ import drawing_differ


def test_draw_one_pip(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.left(90)
    t.forward(9)
    t.right(90)
    t.down()
    t.begin_fill()
    t.circle(-9.0)
    t.end_fill()

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


def test_draw_fuji(drawing_differ):
    expected = SvgDiagram()
    actual = SvgDiagram()

    t = expected.turtle
    t.up()
    t.goto(52.5, 97.5)
    draw_domino_outline(50, t)
    t.right(90)
    t.forward(50),
    t.left(90)
    draw_domino_outline(50, t)
    t.right(90)
    t.forward(50),
    t.left(90)
    draw_domino_outline(50, t)

    actual.turtle.up()
    actual.turtle.goto(0, 100)
    draw_fuji(actual.turtle, 4, 50)

    drawing_differ.assert_equal(actual, expected, 'draw_fuji')
