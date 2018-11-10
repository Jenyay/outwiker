# -*- coding: UTF-8 -*-

import wx

from outwiker.core.defines import REGISTRY_PAGE_CURSOR_POSITION
from outwiker.gui.basetextpanel import BaseTextPanel
from .textpageeditor import TextPageEditor


class TextPanel (BaseTextPanel):
    """
    Класс для представления текстовых страниц
    """

    def __init__(self, parent, application):
        super().__init__(parent, application)

        self.__createGui()
        self.Bind(self.EVT_SPELL_ON_OFF, handler=self._onSpellOnOff)

    def GetEditor(self):
        return self.textEditor

    def Clear(self):
        self.Unbind(self.EVT_SPELL_ON_OFF, handler=self._onSpellOnOff)
        super().Clear()

    def SetCursorPosition(self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        self.textEditor.SetSelection(position, position)
        self.textEditor.ScrollLineToCursor()

    def GetCursorPosition(self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        return self.textEditor.GetCurrentPosition()

    def Print(self):
        self.textEditor.Print()

    def onPreferencesDialogClose(self, prefDialog):
        self.textEditor.setDefaultSettings()

    def UpdateView(self, page):
        self.textEditor.SetText(self._currentpage.content)
        self.textEditor.EmptyUndoBuffer()
        self.textEditor.SetReadOnly(page.readonly)

        reg = page.root.registry.get_page_registry(page)
        try:
            cursor_position = reg.getint(REGISTRY_PAGE_CURSOR_POSITION,
                                         default=0)
            self.SetCursorPosition(cursor_position)
        except (KeyError, ValueError):
            pass

        self.textEditor.SetFocus()

    def __createGui(self):
        self.textEditor = TextPageEditor(self)

        mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
        mainSizer.Add(self.textEditor, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

    def onAttachmentPaste(self, fnames):
        text = self._getAttachString(fnames)
        self.textEditor.AddText(text)
        self.textEditor.SetFocus()

    def GetContentFromGui(self):
        return self.textEditor.GetText()

    def GetSearchPanel(self):
        return self.textEditor.searchPanel

    def _isEnabledTool(self, tool):
        return True

    def _onSpellOnOff(self, event):
        self.textEditor.setDefaultSettings()
