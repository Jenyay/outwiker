# -*- coding: utf-8 -*-

from .i18n import get_


class PageContentLengthInfo:
    """Класс для генерации информации о самых длинных записях"""

    def __init__(self, pageContentList, itemsCount):
        """
        itemsCount - количество выводимых страниц в списках
        """
        self._pageListAll = pageContentList
        self._itemsCount = itemsCount

        global _
        _ = get_()

    @property
    def content(self):
        title = _("The longest notes (in brackets the number of characters):")
        pageListHtml = self._getLongestPages()

        return """<p>{title}<br>
{items}
</p>
<hr/>""".format(
            title=title, items=pageListHtml
        )

    def _getLongestPages(self):
        pageList = self._pageListAll[0 : min(self._itemsCount, len(self._pageListAll))]
        return self._getPageListHtml(pageList)

    def _getPageListHtml(self, pageList):
        """
        Оформить список страниц в виде HTML
        """

        items = [
            "<li><b>{title}</b> ({length})</li>".format(
                title=page.display_subpath, length=length
            )
            for page, length in pageList
        ]

        return "<ul>" + "".join(items) + "</ul>"
