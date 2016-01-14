
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
    from domino_puzzle import Domino
    turtle = __live_turtle__  # @UndefinedVariable
    cell_size = 75
    turtle.up()
    turtle.back(100)
    turtle.left(90)
    turtle.forward(100)
    turtle.down()
    domino1 = Domino(5, 2)
    draw_domino(turtle, domino1, cell_size)

    turtle.up()
    turtle.right(90)
    turtle.forward(cell_size)
    domino2 = Domino(1, 6)
    draw_domino(turtle, domino2, cell_size)

    turtle.up()
    turtle.left(90)
    turtle.forward(cell_size)
    turtle.right(90)
    domino3 = Domino(0, 4)
    draw_domino(turtle, domino3, cell_size)

    turtle.right(90)
    turtle.forward(cell_size*2)
    turtle.left(90)
    turtle.back(cell_size)

    draw_position(turtle)
