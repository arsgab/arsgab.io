from typing import Any

from markdown import Extension, Markdown
from markdown.postprocessors import Postprocessor
from typus.core import TypusCore
from typus.processors import EnQuotes, EnRuExpressions, EscapeHtml, EscapePhrases

THINSPACE = '\N{THIN SPACE}'
NBSPACE = '\N{NO-BREAK SPACE}'
EMDASH = '\N{EM DASH}'
ENDASH = '\N{EN DASH}'
HYPHEN = '-'


class Typus(TypusCore):
    class Expr(EnRuExpressions):
        expressions = (
            'spaces',
            'primes',
            'digit_spaces',
            'pairs',
            'units',
            'ranges',
            'vulgar_fractions',
            'math',
        )

    @staticmethod
    def thinspaced_mdash(text: str) -> str:
        text = text.replace(f' {EMDASH} ', f'{THINSPACE}{EMDASH}{THINSPACE}')
        return text

    @staticmethod
    def format_smiles(text: str) -> str:
        for smile in (':-)', ':-('):
            smile_welldone = smile.replace(HYPHEN, ENDASH)
            text = text.replace(f' {smile}', f'{NBSPACE}{smile_welldone}')
        return text

    processors = (EscapePhrases, EscapeHtml, EnQuotes, Expr)


_typus = Typus()


def typographed(text: str) -> str:
    text = _typus(text)
    text = _typus.thinspaced_mdash(text)
    text = _typus.format_smiles(text)
    return text


class TypographyPostprocesor(Postprocessor):
    def run(self, text: str) -> str:
        return typographed(text)


def makeExtension(**kwargs: Any) -> Extension:  # noqa
    class TypographyExtension(Extension):
        def extendMarkdown(self, md: Markdown) -> None:
            postprocessor = TypographyPostprocesor(md.parser)  # type: ignore
            md.postprocessors.register(postprocessor, 'typography', 999)

    return TypographyExtension(**kwargs)
