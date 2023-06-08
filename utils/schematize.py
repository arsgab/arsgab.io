from typing import NamedTuple

from jinja2.runtime import Context
from pelican.contents import Article
from pelican.utils import SafeDatetime

from pelicanconf import AUTHOR, CONTENT_PATH, DEFAULT_OG_IMAGE, SITE_LANG, SITEDESC, SITENAME

from .media import get_processed_media_url
from .url import qualify_url

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
SCHEMA_ORG = 'https://schema.org'


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


AUTHOR_SCHEMA = {
    '@type': 'Person',
    'name': AUTHOR,
    'url': qualify_url('/'),
}


def generate_schema_for_article(
    article: Article, schema_type: str = 'TechArticle', level: str = 'beginner'
) -> dict[str, str | dict]:
    schema = {
        '@context': SCHEMA_ORG,
        '@type': schema_type,
        'inLanguage': SITE_LANG,
        'headline': article.title,  # noqa
        'url': qualify_url(article.url),
        'author': AUTHOR_SCHEMA,
        'datePublished': schema_org_date_fmt(article.date),
        'dateModified': schema_org_date_fmt(article.modified),
        'proficiencyLevel': level,
        # TODO: extract genre & keywords from article setup
        # 'genre': '...',
        # 'keywords': '...',
    }

    # Meta description of the article
    description = getattr(article, 'meta_description', None)
    if description:
        schema.update(description=description)

    # Same as share image
    image = getattr(article, 'og_image', None)
    if image:
        schema.update(image=get_processed_media_url(image, **OG_IMAGE_PROCESSING_PARAMS))

    # Get word count from source (in very primitive way)
    try:
        wordcount = get_article_wordcount(article)
    except Exception:  # noqa
        wordcount = 0
    if wordcount:
        schema.update(wordcount=wordcount)

    return schema


def schema_org_date_fmt(date: SafeDatetime) -> str:
    date_part, time_part = str(date).split(' ')
    return f'{date_part}T{time_part}'


def get_article_wordcount(article: Article, metadata_delimiter: str = '---') -> int:
    sourcefile = CONTENT_PATH / article.relative_source_path
    source = sourcefile.read_text()
    *_, content = source.split(metadata_delimiter)

    wordcount = 0
    for block in content.splitlines():
        if block.startswith(('#', '*', '[')):
            continue
        words = [chunk for chunk in block.split(' ') if len(chunk) > 3]
        wordcount += len(words)

    return wordcount
