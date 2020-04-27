from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
from functools import partial
from pathlib import Path
from subprocess import call

from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.flowables import Spacer, KeepTogether, ListFlowable
from reportlab.lib.styles import getSampleStyleSheet, ListStyle
from reportlab.lib.units import inch
# noinspection PyUnresolvedReferences
from reportlab.rl_config import defaultPageSize

from diagram import draw_diagram, draw_fuji
from domino_puzzle import BoardError
from footer import FooterCanvas
from book_parser import parse, Styles
from svg_diagram import SvgDiagram

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


def parse_args():
    default_markdown = str(Path(__file__).parent / 'docs' / 'rules.md')
    # noinspection PyTypeChecker
    parser = ArgumentParser(description='Convert rules markdown into a PDF.',
                            formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--booklet',
                        action='store_true',
                        help='Reorder pages for printing as a folded booklet.')
    parser.add_argument('markdown',
                        type=FileType(),
                        nargs='?',
                        default=default_markdown,
                        help='markdown source file to convert')
    return parser.parse_args()


class Diagram:
    MAX_COLUMN_COUNT = 14

    def __init__(self, page_width, page_height, board_state, show_path=False):
        self.page_width = page_width
        self.page_height = page_height
        self.board_state = board_state
        self.show_path = show_path
        lines = board_state.splitlines(True)
        self.row_count = (len(lines) + 1)/2
        self.col_count = max(map(len, lines))/2
        self.cell_size = self.page_width / Diagram.MAX_COLUMN_COUNT
        self.width = self.cell_size * self.col_count
        self.height = self.cell_size * self.row_count
        self.resize()

    def resize(self):
        pass

    def build(self):
        diagram = SvgDiagram(self.width, self.height)
        t = diagram.turtle
        t.up()
        t.back(self.width/2)
        t.left(90)
        t.forward(self.height/2)
        t.right(90)
        t.down()
        self.draw_background(t)
        self.draw_foreground(t)
        return diagram.to_reportlab()

    def draw_foreground(self, t):
        try:
            draw_diagram(t,
                         self.board_state,
                         self.cell_size,
                         show_path=self.show_path)
        except BoardError:
            print(self.board_state)
            raise

    def draw_background(self, t):
        """ Draw background items to appear behind the regular dominoes. """
        pass


class FujisanDiagram(Diagram):
    def draw_background(self, t):
        draw_fuji(t, self.col_count, self.cell_size)

    def resize(self):
        self.height += self.cell_size


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
    if args.booklet:
        for style in styles.byName.values():
            if hasattr(style, 'fontSize'):
                if style.name.startswith('Heading'):
                    scale = 1.5
                else:
                    scale = 2
                style.fontSize *= scale
                style.leading *= scale
    paragraph_style = styles[Styles.Normal]
    numbered_list_style = ListStyle('default_list',
                                    bulletFontSize=paragraph_style.fontSize,
                                    leftIndent=paragraph_style.fontSize*1.5,
                                    bulletFormat='%s.')
    bulleted_list_style = ListStyle('default_list',
                                    bulletFontSize=paragraph_style.fontSize,
                                    leftIndent=paragraph_style.fontSize*1.5)
    story = []
    group = []
    bulleted = []
    headings = []
    first_bullet = None
    for state in states:
        if state.style == Styles.Metadata:
            doc.title = state.text
            continue
        elif state.style == Styles.Diagram:
            if 'Fujisan' in headings or 'Fujisan Problems' in headings:
                flowable = FujisanDiagram(doc.width,
                                          doc.height,
                                          state.text).build()
            else:
                if 'Mountains and Valleys' in headings:
                    diagram_width = (len(state.text.splitlines()[0]) + 1)//2
                    show_path = diagram_width == 6
                else:
                    show_path = False
                flowable = Diagram(doc.width,
                                   doc.height,
                                   state.text,
                                   show_path).build()
                if show_path:
                    group.append(flowable)
                    flowable = Paragraph(
                        'The grey lines show the paths you can walk along.',
                        styles[Styles.Normal])
        else:
            flowable = Paragraph(state.text,
                                 styles[state.style])
        if state.style.startswith(Styles.Heading):
            if bulleted:
                create_list_flowable(bulleted,
                                     group,
                                     story,
                                     first_bullet,
                                     bulleted_list_style,
                                     numbered_list_style)
                group = []
                bulleted = []
                first_bullet = None
            group.append(flowable)
            heading_level = int(state.style[-1])
            headings = headings[:heading_level]
            while len(headings) < heading_level:
                headings.append(None)
            headings[heading_level - 1] = state.text
        elif state.bullet:
            bulleted.append(flowable)
            first_bullet = first_bullet or state.bullet
        else:
            if bulleted:
                create_list_flowable(bulleted,
                                     group,
                                     story,
                                     first_bullet,
                                     bulleted_list_style,
                                     numbered_list_style)
                group = []
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
        create_list_flowable(bulleted,
                             group,
                             story,
                             first_bullet,
                             bulleted_list_style,
                             numbered_list_style)
    doc.build(story, canvasmaker=partial(FooterCanvas, is_booklet=args.booklet))

    call(["evince", pdf_path])


def create_list_flowable(bulleted,
                         group,
                         story,
                         first_bullet,
                         bulleted_list_style,
                         numbered_list_style):
    if first_bullet == '*':
        bullet_type = 'bullet'
        first_bullet = None
        list_style = bulleted_list_style
    else:
        bullet_type = '1'
        list_style = numbered_list_style
    group.append(ListFlowable(bulleted[:1],
                              style=list_style,
                              bulletType=bullet_type,
                              start=first_bullet))
    story.append(KeepTogether(group))
    bulleted = bulleted[1:]
    if bulleted:
        if first_bullet is not None:
            next_bullet = int(first_bullet) + 1
        else:
            next_bullet = first_bullet
        story.append(ListFlowable(bulleted,
                                  style=list_style,
                                  bulletType=bullet_type,
                                  start=next_bullet))


if __name__ == '__main__':
    main()
