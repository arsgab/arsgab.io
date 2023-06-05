from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor
from typus.core import TypusCore
from typus.processors import EnQuotes, EnRuExpressions, EscapeHtml, EscapePhrases


class TypusExpressions(EnRuExpressions):
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


class Typus(TypusCore):
    processors = (
        EscapePhrases,
        EscapeHtml,
        EnQuotes,
        TypusExpressions,
    )


typographed = Typus()


class TypographyPostprocesor(Postprocessor):
    def run(self, text: str) -> str:
        return typographed(text)


def makeExtension(**kwargs) -> Extension:  # noqa
    class TypographyExtension(Extension):
        def extendMarkdown(self, md) -> None:
            md.postprocessors.register(TypographyPostprocesor(md.parser), 'typography', 999)

    return TypographyExtension(**kwargs)
