from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image
from reportlab.graphics.renderPM import drawToString
from space_tracer import LiveImage, LiveImageDiffer

from svg_diagram import SvgDiagram


class LiveSvg(LiveImage):
    def __init__(self, diagram: SvgDiagram):
        super().__init__()
        self.diagram = diagram

    def convert_to_png(self) -> bytes:
        drawing = self.diagram.to_reportlab()
        png_bytes = BytesIO(drawToString(drawing, 'PNG'))
        image = Image.open(png_bytes)
        image_alpha = image.convert('RGBA')
        png_alpha_bytes = BytesIO()
        image_alpha.save(png_alpha_bytes, 'PNG')
        return png_alpha_bytes.getvalue()

    def save(self, file_path: Path) -> Path:
        """ Save the image to a file.

        :param file_path: The path to save the file to, without an extension.
        :return: The path of the saved file, with an extension.
        """
        extended_path = file_path.with_suffix('.svg')
        extended_path.write_text(self.diagram.turtle.to_svg())
        return extended_path


class DiagramDiffer(LiveImageDiffer):
    def assert_equal(self,
                     actual: SvgDiagram,
                     expected: SvgDiagram,
                     file_prefix: str = None):
        """ Raise an AssertionError if this image doesn't match the expected.

        Also display this image as the Actual image, the other image as the
        Expected image, and a difference between them.
        :param actual: the test image
        :param expected: the image to compare to
        :param file_prefix: base name for debug files to write when images
            aren't equal. Debug files are written when diffs_path is passed to
            __init__() and either request fixture is passed to init or
            file_prefix is passed to this method.
        """
        super().assert_equal(LiveSvg(actual), LiveSvg(expected), file_prefix)


@pytest.fixture(scope='session')
def drawing_differ(request):
    diffs_path = Path(__file__).parent / 'image_diffs'
    differ = DiagramDiffer(diffs_path, request)
    yield differ
    differ.remove_common_prefix()
