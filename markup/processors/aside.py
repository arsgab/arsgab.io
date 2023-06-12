from xml.etree.ElementTree import Element, fromstring as xml_from_string

from utils import Shortcode, ShortcodeProcessor


class Aside(Shortcode, self_closing=False):
    def create_element(self, index: int = 0) -> Element:
        rendered = f'<aside markdown="1">{self._inner_content}</aside>'
        return xml_from_string(rendered)


class AsideProcessor(ShortcodeProcessor):
    name = 'aside'
    parser_cls = Aside


makeExtension = AsideProcessor.register()
