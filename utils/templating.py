from jinja2 import pass_context, pass_eval_context
from jinja2.filters import do_mark_safe, do_xmlattr
from jinja2.runtime import Context, EvalContext

from markup import renderer_ref
from pelicanconf import AUTHOR_EMAIL

from .schematize import PageMetadata
from .url import obfuscate_string


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
    obfuscated = obfuscate_string(url)
    attrs = (attrs or {}) | {'data-hidden-href': obfuscated}
    attrs = do_xmlattr(ctx, attrs)
    link = f'<a href="{href}" {attrs}>{text}</a>'
    return do_mark_safe(link)
