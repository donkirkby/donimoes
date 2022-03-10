# hello_reportlab.py
import typing

from reportlab.graphics import renderPM, renderPDF
from reportlab.graphics.renderPM import PMCanvas
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import Color
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import inch
from space_tracer import LivePillowImage

PAGE_SIZE = (9.031*inch, 7.215*inch)


def draw() -> Drawing:
    total_width, total_height = PAGE_SIZE
    drawing = Drawing(total_width, total_height)
    bleed = 0.125 * inch
    margin = 0.5 * inch
    spine = 0.281 * inch
    drawing.add(Rect((total_width + spine) / 2, 0,
                     (total_width - spine) / 2, total_height,
                     fillColor=Color(0, .75, 0),
                     strokeColor=None))
    # canvas.setFont('Helvetica', 16)
    # canvas.drawString(100, 100, "Welcome to Reportlab!")
    return drawing


def live_main():
    total_width, total_height = PAGE_SIZE
    drawing = draw()
    pil = renderPM.drawToPIL(drawing, bg=0x999999)
    image = LivePillowImage(pil)
    image.display((-total_width/2, total_height/2))


def main():
    drawing = draw()
    renderPDF.drawToFile(drawing, "cover.pdf")


if __name__ == '__main__':
    main()
elif __name__ == '__live_coding__':
    live_main()
