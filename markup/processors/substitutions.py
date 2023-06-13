from typing import Any

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor

MD_LINK_NEWTAB_SHORTCUT = '{: newtab }'
MD_LINK_NEWTAB = '{: target="_blank" rel="noopener" }'


class SubstitutionsPreprocessor(Preprocessor):
    def run(self, lines: list[str]) -> list[str]:
        lines_mapper = map(self.expand_newtab_shortcuts, lines)
        return list(lines_mapper)

    @staticmethod
    def expand_newtab_shortcuts(text: str) -> str:
        return text.replace(MD_LINK_NEWTAB_SHORTCUT, MD_LINK_NEWTAB)


def makeExtension(**kwargs: Any) -> Extension:  # noqa
    class SubstitutionsExtension(Extension):
        def extendMarkdown(self, md: Markdown) -> None:
            preprocessor = SubstitutionsPreprocessor(md.parser)  # type: ignore
            md.preprocessors.register(preprocessor, 'substitutions', 1)

    return SubstitutionsExtension(**kwargs)
