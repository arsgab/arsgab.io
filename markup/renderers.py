from datetime import datetime
from random import randint
from uuid import uuid4

from jinja2 import Environment
from pelican import signals
from pelican.generators import Generator

from markup import renderer_ref
from markup.processors.picture import render_picture_tag
from markup.processors.typography import typographed
from pelicanconf import SITENAME
from utils.datastructures import NavItem, dict_to_css_variables, filepath_to_dotnotation, remap
from utils.schematize import generate_schema_for_article
from utils.staticfiles import get_static_url, inline_static_assets
from utils.templating import render_obfuscated_mailto_link, render_page_metadata
from utils.url import get_datafile_url, qualify_url

NAVBAR = [
    NavItem('/', SITENAME, attrs={'rel': 'home'}),
    NavItem('/articles', 'Articles', file='articles.index'),
]

GLOBALS = {
    'NAVBAR': NAVBAR,
    'CURRENT_YEAR': datetime.now().year,
    'random': randint,
    'uuid': uuid4,
    'static': get_static_url,
    'api': get_datafile_url,
    'static_inline': inline_static_assets,
    'picture': render_picture_tag,
    'pagemeta': render_page_metadata,
    'schema': generate_schema_for_article,
    'mailto': render_obfuscated_mailto_link,
}

FILTERS = {
    'qualify': qualify_url,
    'cssvars': dict_to_css_variables,
    'remap': remap,
    'asdot': filepath_to_dotnotation,
    'tpgr': typographed,
}


def customize_jinja_env(env: Environment) -> None:
    env.lstrip_blocks = True
    env.trim_blocks = True
    env.globals.update(GLOBALS)
    env.filters.update(FILTERS)


def on_generators_preread(generator: Generator) -> None:
    customize_jinja_env(generator.env)
    try:
        renderer_ref.get()
    except LookupError:
        # Set context variable value only once, on first lookup
        renderer_ref.set(generator.env)


def register() -> None:
    for signal in (signals.article_generator_preread, signals.page_generator_preread):
        signal.connect(on_generators_preread)
