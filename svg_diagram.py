from io import BytesIO

import svgwrite
import reportlab.graphics.shapes as reportlab_shapes
from reportlab.graphics.renderPM import drawToFile
from svglib.svglib import svg2rlg

from diagram import draw_diagram
from svg_turtle import SvgTurtle


class SvgDiagram:
    def __init__(self, width="400px", height="250px"):
        if not isinstance(width, str):
            width = f'{width}px'
        if not isinstance(height, str):
            height = f'{height}px'
        self.svg_drawing = svgwrite.Drawing(size=(width, height))
        self.turtle = SvgTurtle(self.svg_drawing)

    def to_reportlab(self) -> reportlab_shapes.Drawing:
        svg_text = self.turtle.to_svg()
        svg_bytes = svg_text.encode()
        drawing = svg2rlg(BytesIO(svg_bytes))
        return drawing


def draw_page(turtle, state):
    lines = state.split('\n---\n')[0].splitlines()
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


def main():
    state = """\
0 1 4 3 1 2 4|6
- - - - - -
1 4 3 1 2 4 0|6

0|3 2|5 5|5 5|1

3|6 0|2 2|6 6|1

6|5 6|6 0|4 3|3

5 2 0|0 4|4 2|2
- -
3 3 1|1 0|5 5|4
"""
    # cell size of 60 looks good on puzzling.se.
    diagram = SvgDiagram('480', '420')
    diagram.svg_drawing.add(
        diagram.svg_drawing.rect(fill='white', size=("100%", "100%")))
    draw_page(diagram.turtle, state)
    is_svg = False
    if is_svg:
        diagram.svg_drawing.saveas('diagram.svg')
    else:
        drawing = diagram.to_reportlab()
        drawToFile(drawing, 'docs/images/example.png', 'PNG')
    print('Done.')


if __name__ == '__main__':
    main()
