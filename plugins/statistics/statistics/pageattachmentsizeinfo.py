#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.guiconfig import GeneralGuiConfig

from .i18n import get_


class PageAttachmentSizeInfo (object):
    """Класс для генерации информации о самых записях с самым большим размером прикрепленных файлов"""
    def __init__(self, pageAttachmentSizeList, itemsCount):
        """
        itemsCount - количество выводимых страниц в списках
        """
        self._pageListAll = pageAttachmentSizeList
        self._itemsCount = itemsCount

        global _
        _ = get_()


    @property
    def content (self):
        title = _(u"Pages with the largest size of attachments (in brackets the size of attachments):")
        pageListHtml = self._getGratestPages()

        return u"""<p>{title}<br>
{items}
</p>
<hr/>""".format (title=title, items=pageListHtml)


    def _getGratestPages (self):
        pageList = self._pageListAll[0: min (self._itemsCount, len (self._pageListAll) ) ]
        return self._getPageListHtml (pageList)


    def _getPageListHtml (self, pageList):
        """
        Оформить список страниц в виде HTML
        """
        # Локализованные единицы изменения размеров файлов
        kb = _(u"kB")

        items = [u"<li><a href='{url}'>{title}</a> ({size} {kb})</li>".format (url=u"/" + page.subpath,
            title=page.title,
            size="{0:,.2f}".format (size / 1024.0).replace (",", " "),
            kb=kb)
                for page, size in pageList]

        return u"<ul>" + u"".join (items) + u"</ul>"
