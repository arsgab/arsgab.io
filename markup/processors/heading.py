from re import compile as re_compile
from typing import Iterable
from xml.etree.ElementTree import Element, fromstring as xml_from_string

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class HeadingIdProcessor(Treeprocessor):
    HEADINGS_TAGS = {'h2', 'h3'}
    REGEX = re_compile(r'\[#(?P<idx>\w+)\](?P<text>.+)')
    ANCHOR_SYMBOL = '¶'

    def run(self, root: Element) -> None:
        headings = filter(lambda el: el.tag in self.HEADINGS_TAGS, root)
        self.add_headings_anchors(headings)

    def add_headings_anchors(self, headings: Iterable[Element]) -> None:
        for heading in headings:
            match = self.REGEX.match(heading.text)
            if not match:
                continue
            match_groups = match.groupdict()
            idx = match_groups['idx']
            heading.text = match_groups['text'].lstrip() + ' '
            heading.attrib.update({'id': idx})
            anchor = f'<a href="#{idx}">{self.ANCHOR_SYMBOL}</a>'
            heading.append(xml_from_string(anchor))


def makeExtension(**kwargs) -> Extension:  # noqa
    class HeadingExtension(Extension):
        def extendMarkdown(self, md) -> None:
            md.treeprocessors.register(HeadingIdProcessor(md.parser), 'heading_id', 998)

    return HeadingExtension(**kwargs)
