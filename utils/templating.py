from base64 import b64encode
from typing import NamedTuple

from jinja2 import pass_context, pass_eval_context
from jinja2.filters import do_mark_safe, do_xmlattr
from jinja2.runtime import Context, EvalContext

from markup import renderer_ref
from pelicanconf import AUTHOR_EMAIL, DEFAULT_OG_IMAGE, SITEDESC, SITENAME

from .media import get_processed_media_url

OG_IMAGE_WIDTH = 1200
OG_IMAGE_HEIGHT = 630
OG_IMAGE_PROCESSING_PARAMS = {
    'width': OG_IMAGE_WIDTH,
    'height': OG_IMAGE_HEIGHT,
    'ext': 'jpg',
    'gravity': 'so',
    'rt': 'fill',
    'q': 75,
}


def render_template(template_name: str, ctx: dict = None) -> str:
    renderer = renderer_ref.get()
    if not template_name.endswith('.html'):
        template_name = f'{template_name}.html'
    ctx = ctx or {}
    template = renderer.get_template(template_name)
    rendered = template.render(ctx)
    return do_mark_safe(rendered)


def render_template_partial(partial_name: str, ctx: dict = None) -> str:
    return render_template(f'partials/{partial_name}', ctx=ctx)


class PageMetadata(NamedTuple):
    title: str = SITENAME
    description: str = SITEDESC
    canonical_link: str | None = None
    og_type: str = 'website'
    og_title: str = SITENAME
    og_description: str = SITEDESC
    og_image: str = DEFAULT_OG_IMAGE
    og_image_width: int = OG_IMAGE_WIDTH
    og_image_height: int = OG_IMAGE_HEIGHT
    published_date: str | None = None

    @property
    def og_image_url(self) -> str:
        return get_processed_media_url(self.og_image, **OG_IMAGE_PROCESSING_PARAMS)

    @classmethod
    def from_context(cls, ctx: Context) -> 'PageMetadata':
        article = ctx.get('article')
        if not article:
            title = ctx.get('title') or SITENAME
            return cls(title=title)

        title = getattr(article, 'meta_title', '') or article.title
        description = getattr(article, 'meta_description', '')
        description = description or getattr(article, 'subtitle', '') or SITEDESC
        og_title = getattr(article, 'og_title', '') or title
        og_description = getattr(article, 'og_desc', '') or description
        og_image = getattr(article, 'og_image', '') or DEFAULT_OG_IMAGE
        return cls(
            title=title,
            description=description,
            canonical_link=article.url,
            og_type='article',
            og_title=og_title,
            og_description=og_description,
            og_image=og_image,
            published_date=article.date.strftime('%Y-%m-%d'),
        )


@pass_context
def render_page_metadata(ctx: Context) -> str:
    metadata = PageMetadata.from_context(ctx)
    return render_template_partial('pagemeta', {'meta': metadata})


@pass_eval_context
def render_obfuscated_mailto_link(
    ctx: EvalContext,
    address: str = AUTHOR_EMAIL,
    text: str = 'Email',
    href: str = '#',
    attrs: dict = None,
) -> str:
    attrs = (attrs or {}) | {'data-hidden-mailto': 'true'}
    return render_obfuscated_link(ctx, f'mailto:{address}', text, href=href, attrs=attrs)


def render_obfuscated_link(
    ctx: EvalContext,
    url: str,
    text: str,
    href: str = '#',
    attrs: dict = None,
) -> str:
    obfuscated = _obfuscate_string(url)
    attrs = (attrs or {}) | {'data-hidden-href': obfuscated}
    attrs = do_xmlattr(ctx, attrs)
    link = f'<a href="{href}" {attrs}>{text}</a>'
    return do_mark_safe(link)


def _obfuscate_string(string: str) -> str:
    encoded = b64encode(string.encode())
    return encoded.decode()
