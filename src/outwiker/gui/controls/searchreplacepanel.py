# -*- coding: utf-8 -*-

import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.defines import ICONS_WIDTH, ICONS_HEIGHT
from outwiker.gui.images import readImage


class SearchReplacePanel(wx.Panel):
    def __init__(self, parent):
        super(SearchReplacePanel, self).__init__(
            parent,
            style=wx.TAB_TRAVERSAL | wx.RAISED_BORDER)

        self._mainSizer = None

        self._createGui()
        self._bindEvents()

        # Список элементов, относящихся к замене
        self._replaceGui = [self._replaceLabel,
                            self._replaceText,
                            self._replaceBtn,
                            self._replaceAllBtn,
                            ]

        self.setReplaceGuiVisible(False)

    def setReplaceGuiVisible(self, visible):
        """
        Установить, нужно ли показывать элементы GUI для замены
        """
        for item in self._replaceGui:
            item.Show(visible)

        self.Layout()

    def setPrevButtonVisible(self, visible):
        self._prevSearchBtn.Show(visible)
        self.Layout()

    def setResultLabelVisible(self, visible):
        self._resultLabel.Show(visible)
        self.Layout()

    def _bindEvents(self):
        for child in self.GetChildren():
            child.Bind(wx.EVT_KEY_DOWN, self._onKeyPressed)

    def getResultLabel(self):
        return self._resultLabel

    def getSearchTextCtrl(self):
        return self._searchText

    def getReplaceTextCtrl(self):
        return self._replaceText

    def getNextSearchBtn(self):
        return self._nextSearchBtn

    def getPrevSearchBtn(self):
        return self._prevSearchBtn

    def getReplaceBtn(self):
        return self._replaceBtn

    def getReplaceAllBtn(self):
        return self._replaceAllBtn

    def getCloseBtn(self):
        return self._closeBtn

    def _createGui(self):
        # Поле для ввода искомой фразы
        self._searchText = wx.TextCtrl(self, -1, "",
                                       style=wx.TE_PROCESS_ENTER)

        # Текст для замены
        self._replaceText = wx.TextCtrl(self, -1, "",
                                        style=wx.TE_PROCESS_ENTER)

        # Элементы интерфейса, связанные с поиском
        self._findLabel = wx.StaticText(self, -1, _("Find what: "))

        # Кнопка "Найти далее"
        self._nextSearchBtn = wx.Button(self, -1, _("Next"))

        # Кнопка "Найти выше"
        self._prevSearchBtn = wx.Button(self, -1, _("Prev"))

        # Метка с результатом поиска
        self._resultLabel = wx.StaticText(self, -1, "")
        self._resultLabel.SetMinSize((150, -1))

        # Элементы интерфейса, связанные с заменой
        self._replaceLabel = wx.StaticText(self, -1, _("Replace with: "))

        # Кнопка "Заменить"
        self._replaceBtn = wx.Button(self, -1, _("Replace"))

        # Кнопка "Заменить все"
        self._replaceAllBtn = wx.Button(self, -1, _("Replace All"))

        self._closeBtn = wx.BitmapButton(
            self,
            -1,
            readImage(getBuiltinImagePath("close.svg"), ICONS_WIDTH, ICONS_WIDTH))

        self._layout()

    def _layout(self):
        self._mainSizer = wx.FlexGridSizer(cols=6)
        self._mainSizer.AddGrowableCol(1)

        # Элементы интерфейса для поиска
        self._mainSizer.Add(self._findLabel, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add(self._searchText, 0, wx.ALL |
                            wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add(self._nextSearchBtn, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=1)
        self._mainSizer.Add(self._prevSearchBtn, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=1)
        self._mainSizer.Add(self._closeBtn, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL, border=1)
        self._mainSizer.Add(self._resultLabel, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL, border=2)

        # Элементы интерфейса для замены
        self._mainSizer.Add(self._replaceLabel, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add(self._replaceText, 0, wx.ALL |
                            wx.EXPAND | wx.ALIGN_CENTER_VERTICAL, border=2)
        self._mainSizer.Add(self._replaceBtn, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=1)
        self._mainSizer.Add(self._replaceAllBtn, 0, wx.ALL |
                            wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=1)

        self.SetSizer(self._mainSizer)
        self.Layout()

    def _onKeyPressed(self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self.Close()

        event.Skip()
