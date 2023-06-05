from html.parser import HTMLParser
from re import compile as re_compile
from typing import Callable, Type
from xml.etree.ElementTree import Element

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension


class Shortcode(HTMLParser):
    required_attrs: set[str] = set()
    attrs: dict[str, str]
    _tagname: str

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        self.attrs = dict(attrs) if tag == self._tagname else {}

    def create_element(self, index: int = 0) -> Element:
        raise NotImplementedError


class ShortcodeProcessor(BlockProcessor):
    name: str
    parser_cls: Type[Shortcode]
    _count: int = 0

    def test(self, parent: Element, block: str) -> bool:
        regex = re_compile(rf'\[{self.name}(.+)]')
        return bool(regex.match(block))

    def run(self, parent: Element, blocks: list[str]) -> bool:
        block = blocks.pop(0).replace('[', '<').replace(']', '>')
        node = self.parser_cls()
        node._tagname = self.name
        node.feed(block)
        for attr in self.parser_cls.required_attrs:
            if not node.attrs.get(attr):
                return False

        self._count += 1
        element = node.create_element(index=self._count)
        parent.append(element)
        node.close()
        return True

    @classmethod
    def register(cls, priority: int = 999) -> Callable:
        def handler(**kwargs):
            class ExtensionClass(Extension):
                def extendMarkdown(self, md) -> None:
                    md.parser.blockprocessors.register(cls(md.parser), cls.name, priority)

            return ExtensionClass(**kwargs)

        return handler
