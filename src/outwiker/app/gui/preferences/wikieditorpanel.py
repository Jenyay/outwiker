# -*- coding: utf-8 -*-

import wx

from outwiker.gui.editorstyleslist import EditorStylesList
from outwiker.gui.preferences.prefpanel import BasePrefPanel
from outwiker.pages.wiki.wikiconfig import WikiConfig


class WikiEditorPanel(BasePrefPanel):
    def __init__(self, parent, application):
        super().__init__(parent)

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
        self._stylesList.addStyle(_("Link"), self._config.link.value)
        self._stylesList.addStyle(_("Heading"), self._config.heading.value)
        self._stylesList.addStyle(_("Command"), self._config.command.value)
        self._stylesList.addStyle(_("Comment"), self._config.comment.value)
        self._stylesList.addStyle(_("Attachments"), self._config.attachment.value)
        self._stylesList.addStyle(_("Thumbnail"), self._config.thumbnail.value)

    def Save(self):
        self._config.link.value = self._stylesList.getStyle(0)
        self._config.heading.value = self._stylesList.getStyle(1)
        self._config.command.value = self._stylesList.getStyle(2)
        self._config.comment.value = self._stylesList.getStyle(3)
        self._config.attachment.value = self._stylesList.getStyle(4)
        self._config.thumbnail.value = self._stylesList.getStyle(5)
