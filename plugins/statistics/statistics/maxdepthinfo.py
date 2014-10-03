# -*- coding: UTF-8 -*-

from .i18n import get_


class MaxDepthInfo (object):
    """Класс для оформления сведений о страницах с максимальной глубиной вложенности"""
    def __init__(self, maxDepthList):
        """
        maxDepthList - список кортежей, полученный из класса TreeStat.maxDepth.
        Кортежи состоят из двух элементов: (уровень вложенности, ссылка на страницу)
        """
        self._maxDepthList = maxDepthList

        global _
        _ = get_()


    @property
    def content (self):
        maxDepth = 0 if len (self._maxDepthList) == 0 else self._maxDepthList[0][0]

        maxDepthHtml = u"<p>" + _(u"Max page depth: {0}").format (maxDepth) + "</p>"

        # Сформировать список страниц с наибольшей глубиной вложенности
        pagesList = [u"<li><a href='{link}' title='{link}'>{title}</a></li>".format (
            link="/" + page.subpath,
            title=page.title) for depth, page in self._maxDepthList]

        pagesHtml = u"<p><ul>" + u"".join (pagesList) + u"</ul></p>"

        return maxDepthHtml + pagesHtml + u"<hr/>"
