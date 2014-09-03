# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.texteditor import TextEditor
from outwiker.gui.basetextpanel import BaseTextPanel


class TextPanel (BaseTextPanel):
    """
    Класс для представления текстовых страниц
    """

    def __init__ (self, parent, *args, **kwds):
        BaseTextPanel.__init__ (self, parent, *args, **kwds)

        self.__createGui()


    def Clear (self):
        super (TextPanel, self).Clear()


    def SetCursorPosition (self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        self.textEditor.SetSelection (position, position)


    def GetCursorPosition (self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        return self.textEditor.GetCurrentPosition()


    def Print (self):
        self.textEditor.Print()


    def onPreferencesDialogClose (self, prefDialog):
        self.textEditor.setDefaultSettings()


    def UpdateView (self, page):
        self.textEditor.SetText (self._currentpage.content)
        self.textEditor.EmptyUndoBuffer()
        self.textEditor.SetReadOnly (page.readonly)
        self.SetCursorPosition (self._getCursorPositionOption (page).value)
        self.textEditor.SetFocus()


    def __createGui (self):
        self.textEditor = TextEditor(self, -1)

        mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
        mainSizer.Add(self.textEditor, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)


    def onAttachmentPaste (self, fnames):
        text = self._getAttachString (fnames)
        self.textEditor.AddText (text)
        self.textEditor.SetFocus()


    def GetContentFromGui (self):
        return self.textEditor.GetText()


    def GetSearchPanel (self):
        return self.textEditor.searchPanel


    def _isEnabledTool (self, tool):
        return True
