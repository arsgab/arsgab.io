from collections import defaultdict, deque
from contextlib import suppress
from contextvars import ContextVar
from typing import Any
from xml.etree.ElementTree import Element, fromstring as xml_from_string

from utils import (
    ImageDimensions,
    ImageResizeSet,
    Shortcode,
    ShortcodeProcessor,
    StrEnum,
    get_processed_media_url,
    render_template_partial,
)

PICTURE_DEFAULT_RATIO = 1.777  # 16:9
PICTURE_RATIO_PRECISION = 3
picture_processor_context_ref: ContextVar[defaultdict[int, deque['Picture']]] = ContextVar(
    'picture_processor_context', default=defaultdict(deque)
)


class Picture(Shortcode):
    required_attrs = {'src'}
    index: int = 1
    ratio: float = PICTURE_DEFAULT_RATIO
    dimensions: ImageDimensions
    resizes: ImageResizeSet
    src: str

    class Loading(StrEnum):
        LAZY = 'lazy'
        EAGER = 'eager'

    class Orientation(StrEnum):
        LANDSCAPE = 'landscape'
        PORTRAIT = 'portrait'

    def feed(self, data: str) -> None:
        super().feed(data)
        self.src = self.attrs.get('src')
        if not self.src:
            return

        # Extract dimensions from filename or create fake from predefined ratio
        dimensions = ImageDimensions.extract_from_filename(self.src)
        if dimensions:
            ratio = round(dimensions.width / dimensions.height, PICTURE_RATIO_PRECISION)
        else:
            ratio = self._extract_ratio_value()
            dimensions = ImageDimensions.fake_from_ratio(ratio)
        self.ratio = ratio
        self.dimensions = dimensions

        # Create image resizes set
        self.resizes = self.get_resizes()

    def _extract_ratio_value(self, precision: int = PICTURE_RATIO_PRECISION) -> float:
        ratio = self.attrs.get('ratio')
        if ratio and ':' in ratio:
            width, height = ratio.split(':')
            with suppress(ValueError):
                ratio_value = int(width) / int(height)
                return round(ratio_value, precision)
        elif ratio:
            with suppress(ValueError):
                return float(ratio)
        if self.attrs.get('orient') == self.Orientation.PORTRAIT:
            return round(1 / PICTURE_DEFAULT_RATIO, precision)
        return PICTURE_DEFAULT_RATIO

    def create_element(self, index: int = 0) -> Element:
        self.index = index
        refs = picture_processor_context_ref.get()
        refs[id(self)].append(self)
        rendered = render_template_partial('picture', self.get_context())
        return xml_from_string(rendered)

    def get_resizes(self) -> ImageResizeSet:
        processing_options = {}
        version = self.attrs.get('v')
        if version:
            processing_options.update(cachebuster=f'v{version}')
        return ImageResizeSet(self.src, source_width=self.dimensions.width, **processing_options)

    def get_context(self) -> dict:
        eager = self.attrs.get('lazy') == 'false' or 'eager' in self.attrs
        span, offset = self.attrs.get('grid', '|').split('|')
        span = self.attrs.get('w') or span
        offset = self.attrs.get('x') or offset
        return {
            'src': self.src,
            'index': self.index,
            'id': self.html_id,
            'sources': self.resizes.sources,
            'fallback': self.resizes.fallback,
            'loading': self.Loading.EAGER if eager else self.Loading.LAZY,
            'dimensions': self.dimensions,
            'ratio': self.ratio,
            'alt': self.html_alt,
            'caption': self.html_caption,
            'span': span or '*',
            'offset': offset or '*',
            'bordered': 'bordered' in self.attrs,
        }

    @property
    def html_id(self) -> str:
        return self.attrs.get('id') or f'figure{self.index}'

    @property
    def html_alt(self) -> str:
        return self.attrs.get('alt') or f'Figure {self.index}'

    @property
    def html_caption(self) -> str:
        caption = self.attrs.get('caption') or ''
        return f'<a tabindex="-1" href="#{self.html_id}"><i>Figure {self.index}</i></a>. {caption}'


class PictureProcessor(ShortcodeProcessor):
    name = 'pic'
    parser_cls = Picture


makeExtension = PictureProcessor.register()


# TODO: refactor this block
def render_picture_tag(
    src: str,
    width: int | None = None,
    height: int | None = None,
    ratio: float = PICTURE_DEFAULT_RATIO,
    loading: str = 'lazy',
    **kwargs: Any,
) -> str:
    if not any((width, height)):
        return ''
    elif not width:
        width = int(height * ratio)
    elif not height:
        height = int(width * ratio)
    source = {
        'srcset': [
            get_processed_media_url(src, width=width, height=height, **kwargs),
            get_processed_media_url(src, width=width * 2, height=height * 2, **kwargs) + ' 2x',
        ],
        'media_query': '(min-width: 0px)',
    }
    fallback = get_processed_media_url(src, width=width, height=height, ext='jpg', **kwargs)
    ctx = {
        'sources': (source,),
        'fallback': fallback,
        'loading': loading,
        'ratio': ratio,
        'dimensions': (width, height),
    }
    return render_template_partial('picture-tag', ctx)
