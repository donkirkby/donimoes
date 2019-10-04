from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
from pathlib import Path
from subprocess import call

from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Flowable, Spacer, KeepTogether,\
    ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ListStyle
from reportlab.lib.units import inch
# noinspection PyUnresolvedReferences
from reportlab.rl_config import defaultPageSize

from diagram import draw_diagram
from domino_puzzle import BoardError
from pdf_turtle import PdfTurtle
from book_parser import parse, Styles

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


def parse_args():
    default_markdown = str(Path(__file__).parent / 'docs' / 'rules.md')
    parser = ArgumentParser(description='Convert rules markdown into a PDF.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('markdown',
                        type=FileType(),
                        nargs='?',
                        default=default_markdown,
                        help='markdown source file to convert')
    return parser.parse_args()


class Diagram(Flowable):
    MAX_COLUMN_COUNT = 16

    def __init__(self, board_state):
        super().__init__()
        self.board_state = board_state
        lines = board_state.splitlines(True)
        self.row_count = (len(lines) + 1)/2
        self.col_count = max(map(len, lines))/2
        self.cell_size = None

    def wrap(self, avail_width, avail_height):
        self.cell_size = avail_width / Diagram.MAX_COLUMN_COUNT
        self.width = self.cell_size * self.col_count
        self.height = self.cell_size * self.row_count
        return self.width, self.height

    def draw(self):
        # noinspection PyUnresolvedReferences
        t = PdfTurtle(self.canv, self._frame, self.width, self.height)
        t.up()
        t.back(self.width/2)
        t.left(90)
        t.forward(self.height/2)
        t.right(90)
        t.down()
        try:
            draw_diagram(t, self.board_state, self.cell_size)
        except BoardError:
            print(self.board_state)
            raise


# noinspection PyUnusedLocal
def first_page(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawCentredString(PAGE_WIDTH/2,
                             0.75 * inch,
                             "donkirkby.github.com/donimoes")
    canvas.restoreState()


def main():
    args = parse_args()
    markdown_path = Path(args.markdown.name)
    pdf_stem = markdown_path.stem
    if pdf_stem == 'rules':
        pdf_stem = 'donimoes'
    pdf_path = markdown_path.parent / (pdf_stem + '.pdf')
    with args.markdown:
        states = parse(args.markdown.read())

    doc = SimpleDocTemplate(str(pdf_path),
                            author='Don Kirkby',
                            pagesize=pagesizes.letter,
                            topMargin=0.625*inch,
                            bottomMargin=0.625*inch)
    styles = getSampleStyleSheet()
    paragraph_style = styles[Styles.Normal]
    list_style = ListStyle('default_list',
                           bulletFontSize=paragraph_style.fontSize,
                           bulletFormat='%s.')
    story = []
    group = []
    bulleted = []
    first_bullet = None
    for state in states:
        if state.style == Styles.Metadata:
            doc.title = state.text
            continue
        elif state.style == Styles.Diagram:
            flowable = Diagram(state.text)
        else:
            flowable = Paragraph(state.text,
                                 styles[state.style])
        if state.style.startswith(Styles.Heading):
            if bulleted:
                group.append(ListFlowable(bulleted,
                                          style=list_style,
                                          start=first_bullet))
                story.append(KeepTogether(group))
                group = []
                bulleted = []
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
    doc.build(story, onFirstPage=first_page)

    call(["evince", pdf_path])


if __name__ == '__main__':
    main()
