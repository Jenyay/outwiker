# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.config import WikiConfig


class TOCWikiGenerator:
    """
    Класс для создания оглавления в викинотации по списку разделов
    (экземпляров класса Section)
    """

    def __init__(self, config):
        self._config = WikiConfig(config)

    def make(self, sections):
        if len(sections) == 0:
            return ""

        minLevel = min(sections, key=lambda x: x.level).level
        result = "\n".join(
            [self._makeStrItem(section, minLevel) for section in sections]
        )
        return result

    def _makeStrItem(self, section, minLevel):
        return "{mark} {title}".format(
            mark="*" * (section.level - minLevel + 1),
            title=self._makeTitle(section.title, section.anchor),
        )

    def _makeTitle(self, title, anchor):
        if len(anchor) == 0:
            return title

        if self._config.linkStyleOptions.value == 1:
            return "[[#{anchor} | {title}]]".format(title=title, anchor=anchor)
        else:
            return "[[{title} -> #{anchor}]]".format(title=title, anchor=anchor)
