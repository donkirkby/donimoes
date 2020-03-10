from base64 import standard_b64encode
from io import StringIO, BytesIO
from pathlib import Path
from turtle import Turtle

import pytest
from PIL import Image
from reportlab.graphics.renderPM import drawToString

from svg_diagram import SvgDiagram


class DiagramDiffer:
    def __init__(self):
        # maximum diff between RGB values to ignore. Default allows minor
        # differences from antialiasing.
        self.tolerance = 3

        self.work_dir: Path = Path(__file__).parent / 'image_diffs'
        self.work_dir.mkdir(exist_ok=True)
        self.mismatch_found = False
        self.test_names = set()
        for work_file in self.work_dir.iterdir():
            if work_file.name == 'README.md':
                continue
            assert work_file.suffix in ('.svg', '.png')
            work_file.unlink()

    def diff_pixel(self, actual_pixel, expected_pixel):
        ar, ag, ab, aa = actual_pixel
        er, eg, eb, ea = expected_pixel
        max_diff = max(abs(a - b) for a, b in zip(actual_pixel, expected_pixel))
        if max_diff > self.tolerance:
            self.mismatch_found = True
            # Colour
            dr = 0xff
            dg = (ag + eg) // 5
            db = (ab + eb) // 5

            # Opacity
            da = 0xff
        else:
            # Colour
            dr, dg, db = ar, ag, ab

            # Opacity
            da = aa // 3
        return dr, dg, db, da

    def assert_equal(self,
                     actual_diagram: SvgDiagram,
                     expected_diagram: SvgDiagram,
                     name: str):
        if name in self.test_names:
            raise ValueError(f'Duplicate test name: {name!r}')
        self.test_names.add(name)
        actual_png = diagram_to_image(actual_diagram)
        expected_png = diagram_to_image(expected_diagram)
        w = max(actual_png.width, expected_png.width)
        h = max(actual_png.height, expected_png.height)

        png_actual_padded = Image.new(actual_png.mode, (w, h))
        png_expected_padded = Image.new(expected_png.mode, (w, h))
        png_actual_padded.paste(actual_png)
        png_expected_padded.paste(expected_png)
        png_diff = Image.new(actual_png.mode, (w, h))
        self.mismatch_found = False
        png_diff.putdata([self.diff_pixel(actual_pixel, expected_pixel)
                          for actual_pixel, expected_pixel in zip(
                            png_actual_padded.getdata(),
                            png_expected_padded.getdata())])

        # Display image when in live turtle mode.
        display_image = getattr(Turtle, 'display_image', None)
        if display_image is not None:
            t = Turtle()
            try:
                w = t.screen.cv.cget('width')
                h = t.screen.cv.cget('height')
                ox, oy = w/2, h/2
                text_height = 20
                t.penup()
                t.goto(-ox, oy)
                t.right(90)
                t.forward(text_height)
                t.write(f'Actual')
                display_image(ox+t.xcor(), oy-t.ycor(),
                              image=encode_image(actual_png))
                t.forward(actual_png.height)
                t.forward(text_height)
                t.write(f'Diff')
                display_image(ox+t.xcor(), oy-t.ycor(),
                              image=encode_image(png_diff))
                t.forward(png_diff.height)
                t.forward(text_height)
                t.write('Expected')
                display_image(ox+t.xcor(), oy-t.ycor(),
                              image=encode_image(expected_png))
                t.forward(expected_png.height)
            except Exception as ex:
                t.write(str(ex))

        if not self.mismatch_found:
            return
        actual_svg = StringIO()
        actual_diagram.svg_drawing.write(actual_svg, pretty=True)
        actual_text = actual_svg.getvalue()
        expected_svg = StringIO()
        expected_diagram.svg_drawing.write(expected_svg, pretty=True)
        expected_text = expected_svg.getvalue()
        (self.work_dir / (name+'_actual.svg')).write_text(actual_text)
        (self.work_dir / (name+'_expected.svg')).write_text(expected_text)
        png_diff.save(self.work_dir / (name+'_diff.png'))
        assert actual_text == expected_text
        assert not self.mismatch_found


def diagram_to_image(diagram: SvgDiagram) -> Image.Image:
    drawing = diagram.to_reportlab()
    png_bytes = BytesIO(drawToString(drawing, 'PNG'))
    image = Image.open(png_bytes)
    return image.convert('RGBA')


def encode_image(image: Image.Image) -> bytes:
    writer = BytesIO()
    image.save(writer, format='PNG')
    encoded = standard_b64encode(writer.getvalue())
    return encoded.decode('UTF-8')


@pytest.fixture(scope='session')
def drawing_differ():
    return DiagramDiffer()
