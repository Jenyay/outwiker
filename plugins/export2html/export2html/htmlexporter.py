# -*- coding: UTF-8 -*-

import os.path
import re

# from BeautifulSoup import BeautifulSoup

from .baseexporter import BaseExporter


class HtmlExporter (BaseExporter):
    """
    Класс для экспорта HTML- и викистраниц
    """
    def __init__ (self, page):
        BaseExporter.__init__ (self, page)

        from .i18n import _
        global _


    def export (self, outdir, exportname, imagesonly, alwaysOverwrite):
        """
        Экспорт HTML-страниц
        """
        assert (self._page.getTypeString() == "html" or
                self._page.getTypeString() == "wiki")

        self.__htmlFileName = u"__content.html"

        # Чтение файла с содержимым
        try:
            with open (os.path.join (self._page.path, self.__htmlFileName)) as fp:
                content = unicode (fp.read(), "utf8")
        except IOError:
            content = u""

        changedContent = self.__prepareHtmlContent (content, exportname)

        self._exportContent (self._page,
                             changedContent,
                             exportname,
                             outdir,
                             imagesonly,
                             alwaysOverwrite)


    def __replaceAttaches (self, content, tag, attrib, exportname):
        """
        Заменить ссылки на папку __attach на новую папку с вложениями
        """
        __attachDir = "__attach"

        tag_regex = """<\s*({tag})\s+
            (.*?)
            ({attrib})\s*=['"]{attach}(.*?)['"]
            (.*?)
            (/?)>
            """.format (tag=tag, attrib=attrib, attach=__attachDir)

        regex = re.compile (tag_regex, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)

        replace = u'<\\1 \\2\\3="{exportname}\\4"\\5\\6>'.format (exportname=exportname)
        content = regex.sub (replace, content)

        # for currenttag in tags:
        return content


    def __prepareHtmlContent (self, content, exportname):
        """
        Заменить ссылки на прикрепленные файлы
        Используется при экспорте HTML-страниц
        """
        content = self.__replaceAttaches (content, "a", "href", exportname)
        content = self.__replaceAttaches (content, "img", "src", exportname)

        return content
