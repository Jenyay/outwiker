# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.editorstyleslist import EditorStylesList
from outwiker.pages.wiki.wikiconfig import WikiConfig


class WikiEditorPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        self._config = WikiConfig (Application.config)

        self.__createGui()
        self.__layout()


    def __createGui (self):
        self._stylesList = EditorStylesList (self)


    def __layout(self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (0)

        mainSizer.Add (self._stylesList, flag = wx.ALL | wx.EXPAND, border = 2)

        self.SetSizer (mainSizer)
        self.Layout()


    def LoadState(self):
        self._stylesList.addStyle (_(u"Link"), self._config.link.value)
        self._stylesList.addStyle (_(u"Heading"), self._config.heading.value)
        self._stylesList.addStyle (_(u"Command"), self._config.command.value)


    def Save (self):
        self._config.link.value = self._stylesList.getStyle (0)
        self._config.heading.value = self._stylesList.getStyle (1)
        self._config.command.value = self._stylesList.getStyle (2)
