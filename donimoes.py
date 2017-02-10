from subprocess import call

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Flowable, Spacer, KeepTogether,\
    ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ListStyle
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize  # @UnresolvedImport

from diagram import draw_diagram
from pdf_turtle import PdfTurtle
from book_parser import parse, Styles

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


class Diagram(Flowable):
    MAX_COLUMN_COUNT = 16

    def __init__(self, board_state):
        self.board_state = board_state
        lines = board_state.splitlines(True)
        self.row_count = (len(lines) + 1)/2
        self.col_count = max(map(len, lines))/2

    def wrap(self, availWidth, availHeight):
        self.cell_size = availWidth / Diagram.MAX_COLUMN_COUNT
        self.width = self.cell_size * self.col_count
        self.height = self.cell_size * self.row_count
        return (self.width, self.height)

    def draw(self):
        t = PdfTurtle(self.canv, self._frame, self.width, self.height)
        t.up()
        t.back(self.width/2)
        t.left(90)
        t.forward(self.height/2)
        t.right(90)
        t.down()
        try:
            draw_diagram(t, self.board_state, self.cell_size)
        except:
            print(self.board_state)
            raise


def firstPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(PAGE_WIDTH/2,
                             0.75 * inch,
                             "donkirkby.github.com/donimoes")
    canvas.restoreState()


def go():
    doc = SimpleDocTemplate("donimoes.pdf")
    styles = getSampleStyleSheet()
    paragraph_style = styles[Styles.Normal]
    list_style = ListStyle('default_list',
                           bulletFontSize=paragraph_style.fontSize,
                           bulletFormat='%s.')
    story = []
    f = open('rules.md')
    group = []
    bulleted = []
    first_bullet = None
    states = parse(f.read())
    for state in states:
        if state.style == Styles.Diagram:
            flowable = Diagram(state.text)
        else:
            flowable = Paragraph(state.text,
                                 styles[state.style])
        if state.style.startswith(Styles.Heading):
            group.append(flowable)
        elif state.bullet:
            bulleted.append(flowable)
            first_bullet = first_bullet or state.bullet
        else:
            if bulleted:
                story.append(ListFlowable(bulleted,
                                          style=list_style,
                                          start=first_bullet))
                bulleted = []
                first_bullet = None
                story.append(Spacer(1, 0.055*inch))
            if not group:
                story.append(flowable)
            else:
                group.append(flowable)
                story.append(KeepTogether(group))
                group = []
            story.append(Spacer(1, 0.055*inch))
    if bulleted:
        story.append(ListFlowable(bulleted,
                                  style=list_style,
                                  start=first_bullet))
    doc.build(story, onFirstPage=firstPage)

if __name__ == '__main__':
    go()

    call(["evince", "donimoes.pdf"])
