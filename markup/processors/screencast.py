from os.path import splitext
from xml.etree.ElementTree import Element, fromstring as xml_from_string

from utils import (
    Shortcode,
    ShortcodeProcessor,
    StrEnum,
    get_media_url,
    get_processed_media_url,
    render_template_partial,
)


class Screencast(Shortcode):
    required_attrs = {'src'}

    class Loading(StrEnum):
        LAZY = 'lazy'
        EAGER = 'eager'

    def create_element(self, index: int = 0) -> Element:
        rendered = render_template_partial('screencast', self.get_context())
        return xml_from_string(rendered)

    def get_context(self) -> dict:
        src, _ = splitext(self.attrs['src'])
        eager = self.attrs.get('lazy') == 'false' or 'eager' in self.attrs
        return {
            'src': src,
            'poster': get_processed_media_url(f'{src}.jpg', q=60),
            'sources': [
                {'type': 'video/webm', 'src': get_media_url(f'{src}.webm')},
                {'type': 'video/mp4', 'src': get_media_url(f'{src}.mp4')},
            ],
            'loading': self.Loading.EAGER if eager else self.Loading.LAZY,
            'bordered': 'bordered' in self.attrs,
        }


class ScreencastProcessor(ShortcodeProcessor):
    name = 'screencast'
    parser_cls = Screencast


makeExtension = ScreencastProcessor.register()
