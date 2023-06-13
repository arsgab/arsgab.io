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

VIDEO_DEFAULT_WIDTH = 800
VIDEO_DEFAULT_HEIGHT = 600
VIDEO_DEFAULT_RATIO = 1.333


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
        try:
            width, height = int(self.attrs.get('width'))  # type: ignore
            height = int(self.attrs.get('height'))  # type: ignore
            ratio = round(width / height, 3)  # type: ignore
        except (ValueError, TypeError):
            width, height = VIDEO_DEFAULT_WIDTH, VIDEO_DEFAULT_HEIGHT
            ratio = VIDEO_DEFAULT_RATIO
        try:
            playback_rate = float((self.attrs.get('speed') or '1.0').rstrip('x'))
        except ValueError:
            playback_rate = 1.0
        return {
            'loading': self.Loading.EAGER if eager else self.Loading.LAZY,
            'src': src,
            'sources': [
                {'type': 'video/webm', 'src': get_media_url(f'{src}.webm')},
                {'type': 'video/mp4', 'src': get_media_url(f'{src}.mp4')},
            ],
            'width': width,
            'height': height,
            'ratio': ratio,
            'poster': get_processed_media_url(src, q=60),
            'bordered': 'bordered' in self.attrs,
            'focusable': 'focusable' in self.attrs,
            'id': self.attrs.get('id'),
            'playback_rate': playback_rate,
        }


class ScreencastProcessor(ShortcodeProcessor):
    name = 'screencast'
    parser_cls = Screencast


makeExtension = ScreencastProcessor.register()
