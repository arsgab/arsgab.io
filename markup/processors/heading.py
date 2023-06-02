from xml.etree.ElementTree import Element

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class HeadingIdProcessor(Treeprocessor):
    def run(self, root: Element) -> None:
        # TODO
        ...


def makeExtension(**kwargs) -> Extension:  # noqa
    class HeadingExtension(Extension):
        def extendMarkdown(self, md) -> None:
            md.treeprocessors.register(HeadingIdProcessor(md.parser), 'heading_id', 998)

    return HeadingExtension(**kwargs)
