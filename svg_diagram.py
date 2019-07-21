from turtle import *  # @UnusedWildImport

import svgwrite

from diagram import draw_diagram
from svg_turtle import SvgTurtle


def draw_page(turtle):
    state = """\
5 2|4   5 2|4     5 2|4   5 2*4
-       -         -       *
2 2|6   2   2>6   2 2<6   2 2*6
"""
    lines = state.splitlines()
    row_count = (len(lines) + 1) // 2
    column_count = (max(len(line) for line in lines) + 1) // 2
    width = turtle.screen.window_width()
    height = turtle.screen.window_height()
    cell_size = min(width/column_count, height/row_count)
    turtle.up()
    turtle.back(cell_size*column_count/2)
    turtle.right(90)
    turtle.back(cell_size*row_count/2)
    turtle.left(90)

    draw_diagram(turtle, state, cell_size)


def write_file(draw_func, filename, size):
    drawing = svgwrite.Drawing(filename, size=size)
    drawing.add(drawing.rect(fill='white', size=("100%", "100%")))
    t = SvgTurtle(drawing)
    Turtle._screen = t.screen
    Turtle._pen = t
    draw_func(t)
    drawing.save()


def main():
    write_file(draw_page, 'diagram.svg', size=("500px", "500px"))
    print('Done.')


if __name__ == '__main__':
    main()
