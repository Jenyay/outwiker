#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

from BeautifulSoup import BeautifulSoup

from .exceptions import HtmlNotFoundError
from .baseexporter import BaseExporter


class HtmlExporter (BaseExporter):
    """
    Класс для экспорта HTML- и викистраниц
    """
    def export (self, outdir, exportname, imagesonly, alwaysOverwrite):
        """
        Экспорт HTML-страниц
        """
        assert (self._page.getTypeString() == "html" or 
                self._page.getTypeString() == "wiki" )

        self.__htmlFileName = u"__content.html"

        # Чтение файла с содержимым
        try:
            with open (os.path.join (self._page.path, self.__htmlFileName) ) as fp:
                content = unicode (fp.read(), "utf8")
        except IOError:
            raise HtmlNotFoundError (_(u"{0} not found").format (self.__htmlFileName) )

        changedContent = self.__prepareHtmlContent (content, exportname)

        self._exportContent (self._page, 
                changedContent,
                exportname,
                outdir,
                imagesonly,
                alwaysOverwrite)


    def __replaceAttaches (self, tags, attrib, exportname):
        """
        Заменить ссылки на папку __attach на новую папку с вложениями
        """
        self.__attachDir = "__attach"

        for tag in tags:
            if tag.has_key (attrib) and tag[attrib].startswith (self.__attachDir):
                tag[attrib] = tag[attrib].replace (self.__attachDir, exportname, 1)


    def __prepareHtmlContent (self, content, exportname):
        """
        Заменить ссылки на прикрепленные файлы
        Используется при экспорте HTML-страниц
        """
        soup = BeautifulSoup (content)
        images = soup.findAll ("img")
        self.__replaceAttaches (images, "src", exportname)

        links = soup.findAll ("a")
        self.__replaceAttaches (links, "href", exportname)

        return unicode (soup.renderContents(), "utf8")
