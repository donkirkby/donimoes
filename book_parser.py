import os
import re

import typing


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
    last_linked = None
    for s in states:
        try:
            name, address = s.get_link()
        except AttributeError:
            unlinked_states.append(s)
            if not isinstance(s, StartState):
                last_linked = s
            continue
        if last_linked is None:
            raise ValueError('Link must follow a paragraph.')
        last_linked.extra_markdown += s.raw_text
        links[name] = address
    printed_states = []
    last_printed = None
    for s in unlinked_states:
        if not s.is_printed():
            last_printed.raw_text += s.raw_text
            continue
        s.text = replace_links(s.text, links)
        s.text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s.text)
        printed_states.append(s)
        last_printed = s
    return printed_states


def replace_links(text, links):
    replacement = ''
    index = 0
    for match in re.finditer(r'\[([^]]+)]\[([^]]+)]', text):
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
    def __init__(self,
                 text: str = None,
                 style: str = Styles.Normal,
                 bullet: str = None,
                 raw_text: str = None):
        self.text = text
        if raw_text is None:
            raw_text = text
        self.raw_text = '' if raw_text is None else raw_text + os.linesep
        self.style = style
        self.bullet = bullet
        self.image_path = None
        self.extra_markdown = ''

    def add(self, line):
        if line.startswith('    '):
            return DiagramState('').add(line)
        if line == '---':
            return MetadataState(line)
        match = re.match(r'^\[([^]]+)]:\s*(.*)$', line)
        if match:
            link_name = match.group(1)
            address = match.group(2)
            return LinkState(link_name, address, line)
        match = re.match(r'^(#+)\s*(.*?)\s*#*$', line)
        if match:
            level = len(match.group(1))
            heading_text = match.group(2)
            return ParsingState(heading_text,
                                Styles.Heading + str(level),
                                raw_text=line)
        match = re.match(r'^((\*)|(\d+)\.)\s+(.*)$', line)
        if match:
            bullet = match.group(2) or match.group(3)
            text = match.group(4)
            return BulletedState(text, bullet=bullet, raw_text=line)
        if line:
            return ParagraphState(line)
        self.raw_text += line + os.linesep
        return self

    @staticmethod
    def is_printed():
        return True

    def __repr__(self):
        return 'ParsingState({!r}, {!r}, {!r})'.format(self.text,
                                                       self.style,
                                                       self.bullet)

    def __eq__(self, other):
        return (self.text == other.text and
                self.style == other.style and
                self.bullet == other.bullet)

    def write_markdown(self, markdown_file: typing.TextIO):
        """ Write the markdown for this state.

        :param markdown_file: the destination to write the markdown to
        """
        markdown_file.write(self.raw_text)
        markdown_file.write(self.extra_markdown)


class StartState(ParsingState):
    def is_printed(self):
        return False

    def __repr__(self):
        return 'StartState()'


class MetadataState(ParsingState):
    def __init__(self, text=None):
        super().__init__(text, Styles.Metadata)
        self.subtitle = None

    def is_printed(self):
        return True

    def __repr__(self):
        return f'MetadataState({self.text!r})'

    def add(self, line):
        self.raw_text += line + os.linesep
        if line == '---':
            return StartState()
        match = re.match('title: *', line)
        if match is not None:
            self.text = line[match.end():]
        match = re.match('subtitle: *', line)
        if match is not None:
            self.subtitle = line[match.end():]
        return self


class ParagraphState(ParsingState):
    def add(self, line):
        self.raw_text += line + os.linesep
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
        self.raw_text += line + os.linesep
        self.text = self.text + ' ' + line.strip()
        return self

    def __repr__(self):
        return 'BulletedState({!r}, bullet={!r})'.format(self.text,
                                                         self.bullet)


class LinkState(ParsingState):
    def __init__(self, name: str, address: str, raw_text: str):
        super().__init__(raw_text=raw_text)
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

    def write_markdown(self, markdown_file: typing.TextIO):
        print(f'![Diagram]({self.image_path})', file=markdown_file)
        print(file=markdown_file)
        markdown_file.write(self.extra_markdown)

    def __repr__(self):
        return 'DiagramState({!r})'.format(self.text)
