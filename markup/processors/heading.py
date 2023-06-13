from re import compile as re_compile
from typing import Any, Iterable, Iterator
from xml.etree.ElementTree import Element, fromstring as xml_from_string

from markdown import Extension, Markdown
from markdown.treeprocessors import Treeprocessor

from utils import render_template_partial


class HeadingIdProcessor(Treeprocessor):
    HEADINGS_TAGS = {'h2', 'h3'}
    REGEX = re_compile(r'\{#(?P<idx>[\w-]+)\}(?P<text>.+)')
    ANCHOR_SYMBOL = '¶'

    def run(self, root: Element) -> None:
        headings = filter(lambda el: el.tag in self.HEADINGS_TAGS, root)
        anchors = self.add_headings_anchors(headings)
        toc = [{'id': idx, 'title': title} for idx, title in anchors]
        toc_rendered = render_template_partial('article-toc', {'toc': toc})
        root.insert(0, xml_from_string(toc_rendered))

    def add_headings_anchors(self, headings: Iterable[Element]) -> Iterator[tuple[str, str]]:
        for heading in headings:
            match = self.REGEX.match(heading.text or '')
            if not match:
                continue
            match_groups = match.groupdict()
            idx = match_groups['idx']
            text = match_groups['text'].strip()
            heading.text = text + ' '
            heading.attrib.update({'id': idx})
            anchor = f'<a href="#{idx}" tabindex="-1">{self.ANCHOR_SYMBOL}</a>'
            heading.append(xml_from_string(anchor))
            if heading.tag == 'h2':
                yield idx, text


def makeExtension(**kwargs: Any) -> Extension:  # noqa
    class HeadingExtension(Extension):
        def extendMarkdown(self, md: Markdown) -> None:
            processor = HeadingIdProcessor(md.parser)  # type: ignore
            md.treeprocessors.register(processor, 'heading_id', 998)

    return HeadingExtension(**kwargs)
