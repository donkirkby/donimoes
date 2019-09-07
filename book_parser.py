import re


class Styles(object):
    Normal = 'Normal'
    Heading = 'Heading'
    Heading1 = 'Heading1'
    Heading2 = 'Heading2'
    Diagram = 'Diagram'
    Metadata = 'Metadata'


def parse(source):
    lines = source.splitlines()
    states = []
    state = StartState()
    for line in lines:
        new_state = state.add(line)
        if new_state is not state:
            states.append(new_state)
            state = new_state

    links = {}
    unlinked_states = []
    for s in states:
        try:
            name, address = s.get_link()
        except AttributeError:
            unlinked_states.append(s)
            continue
        links[name] = address
    printed_states = []
    for s in unlinked_states:
        if not s.is_printed():
            continue
        s.text = replace_links(s.text, links)
        s.text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s.text)
        printed_states.append(s)
    return printed_states


def replace_links(text, links):
    replacement = ''
    index = 0
    for match in re.finditer(r'\[([^\]]+)\]\[([^\]]+)\]', text):
        block = text[index:match.start()]
        replacement += block
        link_name = match.group(2)
        link = links[link_name]
        replacement += '<a href="%s">%s</a>' % (link, match.group(1))
        index = match.end()

    if replacement:
        block = text[index:]
        if block.startswith(' '):
            block = '&nbsp;' + block[1:]
        replacement += block
    return replacement or text


class ParsingState(object):
    def __init__(self, text=None, style=Styles.Normal, bullet=None):
        self.text = text
        self.style = style
        self.bullet = bullet

    def add(self, line):
        if line.startswith('    '):
            return DiagramState('').add(line)
        if line == '---':
            return MetadataState()
        match = re.match(r'^\[([^\]]+)\]:\s*(.*)$', line)
        if match:
            link_name = match.group(1)
            address = match.group(2)
            return LinkState(link_name, address)
        match = re.match(r'^(#+)\s*(.*?)\s*#*$', line)
        if match:
            level = len(match.group(1))
            heading_text = match.group(2)
            return ParsingState(heading_text, Styles.Heading + str(level))
        match = re.match(r'^(\d+)\.\s+(.*)$', line)
        if match:
            bullet = match.group(1)
            text = match.group(2)
            return BulletedState(text, bullet=bullet)
        if line:
            return ParagraphState(line)
        return self

    def is_printed(self):
        return True

    def __repr__(self):
        return 'ParsingState({!r}, {!r}, {!r})'.format(self.text,
                                                       self.style,
                                                       self.bullet)

    def __eq__(self, other):
        return (self.text == other.text and
                self.style == other.style and
                self.bullet == other.bullet)


class StartState(ParsingState):
    def is_printed(self):
        return False

    def __repr__(self):
        return 'StartState()'


class MetadataState(ParsingState):
    def __init__(self, text=None):
        super().__init__(text, Styles.Metadata)

    def is_printed(self):
        return True

    def __repr__(self):
        return f'MetadataState({self.text!r})'

    def add(self, line):
        if line == '---':
            return StartState()
        match = re.match('title: *', line)
        if match is not None:
            self.text = line[match.end():]
        return self


class ParagraphState(ParsingState):
    def add(self, line):
        if line:
            self.text = self.text + ' ' + line
            return self
        return StartState()

    def __repr__(self):
        return 'ParagraphState({!r})'.format(self.text)


class BulletedState(ParsingState):
    def add(self, line):
        if not line.startswith('  '):
            return StartState().add(line)
        self.text = self.text + ' ' + line.strip()
        return self

    def __repr__(self):
        return 'BulletedState({!r}, bullet={!r})'.format(self.text,
                                                         self.bullet)


class LinkState(ParsingState):
    def __init__(self, name, address):
        super().__init__()
        self.name = name
        self.address = address

    def get_link(self):
        return self.name, self.address

    def is_printed(self):
        return False

    def __repr__(self):
        return 'LinkState({!r}, {!r})'.format(self.name, self.address)


class DiagramState(ParsingState):
    def __init__(self, line):
        super(DiagramState, self).__init__(line, Styles.Diagram)

    def add(self, line):
        if line.startswith('    '):
            self.text = self.text + line[4:] + '\n'
            return self
        return StartState().add(line)

    def __repr__(self):
        return 'DiagramState({!r})'.format(self.text)

if __name__ == '__live_coding__':
    import unittest

    def testSomething(self):
        source = """\
Paragraph with **emphasized text**.
"""
        expected_tree = [
            ParagraphState('Paragaph with <b>emphasized text</b>.')]
        tree = parse(source)

        self.assertEqual(expected_tree, tree)

    class DummyTest(unittest.TestCase):

        def test_delegation(self):
            testSomething(self)

    suite = unittest.TestSuite()
    suite.addTest(DummyTest("test_delegation"))
    test_results = unittest.TextTestRunner().run(suite)

    print(test_results.errors)
    print(test_results.failures)
