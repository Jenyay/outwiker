# -*- coding: UTF-8 -*-
from outwiker.pages.wiki.wikiconfig import WikiConfig


class TOCWikiGenerator (object):
    """
    Класс для создания оглавления в викинотации по списку разделов (экземпляров класса Section)
    """
    def __init__ (self, config):
        self._config = WikiConfig (config)


    def make (self, sections):
        result = u"\n".join ([self._makeStrItem (section) for section in sections])
        return result


    def _makeStrItem (self, section):
        return u"{mark} {title}".format (
            mark = u"*" * section.level,
            title = self._makeTitle (section.title, section.anchor))


    def _makeTitle (self, title, anchor):
        if len (anchor) == 0:
            return title

        if self._config.linkStyleOptions.value == 1:
            return u"[[#{anchor} | {title}]]".format (title = title,
                                                      anchor = anchor)
        else:
            return u"[[{title} -> #{anchor}]]".format (title = title,
                                                       anchor = anchor)
