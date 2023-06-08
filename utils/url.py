from base64 import b64encode
from urllib.parse import urljoin

from pelicanconf import DATA_URL, SITE_FQDN


def qualify_url(url: str, host: str = SITE_FQDN, scheme: str = 'https') -> str:
    if not url:
        return ''
    if url.startswith('http'):
        return url
    base = f'{scheme}://{host}'
    return urljoin(base, url)


def get_datafile_url(filename: str) -> str:
    return f'{DATA_URL}{filename}'


def obfuscate_string(string: str) -> str:
    encoded = b64encode(string.encode())
    return encoded.decode()
