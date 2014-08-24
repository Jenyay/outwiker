# -*- coding: UTF-8 -*-


class TOCWikiGenerator (object):
    """
    Класс для создания оглавления в викинотации по списку разделов (экземпляров класса Section)
    """
    def make (self, sections):
        result = u"\n".join ([self._makeStrItem (section) for section in sections])
        return result


    def _makeStrItem (self, section):
        return u"{mark} {title}".format (
                mark = u"*" * section.level,
                title = self._makeTitle (section.title, section.anchor))


    def _makeTitle (self, title, anchor):
        return title
