from os import environ as env
from pathlib import Path

from dotenv import load_dotenv

BASE_PATH = Path('.')
load_dotenv()

# Site setup
AUTHOR = env.get('AUTHOR') or 'Arseny Gabdullin'
AUTHOR_EMAIL = env.get('AUTHOR_EMAIL') or 'mail@arsgab.io'
AUTHOR_EMAIL_SECONDARY = env.get('AUTHOR_EMAIL_SECONDARY') or 'me@arsgab.io'
SITENAME = env.get('SITENAME') or AUTHOR
SITE_FQDN = env.get('SITE_FQDN') or 'arsgab.io'
SITEDESC = env.get('SITEDESC') or 'OFFICIAL WEBSITE'
TIMEZONE = env.get('TIMEZONE') or 'Europe/Belgrade'
STATS_SCRIPTS_URL = env.get('STATS_SCRIPTS_URL') or 'https://stat.arsgab.io/stonks'
STATS_WEBSITE_ID = env.get('STATS_WEBSITE_ID')
DEFAULT_OG_IMAGE = env.get('DEFAULT_OG_IMAGE') or 'share.jpeg'
DEFAULT_DATE = 'fs'

# Build setup
OUTPUT_PATH = BASE_PATH / 'dist'
PATH = 'articles'
ARTICLE_URL = '/articles/{slug}'
ARTICLE_SAVE_AS = PATH + '/{slug}.html'
PAGE_URL = '/{slug}'
PAGE_SAVE_AS = '{slug}.html'
DIRECT_TEMPLATES = ['index', 'allarticles']
ALLARTICLES_SAVE_AS = PATH + '/index.html'
THEME = 'assets'
THEME_TEMPLATES_OVERRIDES = [f'{THEME}/scripts']
THEME_STATIC_PATHS = ['favicons', 'images', 'manifest.webmanifest']
THEME_STATIC_DIR = 'static'
IGNORE_FILES = ['*.css']
PLUGIN_PATHS = ['markup']
PLUGINS = ['renderers']
DATAFILES_PATH = OUTPUT_PATH / 'data'
DATA_URL = '/api/'
LOAD_CONTENT_CACHE = env.get('LOAD_CONTENT_CACHE') == 'true'
DELETE_OUTPUT_DIRECTORY = env.get('DELETE_OUTPUT_DIRECTORY') == 'true'

# Create build directories
OUTPUT_PATH.mkdir(exist_ok=True)
DATAFILES_PATH.mkdir(exist_ok=True)

# Staticfiles
STATIC_PATHS = []
STATIC_ASSETS_PATH = BASE_PATH / THEME
STATIC_BUILD_PATH = OUTPUT_PATH / THEME_STATIC_DIR
STATIC_URL = f'/{THEME_STATIC_DIR}/'
INLINE_SCRIPTS = env.get('INLINE_SCRIPTS') == 'true'

# Processors/renderers setup
_PROCESSORS = ['picture', 'screencast', 'heading', 'typography']
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.meta': {},
        'markdown.extensions.abbr': {},
        'markdown.extensions.md_in_html': {},
        **{f'markup.processors.{processor}': {} for processor in _PROCESSORS},
    },
    'output_format': 'html5',
}

# Media processing setup
IMGPROXY_KEY = env.get('IMGPROXY_KEY')
IMGPROXY_SALT = env.get('IMGPROXY_SALT')
IMGPROXY_FQDN = env.get('IMGPROXY_FQDN', 'img.arsgab.io')
IMGPROXY_DEFAULT_QUALITY = int(env.get('IMGPROXY_DEFAULT_QUALITY', '80'))
IMGPROXY_URL_NAMESPACE = env.get('IMGPROXY_URL_NAMESPACE') or SITE_FQDN
IMGPROXY_PLAIN_SOURCE_URL = env.get('IMGPROXY_PLAIN_SOURCE_URL') == 'true'

# Disable category/author/feeds pages build
CATEGORY_SAVE_AS = AUTHOR_SAVE_AS = ''
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
DISPLAY_PAGES_ON_MENU = DISPLAY_CATEGORIES_ON_MENU = False

# JSON-LD schema for website
MAIN_JSON_LD = {
    '@context': 'http://schema.org',
    '@type': 'Person',
    'name': AUTHOR,
    'image': 'https://avatars.githubusercontent.com/u/1730172',
    'url': f'https://{SITE_FQDN}',
    'jobTitle': 'Software Engineer',
    'alumniOf': 'Saint Petersburg State University',
    'gender': 'male',
    'sameAs': [
        'https://www.linkedin.com/in/arsgab/',
        'https://github.com/arsgab',
        'https://instagram.com/arseny.ga',
        'https://www.facebook.com/arsgab',
        'https://twitter.com/arsgab',
        'https://mastodon.online/@arsgab',
        'https://www.strava.com/athletes/arsgab',
    ],
}
