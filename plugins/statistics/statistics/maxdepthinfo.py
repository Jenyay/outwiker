#!/usr/bin/python
# -*- coding: UTF-8 -*-

class MaxDepthInfo (object):
    """Класс для оформления сведений о страницах с максимальной глубиной вложенности"""
    def __init__(self, treestat):
        super(MaxDepthInfo, self).__init__()
        self._treestat = treestat


    @property
    def content (self):
        maxDepthList = self._treestat.maxDepth
        maxDepth = 0 if len (maxDepthList) == 0 else self._treestat.maxDepth[0][0]

        maxDepthHtml = u"<p>" + _(u"Max page depth: {0}").format (maxDepth) + "</p>";

        # Сформировать список страниц с наибольшей глубиной вложенности
        pagesList = [u"<li><a href='{link}' title='{link}'>{title}</a></li>".format (link="/" + page.subpath, 
            title=page.title) for depth, page in maxDepthList]

        pagesHtml = u"<p><ul>" + u"".join (pagesList) + u"</ul></p>"

        return maxDepthHtml + pagesHtml + u"<hr/>"

        
