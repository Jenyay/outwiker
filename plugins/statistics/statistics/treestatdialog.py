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
from .pageattachmentsizeinfo import PageAttachmentSizeInfo
from .statisticsconfig import StatisticsConfig
from .longprocessrunner import LongProcessRunner


class TreeStatDialog (wx.Dialog):
    def __init__ (self, parent, application, treestat):
        """
        treestat - экземпляр класса TreeStat
        """
        super (TreeStatDialog, self).__init__ (
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self._application = application
        self._treestat = treestat
        self._config = StatisticsConfig (self._application.config)

        # Размер списков со страницами
        self._itemsCount = 20

        # Шаблон для содержимого HTML-рендера
        self._htmlTemplate = u"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='X-UA-Compatible' CONTENT='IE=edge' />
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>
</HEAD>

<BODY>
{content}
</BODY>
</HTML>"""

        global _
        _ = get_()

        self.SetTitle (_(u"Tree Statistic"))

        self.SetSize ((self._config.treeDialogWidth.value, self._config.treeDialogHeight.value))

        self.Show()
        self._createGUI ()
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

        if self._application.selectedPage is not None:
            self._htmlRender.page = self._application.selectedPage
        elif len (self._application.wikiroot.children) != 0:
            self._htmlRender.page = self._application.wikiroot.children[0]

        mainSizer.Add (self._htmlRender, flag=wx.EXPAND | wx.ALL, border=4)

        # Кнопка Ok
        okBtn = wx.Button (self, wx.ID_OK)
        mainSizer.Add (okBtn, flag=wx.ALIGN_RIGHT | wx.ALL, border=4)

        self.Bind (wx.EVT_CLOSE, self._onClose)
        self.Bind (wx.EVT_BUTTON, self._onClose, id=wx.ID_OK)

        self.SetSizer (mainSizer)
        self.Layout()


    def _updateStatistics (self):
        # Шаманство, связанное с тем, что HTML-рендер ожидает, что есть выбранная страница
        if self._htmlRender.page is None:
            self._setHtml (_(u"A tree has no pages"))
            return

        self._setHtml (_(u"Collecting statistics. Please wait..."))

        runner = LongProcessRunner (self._getContent,
                                    self,
                                    _(u"Statistics"),
                                    _(u"Collecting statistics..."))

        resultList = runner.run ()

        self._setHtml (resultList)


    def _setHtml (self, content):
        resultHtml = self._htmlTemplate.format (content=content)
        self._htmlRender.SetPage (resultHtml, getCurrentDir())


    def _getContent (self):
        """
        Создать HTML со статистикой. То, что должно быть внутри тега <body>
        """
        infoList = [PageCountInfo (self._treestat.pageCount),
                    MaxDepthInfo (self._treestat.maxDepth),
                    TagsInfo (self._treestat.frequentTags, self._itemsCount),
                    DatePageInfo (self._treestat.pageDate, self._itemsCount, self._application.config),
                    PageContentLengthInfo (self._treestat.pageContentLength, self._itemsCount),
                    PageAttachmentSizeInfo (self._treestat.pageAttachmentsSize, self._itemsCount)]

        return u"".join ([info.content for info in infoList])


    def _onClose (self, event):
        self._saveParams()
        event.Skip()


    def _saveParams (self):
        width, height = self.GetSizeTuple()
        self._config.treeDialogWidth.value = width
        self._config.treeDialogHeight.value = height
