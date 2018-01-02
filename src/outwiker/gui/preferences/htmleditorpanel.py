# -*- coding: utf-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.gui.editorstyleslist import EditorStylesList
from outwiker.gui.guiconfig import HtmlEditorStylesConfig
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class HtmlEditorPanel(BasePrefPanel):
    def __init__(self, parent):
        super(type(self), self).__init__(parent)

        self._config = HtmlEditorStylesConfig(Application.config)

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
        self._stylesList.addStyle(_(u"Tag"),
                                  self._config.tag.value)

        self._stylesList.addStyle(_(u"Unknown tag"),
                                  self._config.tagUnknown.value)

        self._stylesList.addStyle(_(u"Attribute"),
                                  self._config.attribute.value)

        self._stylesList.addStyle(_(u"Unknown attribute"),
                                  self._config.attributeUnknown.value)

        self._stylesList.addStyle(_(u"Number"),

                                  self._config.number.value)
        self._stylesList.addStyle(_(u"String"),

                                  self._config.string.value)

        self._stylesList.addStyle(_(u"Comment"),
                                  self._config.comment.value)

    def Save(self):
        self._config.tag.value = self._stylesList.getStyle(0)
        self._config.tagUnknown.value = self._stylesList.getStyle(1)
        self._config.attribute.value = self._stylesList.getStyle(2)
        self._config.attributeUnknown.value = self._stylesList.getStyle(3)
        self._config.number.value = self._stylesList.getStyle(4)
        self._config.string.value = self._stylesList.getStyle(5)
        self._config.comment.value = self._stylesList.getStyle(6)
