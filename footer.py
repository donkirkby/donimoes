from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, is_booklet=False, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.is_booklet = is_booklet

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        if not self.is_booklet:
            reordered_pages = self.pages
        else:
            while len(self.pages) % 8 != 0:
                self.showPage()
            original_pages = self.pages[:]
            reordered_pages = []
            while original_pages:
                reordered_pages.append(original_pages.pop(1))
                reordered_pages.append(original_pages.pop(-2))
                reordered_pages.append(original_pages.pop(2))
                reordered_pages.append(original_pages.pop(-3))
                reordered_pages.append(original_pages.pop(-1))
                reordered_pages.append(original_pages.pop(0))
                reordered_pages.append(original_pages.pop(-1))
                reordered_pages.append(original_pages.pop(0))
        for page in reordered_pages:
            self.__dict__.update(page)
            self.draw_canvas()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self):
        x = 30
        self.saveState()
        self.setFont('Times-Roman', 14 if self.is_booklet else 9)
        if self._pageNumber % 2:
            self.drawString(LETTER[0]-x, 65, str(self._pageNumber))
        else:
            self.drawString(x, 65, str(self._pageNumber))
        if self._pageNumber == 1:
            self.drawCentredString(LETTER[0] / 2,
                                   65,
                                   "donkirkby.github.com/donimoes")
        self.restoreState()
