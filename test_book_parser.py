import unittest
from io import StringIO

import pytest

from book_parser import parse, Styles, ParagraphState, BulletedState, \
    ParsingState, DiagramState, MetadataState


class BookParserTest(unittest.TestCase):
    def test_paragraph(self):
        source = """\
This is a one-line paragraph.
"""
        expected_tree = [ParagraphState('This is a one-line paragraph.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_multiline_paragraph(self):
        source = """\
This is a
two-line paragraph.
"""
        expected_tree = [ParagraphState('This is a two-line paragraph.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_two_paragraphs(self):
        source = """\
This is a paragraph.

This is another.
"""
        expected_tree = [ParagraphState('This is a paragraph.'),
                         ParagraphState('This is another.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_long_gap(self):
        source = """\
This is a paragraph.


This is another.
"""
        expected_tree = [ParagraphState('This is a paragraph.'),
                         ParagraphState('This is another.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_metadata(self):
        source = """\
---
title: Some Title
subtitle: Something else
---
This is a paragraph.
"""
        expected_tree = [MetadataState('Some Title'),
                         ParagraphState('This is a paragraph.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_diagram(self):
        source = """\
    Indent of four spaces
    makes a diagram.
    Indent is removed.
"""
        expected_diagram = """\
Indent of four spaces
makes a diagram.
Indent is removed.
"""
        expected_tree = [DiagramState(expected_diagram)]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_diagram_and_paragraph(self):
        source = """\
    Short diagram.
Following paragraph.
"""
        expected_tree = [DiagramState('Short diagram.\n'),
                         ParagraphState('Following paragraph.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_links(self):
        source = """\
Paragraph with [example link][link].

[link]: http://example.com
"""
        expected_tree = [ParagraphState(
            'Paragraph with <a href="http://example.com">example link</a>.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_two_links(self):
        source = """\
Now [two][first] [links][second].

[first]: http://example.com
[second]: http://bogus.com
"""
        expected_tree = [ParagraphState(
            'Now <a href="http://example.com">two</a> '
            '<a href="http://bogus.com">links</a>.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_bold(self):
        source = """\
Paragraph with **emphasized text**.
"""
        expected_tree = [
            ParagraphState('Paragraph with <b>emphasized text</b>.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_heading(self):
        source = """\
# Title #
Some text.
"""
        expected_tree = [ParsingState('Title', Styles.Heading1),
                         ParagraphState('Some text.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_heading2(self):
        source = """\
## Title #
Some text.
"""
        expected_tree = [ParsingState('Title', Styles.Heading2),
                         ParagraphState('Some text.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_numbered(self):
        source = """\
Some text.

1. First
2. Second
"""
        expected_tree = [ParagraphState('Some text.'),
                         BulletedState('First', bullet='1'),
                         BulletedState('Second', bullet='2')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    def test_numbered_multiple_lines(self):
        source = """\
Some text.

1. First item
    with multiple lines.
2. Second item.
"""
        expected_tree = [
            ParagraphState('Some text.'),
            BulletedState('First item with multiple lines.', bullet='1'),
            BulletedState('Second item.', bullet='2')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)


def test_raw_text_paragraph(tmpdir):
    source = """\
Some text
on two lines.

More text.
"""
    tree = parse(source)
    converted = StringIO()
    for state in tree:
        state.write_markdown(converted)

    assert converted.getvalue() == source


def test_bullet_list(tmpdir):
    source = """\
A paragraph.

* A list item.
* Another item.

More text.
"""
    tree = parse(source)
    converted = StringIO()
    for state in tree:
        state.write_markdown(converted)

    assert converted.getvalue() == source


def test_linked(tmpdir):
    source = """\
A paragraph with a [Link][link] in the middle.

[link]: https://example.com/
"""
    tree = parse(source)
    converted = StringIO()
    for state in tree:
        state.write_markdown(converted)

    assert converted.getvalue() == source


def test_rule_diagrams():
    source = """\
One paragraph

    1|2 3
        -
    5|6 4

Another paragraph

    0|0 1
        -
    2|2 1

Last paragraph
"""
    expected_text = """\
One paragraph

![Diagram](images/diagram1.png)

Another paragraph

![Diagram](images/diagram2.png)

Last paragraph
"""
    tree = parse(source)
    assert len(tree) == 5
    tree[1].image_path = 'images/diagram1.png'
    tree[3].image_path = 'images/diagram2.png'
    converted = StringIO()
    for state in tree:
        state.write_markdown(converted)

    assert converted.getvalue() == expected_text


def test_link_after_diagram():
    source = """\
Paragraph with [a link][link].

    1|2 3
        -
    5|6 4

[link]: https://example.com

Last paragraph
"""
    expected_text = """\
Paragraph with [a link][link].

![Diagram](images/diagram1.png)

[link]: https://example.com

Last paragraph
"""
    tree = parse(source)
    tree[1].image_path = 'images/diagram1.png'
    converted = StringIO()
    for state in tree:
        state.write_markdown(converted)

    assert converted.getvalue() == expected_text


def test_link_first():
    source = """\
[link]: https://example.com

Paragraph with [a link][link].

Last paragraph
"""
    with pytest.raises(ValueError, match='Link must follow a paragraph.'):
        parse(source)
