""" Generate images to use for a table on the playingcards.io web site. """
from pathlib import Path
from turtle import Turtle

from svg_diagram import SvgDiagram


class Tetromino:
    shape_name = '?'

    def __init__(self, t: Turtle, fill_colour: str = 'black', size: int = 40):
        self.t = t
        self.fill_colour = fill_colour
        self.size = size

    def prep(self):
        self.t.pensize(self.size//10)
        self.t.fillcolor(self.fill_colour)

    def draw(self):
        self.prep()
        self.t.begin_fill()
        self.draw_shape()
        self.t.end_fill()

    def draw_shape(self):
        pass


class TetrominoO(Tetromino):
    shape_name = 'o'

    def draw_shape(self):
        t = self.t
        for _ in range(4):
            t.forward(self.size*2)
            t.right(90)


class TetrominoL(Tetromino):
    shape_name = 'l'

    def draw_shape(self):
        t = self.t
        size = self.size
        t.forward(size*3)
        t.right(90)
        t.forward(size)
        t.right(90)
        t.forward(size*2)
        t.left(90)
        t.forward(size)
        t.right(90)
        t.forward(size)
        t.right(90)
        t.forward(size*2)
        t.right(90)


class TetrominoJ(Tetromino):
    shape_name = 'j'

    def draw_shape(self):
        t = self.t
        size = self.size
        t.forward(size*3)
        t.right(90)
        t.forward(size*2)
        t.right(90)
        t.forward(size)
        t.right(90)
        t.forward(size)
        t.left(90)
        t.forward(size*2)
        t.right(90)
        t.forward(size)
        t.right(90)


class TetrominoS(Tetromino):
    shape_name = 's'

    def draw_shape(self):
        t = self.t
        size = self.size
        t.end_fill()
        t.up()
        t.forward(size)
        t.begin_fill()
        t.down()
        for _ in range(2):
            t.forward(2*size)
            t.right(90)
            t.forward(size)
            t.right(90)
            t.forward(size)
            t.left(90)
            t.forward(size)
            t.right(90)
        t.end_fill()
        t.up()
        t.back(size)


class TetrominoZ(Tetromino):
    shape_name = 'z'

    def draw_shape(self):
        t = self.t
        size = self.size
        for _ in range(2):
            t.forward(size*2)
            t.right(90)
            t.forward(size)
            t.left(90)
            t.forward(size)
            t.right(90)
            t.forward(size)
            t.right(90)


class TetrominoT(Tetromino):
    shape_name = 't'

    def draw_shape(self):
        t = self.t
        size = self.size
        t.forward(size*3)
        t.right(90)
        t.forward(size)
        t.right(90)
        t.forward(size)
        t.left(90)
        t.forward(size)
        t.right(90)
        t.forward(size)
        t.right(90)
        t.forward(size)
        t.left(90)
        t.forward(size)
        t.right(90)
        t.forward(size)
        t.right(90)


class TetrominoI(Tetromino):
    shape_name = 'i'

    def draw_shape(self):
        t = self.t
        size = self.size
        for _ in range(2):
            t.forward(size*4)
            t.right(90)
            t.forward(size)
            t.right(90)


def demo():
    t = Turtle()
    white = 'darkgrey'
    t.up()
    size = 40
    t.back(size*13.5)
    t.down()
    TetrominoO(t, white).draw()
    t.up()
    t.forward(size*3)
    t.down()
    TetrominoL(t, white).draw()
    t.up()
    t.forward(size*4)
    t.down()
    TetrominoJ(t, white).draw()
    t.up()
    t.forward(size*4)
    t.down()
    TetrominoS(t, white).draw()
    t.up()
    t.forward(size*4)
    t.down()
    TetrominoZ(t, white).draw()
    t.up()
    t.forward(size*4)
    t.down()
    TetrominoT(t, white).draw()
    t.up()
    t.forward(size*4)
    t.down()
    TetrominoI(t, white).draw()


def main():
    out_path = Path('playing_cards_io')
    out_path.mkdir(exist_ok=True)
    shape_classes = [TetrominoT,
                     TetrominoZ,
                     TetrominoI,
                     TetrominoS,
                     TetrominoO,
                     TetrominoJ,
                     TetrominoL]
    for cls in shape_classes:
        for colour_name, colour_suffix in (('ivory', 'w'), ('darkgrey', 'b')):
            diagram = SvgDiagram('160', '80')
            diagram.turtle.up()
            diagram.turtle.goto(-78, 38)
            diagram.turtle.down()
            t = cls(diagram.turtle, fill_colour=colour_name, size=38)
            shape_name = t.shape_name
            t.draw()
            file_name = f'tetromino-{shape_name}{colour_suffix}.svg'
            diagram.svg_drawing.saveas(out_path / file_name)


if __name__ == '__main__':
    main()
else:
    demo()
