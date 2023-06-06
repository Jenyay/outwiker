# -*- coding: utf-8 -*-

import html

from .template import loadTemplate
from .baseexporter import BaseExporter


class TextExporter(BaseExporter):
    """
    Класс для экспорта текстовых страниц
    """

    def __init__(self, page):
        super().__init__(page)

        from .i18n import _

        global _

    def export(self, outdir, exportname, imagesonly, alwaysOverwrite):
        """
        Экспортировать содержимое текстовой страницы
        Может бросить исключение IOError, если не найден файл с шаблоном
        Используется для экспорта текстовых страниц
        """
        singleTemplate = "single.html"

        assert self._page.getTypeString() == "text"

        template = loadTemplate(singleTemplate)
        content = self.__prepareTextContent(self._page.content)
        resultcontent = template.substitute(content=content, title=self._page.title)

        self._exportContent(
            self._page, resultcontent, exportname, outdir, imagesonly, alwaysOverwrite
        )

    def __prepareTextContent(self, content):
        result = "<pre>{0}</pre>".format(html.escape(content))
        return result
