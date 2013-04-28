#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.guiconfig import GeneralGuiConfig

from .i18n import get_


class DatePageInfo (object):
    """Класс для генерации информации о старых страницах и страницах, которые изменяли в последнее время"""
    def __init__(self, treestat, itemsCount, config):
        """
        itemsCount - количество выводимых страниц в списках
        """
        self._treestat = treestat
        self._itemsCount = itemsCount

        self._pageDate = treestat.pageDate
        self._pageCount = treestat.pageCount

        self._config = GeneralGuiConfig (config)

        global _
        _ = get_()


    @property
    def content (self):
        recentPages = self._getRecentEditedPages()
        oldPages = self._getOldestPages()

        return u"""{recentPages}
{oldPages}
<hr/>""".format (recentPages=recentPages, oldPages=oldPages)



    def _getRecentEditedPages (self):
        title = _(u"Recent edited pages:")
        pageList = self._pageDate[0: min (self._itemsCount, self._pageCount)]

        itemsHtml = self._getPageListHtml (pageList)
        return u"""<p>{title}<br>{items}</p>""".format (title=title, items=itemsHtml)


    def _getOldestPages (self):
        title = _(u"Oldest pages:")
        pageListRevert = self._pageDate[:]
        pageListRevert.reverse()

        pageList = pageListRevert[0: min (self._itemsCount, self._pageCount)]

        itemsHtml = self._getPageListHtml (pageList)
        return u"""<p>{title}<br>{items}</p>""".format (title=title, items=itemsHtml)


    def _getPageListHtml (self, pageList):
        """
        Оформить список страниц в виде HTML
        """
        items = [u"<li><a href='{url}'>{title}</a> ({date})</li>".format (url=u"/" + page.subpath,
            title=page.title,
            date=page.datetime.strftime (self._config.dateTimeFormat.value))
                for page in pageList]

        return u"<ul>" + u"".join (items) + u"</ul>"
