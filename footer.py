from reportlab.pdfgen import canvas


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, is_booklet=False, font_name='Times-Roman', **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.is_booklet = is_booklet
        self.font_name = font_name

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        if True or not self.is_booklet:
            reordered_pages = self.pages
        else:
            page_offsets = (1, -2, 2, -3, -1, 0, -1, 0)
            while len(self.pages) % len(page_offsets) != 0:
                self.showPage()
            original_pages = self.pages[:]
            reordered_pages = []
            while original_pages:
                for page_offset in page_offsets:
                    reordered_pages.append(original_pages.pop(page_offset))
        for page in reordered_pages:
            self.__dict__.update(page)
            self.draw_canvas()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self):
        x = 30
        width, height = self._pagesize

        # noinspection PyUnresolvedReferences
        bottom = self._doctemplate.bottomMargin

        self.saveState()
        self.setFont(self.font_name, 7 if self.is_booklet else 9)
        if self._pageNumber % 2:
            self.drawString(width-x, bottom, str(self._pageNumber))
        else:
            self.drawString(x, bottom, str(self._pageNumber))
        if self._pageNumber == 1:
            self.drawCentredString(width / 2,
                                   bottom,
                                   "donkirkby.github.io/donimoes")
        self.restoreState()
