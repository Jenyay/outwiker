#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .i18n import get_
from .pagecountpanel import PageCountPanel
from .maxdepthpanel import MaxDepthPanel


class TreeStatDialog (wx.Dialog):
    def __init__ (self, parent, treestat):
        """
        treestat - экземпляр класса TreeStat
        """
        super (TreeStatDialog, self).__init__ (parent)

        global _
        _ = get_()

        self.SetTitle (_(u"Tree Statistic"))
        self._createGUI ()
        self.Fit()
        self.Center (wx.CENTRE_ON_SCREEN)

        self.updateStat (treestat)


    def _createGUI (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        # Панель с информацией о количестве страниц
        self.pageCountPanel = PageCountPanel (self)
        mainSizer.Add (self.pageCountPanel, flag=wx.EXPAND | wx.ALL, border=4)

        # Панель с информацией о страницах с наибольшей вложенностью
        self.maxDepthPanel = MaxDepthPanel (self)
        mainSizer.Add (self.maxDepthPanel, flag=wx.EXPAND | wx.ALL, border=4)

        # Кнопка Ok
        okBtn = wx.Button (self, wx.ID_OK)
        mainSizer.Add (okBtn, flag=wx.ALIGN_RIGHT | wx.ALL, border=4)

        self.SetSizer (mainSizer)
        self.Layout()


    def updateStat (self, treestat):
        self._updatePageCount (treestat)
        self._updateMaxDepth (treestat)


    def _updatePageCount (self, treestat):
        """
        Обновление количества страниц
        """
        self.pageCountPanel.pageCount.SetValue (str (treestat.pageCount))


    def _updateMaxDepth (self, treestat):
        """
        Обновление панели с информацией о страницах с наибольшей вложенностью
        """
        self.maxDepthPanel.maxDepth.SetValue (str (treestat.pageCount))
