# -*- coding: utf-8 -*-

import wx

from outwiker.gui.editorstyleslist import EditorStylesList
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class WikiEditorPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super(type(self), self).__init__(parent)

        self._config = WikiConfig(application.config)
        self.__createGui()
        self.__layout()
        self.SetupScrolling()

    def __createGui(self):
        self._stylesList = EditorStylesList(self)

    def __layout(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)

        mainSizer.Add(self._stylesList, flag=wx.ALL | wx.EXPAND, border=2)

        self.SetSizer(mainSizer)
        self.Layout()

    def LoadState(self):
        self._stylesList.addStyle(_(u"Link"), self._config.link.value)
        self._stylesList.addStyle(_(u"Heading"), self._config.heading.value)
        self._stylesList.addStyle(_(u"Command"), self._config.command.value)

    def Save(self):
        self._config.link.value = self._stylesList.getStyle(0)
        self._config.heading.value = self._stylesList.getStyle(1)
        self._config.command.value = self._stylesList.getStyle(2)
