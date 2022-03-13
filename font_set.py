from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_fonts(include_courier=False):
    source_path = Path(__file__).parent
    fonts_path = source_path / 'fonts'
    fredoka_file = fonts_path / 'Fredoka_One' / 'FredokaOne-Regular.ttf'
    raleway_file = fonts_path / 'Raleway' / 'static' / 'Raleway-Regular.ttf'
    raleway_bold_file = fonts_path / 'Raleway' / 'static' / 'Raleway-Bold.ttf'
    raleway_italic_file = fonts_path / 'Raleway' / 'static' / 'Raleway-Italic.ttf'
    raleway_bold_italic_file = fonts_path / 'Raleway' / 'static' / 'Raleway-BoldItalic.ttf'
    courier_file = fonts_path / 'Courier_Prime' / 'CourierPrime-Regular.ttf'
    pdfmetrics.registerFont(TTFont("Fredoka", fredoka_file))
    pdfmetrics.registerFont(TTFont("Raleway", raleway_file))
    pdfmetrics.registerFont(TTFont("Raleway-Bold", raleway_bold_file))
    pdfmetrics.registerFont(TTFont("Raleway-Italic", raleway_italic_file))
    pdfmetrics.registerFont(TTFont("Raleway-BoldItalic", raleway_bold_italic_file))
    pdfmetrics.registerFontFamily('Raleway',
                                  'Raleway',
                                  'Raleway-Bold',
                                  'Raleway-Italic',
                                  'Raleway-BoldItalic')
    if include_courier:
        pdfmetrics.registerFont(TTFont("Courier", courier_file))
        pdfmetrics.registerFontFamily('Courier',
                                      'Courier')
