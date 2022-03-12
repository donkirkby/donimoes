from reportlab.pdfgen import canvas


class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, is_booklet=False, font_name='Times-Roman', **kwargs):
        super().__init__(*args, **kwargs)
        self.is_booklet = is_booklet
        self.font_name = font_name
        self.previous_bottom = 0

    def showPage(self):
        self.draw_canvas()
        super().showPage()

    def draw_canvas(self):
        x = 30
        width, height = self._pagesize

        template = getattr(self, '_doctemplate', None)
        if template is None:
            bottom = self.previous_bottom
        else:
            bottom = self.previous_bottom = template.bottomMargin

        self.saveState()
        self.setFont(self.font_name, 7 if self.is_booklet else 9)
        if self._pageNumber % 2:
            self.drawRightString(width-x, bottom, str(self._pageNumber))
        else:
            self.drawString(x, bottom, str(self._pageNumber))
        if self._pageNumber == 1:
            self.drawCentredString(width / 2,
                                   bottom,
                                   "donkirkby.github.io/donimoes")
        self.restoreState()
