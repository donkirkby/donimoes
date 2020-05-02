from reportlab.graphics.renderPM import drawToFile

from svg_diagram import SvgDiagram, draw_page


def main():
    diagram = SvgDiagram(width="600", height="500")
    draw_page(diagram.turtle)
    drawing = diagram.to_reportlab()
    drawToFile(drawing, 'diagram.png', 'PNG')
    print('Done.')


if __name__ == '__main__':
    main()
