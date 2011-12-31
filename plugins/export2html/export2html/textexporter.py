#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cgi
import os.path
from string import Template

from .baseexporter import BaseExporter

class TextExporter (BaseExporter):
    """
    Класс для экспорта текстовых страниц
    """
    def export (self, outdir, exportname, imagesonly, alwaysOverwrite):
        """
        Экспортировать содержимое текстовой страницы
        Может бросить исключение IOError, если не найден файл с шаблоном
        Используется для экспорта текстовых страниц
        """
        assert self._page.getTypeString() == "text"
        template = self.__loadTemplate()
        content = self.__prepareTextContent (self._page.content)
        resultcontent = template.substitute (content=content, title=self._page.title)

        self._exportContent (self._page, 
                resultcontent,
                exportname,
                outdir,
                imagesonly,
                alwaysOverwrite)


    def __prepareTextContent (self, content):
        result = u"<pre>{0}</pre>".format (cgi.escape (content))
        return result


    def __loadTemplate (self):
        """
        Загрузить шаблон.
        Используется для экспорта текстовых страниц
        """
        templatedir = u"templates"
        singleTemplate = u"single.html"

        templateFileName = os.path.join (os.path.dirname (__file__), templatedir, singleTemplate)
        with open (templateFileName) as fp:
            template = unicode (fp.read(), "utf8")

        return Template (template)
