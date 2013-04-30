#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.htmlrenderfactory import getHtmlRender
from outwiker.core.system import getCurrentDir

from .i18n import get_
from .maxdepthinfo import MaxDepthInfo
from .pagecountinfo import PageCountInfo
from .tagsinfo import TagsInfo
from .datepageinfo import DatePageInfo
from .pagecontentlengthinfo import PageContentLengthInfo


class TreeStatDialog (wx.Dialog):
    def __init__ (self, parent, application, treestat):
        """
        treestat - экземпляр класса TreeStat
        """
        super (TreeStatDialog, self).__init__ (parent)
        self._application = application
        self._treestat = treestat

        # Размер списков со страницами
        self._itemsCount = 10

        global _
        _ = get_()

        self.SetTitle (_(u"Tree Statistic"))
        self.Show()
        self._createGUI ()
        self.SetSize ((600, 500))
        self.Center (wx.CENTRE_ON_SCREEN)

        self._updateStatistics()


    def _createGUI (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        self._htmlRender = getHtmlRender (self)

        # Шаманство, связанное с тем, что HTML-рендер ожидает, что есть выбранная страница
        # Если бы ему это было не обязательно, то достаточно было бы использовать только следующую строку
        # self._htmlRender.page = self._application.selectedPage

        if self._application.selectedPage != None:
            self._htmlRender.page = self._application.selectedPage
        elif len (self._application.wikiroot.children) != 0:
            self._htmlRender.page = self._application.wikiroot.children[0]

        mainSizer.Add (self._htmlRender, flag=wx.EXPAND | wx.ALL, border=4)

        # Кнопка Ok
        okBtn = wx.Button (self, wx.ID_OK)
        mainSizer.Add (okBtn, flag=wx.ALIGN_RIGHT | wx.ALL, border=4)

        self.SetSizer (mainSizer)
        self.Layout()


    def _updateStatistics (self):
        # Шаманство, связанное с тем, что HTML-рендер ожидает, что есть выбранная страница
        if self._htmlRender.page == None:
            return _(u"A tree has no pages")

        htmlTemplate = u"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='X-UA-Compatible' CONTENT='IE=edge' />
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>
</HEAD>

<BODY>
{content}
</BODY>
</HTML>"""

        content = self._getContent ()

        resultHtml = htmlTemplate.format (content=content)
        self._htmlRender.SetPage (resultHtml, getCurrentDir())


    def _getContent (self):
        """
        Создать HTML со статистикой. То, что должно быть внутри тега <body>
        """
        infoList = [PageCountInfo (self._treestat),
                MaxDepthInfo (self._treestat),
                TagsInfo (self._treestat, self._itemsCount),
                DatePageInfo (self._treestat, self._itemsCount, self._application.config),
                PageContentLengthInfo (self._treestat, self._itemsCount)]

        return u"".join ([info.content for info in infoList])
