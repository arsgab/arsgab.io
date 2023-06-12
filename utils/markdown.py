from html.parser import HTMLParser
from re import DOTALL, compile as re_compile
from typing import Callable, Match, Type
from xml.etree.ElementTree import Element

from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension


class Shortcode(HTMLParser):
    self_closing: bool
    required_attrs: set[str] = set()
    self_closing: bool = False
    attrs: dict[str, str]
    _tagname: str
    _inner_content: str

    def __init_subclass__(cls, self_closing: bool = True, **kwargs) -> None:
        cls.self_closing = self_closing
        super().__init_subclass__(**kwargs)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str]]) -> None:
        self.attrs = dict(attrs) if tag == self._tagname else {}

    def handle_data(self, data: str) -> None:
        self._inner_content = data or ''

    def create_element(self, index: int = 0) -> Element:
        raise NotImplementedError


class ShortcodeProcessor(BlockProcessor):
    name: str
    parser_cls: Type[Shortcode]
    _match: Match
    _count: int = 0

    def test(self, parent: Element, block: str) -> bool:
        if self.parser_cls.self_closing:
            pattern = rf'^\[{self.name}(?P<attrs>.*?)\]$'
            flags = 0
        else:
            pattern = rf'^\[{self.name}(?P<attrs>.*?)\](?P<inner>.*?)\[\/{self.name}\]$'
            flags = DOTALL
        regex = re_compile(pattern, flags=flags)
        self._match = regex.match(block)
        return bool(self._match)

    def run(self, parent: Element, blocks: list[str]) -> bool:
        blocks.pop(0)
        match_parts = self._match.groupdict()
        block = f'<{self.name}{match_parts["attrs"]}>'
        if not self.parser_cls.self_closing:
            block = f'<{self.name}{match_parts["attrs"]}>{match_parts["inner"]}</{self.name}>'
        node = self.parser_cls()
        node._tagname = self.name
        node.feed(block)
        required_attrs = self.parser_cls.required_attrs
        if required_attrs and not all((node.attrs.get(attr) for attr in required_attrs)):
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
