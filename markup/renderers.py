from datetime import datetime
from random import randint
from uuid import uuid4

from jinja2 import Environment
from pelican import ArticlesGenerator, signals
from pelican.contents import Article

from markup import renderer_ref
from markup.processors.picture import render_picture_tag
from pelicanconf import SITENAME
from utils.datastructures import NavItem, dict_to_css_variables, filepath_to_dotnotation, remap
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
    'mailto': render_obfuscated_mailto_link,
}

FILTERS = {
    'qualify': qualify_url,
    'cssvars': dict_to_css_variables,
    'remap': remap,
    'asdot': filepath_to_dotnotation,
}


def setup_jinja_env(generator: ArticlesGenerator) -> Environment:
    generator.env.globals.update(GLOBALS)
    generator.env.filters.update(FILTERS)
    renderer_ref.set(generator.env)
    return generator.env


def update_article_context(article_generator: ArticlesGenerator, content: Article) -> None:
    ...


def register() -> None:
    signals.article_generator_preread.connect(setup_jinja_env)
    signals.page_generator_preread.connect(setup_jinja_env)
    signals.article_generator_write_article.connect(update_article_context)
