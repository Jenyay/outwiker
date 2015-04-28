# -*- coding: UTF-8 -*-

from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.system import getOS

from .i18n import get_


class DatePageInfo (object):
    """Класс для генерации информации о старых страницах и страницах, которые изменяли в последнее время"""
    def __init__(self, pageDateList, itemsCount, config):
        """
        itemsCount - количество выводимых страниц в списках
        """
        self._itemsCount = itemsCount
        self._pageDateList = pageDateList
        self._dateTimeFormat = GeneralGuiConfig (config).dateTimeFormat.value

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
        pageList = self._pageDateList[0: min (self._itemsCount, len (self._pageDateList))]

        itemsHtml = self._getPageListHtml (pageList)
        return u"""<p>{title}<br>{items}</p>""".format (title=title, items=itemsHtml)


    def _getOldestPages (self):
        title = _(u"Oldest pages:")
        pageListRevert = self._pageDateList[:]
        pageListRevert.reverse()

        pageList = pageListRevert[0: min (self._itemsCount, len (self._pageDateList))]

        itemsHtml = self._getPageListHtml (pageList)
        return u"""<p>{title}<br>{items}</p>""".format (title=title, items=itemsHtml)


    def _getPageListHtml (self, pageList):
        """
        Оформить список страниц в виде HTML
        """
        items = [u"<li><a href='{url}'>{title}</a> ({date})</li>".format (
            url=u"/" + page.subpath,
            title=page.title,
            date=unicode (page.datetime.strftime (self._dateTimeFormat), getOS().filesEncoding))
            for page in pageList]

        return u"<ul>" + u"".join (items) + u"</ul>"
