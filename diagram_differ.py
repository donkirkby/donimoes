import typing
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
        png_alpha_bytes = BytesIO()
        self.write_png(png_alpha_bytes)
        return png_alpha_bytes.getvalue()

    def write_png(self, file: typing.Union[typing.BinaryIO, Path]):
        drawing = self.diagram.to_reportlab()
        png_bytes = BytesIO(drawToString(drawing, 'PNG'))
        image = Image.open(png_bytes)
        image_alpha = image.convert('RGBA')
        image_alpha.save(file, 'PNG')

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
        __tracebackhide__ = True
        super().assert_equal(LiveSvg(actual), LiveSvg(expected), file_prefix)


@pytest.fixture(scope='session')
def session_drawing_differ():
    """ Track all images compared in a session. """
    diffs_path = Path(__file__).parent / 'image_diffs'
    differ = DiagramDiffer(diffs_path)
    yield differ
    differ.remove_common_prefix()


@pytest.fixture
def drawing_differ(request, session_drawing_differ):
    """ Pass the current request to the session image differ. """
    session_drawing_differ.request = request
    yield session_drawing_differ
