#!/usr/bin/env python
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

    
    def Print (self):
        self.textEditor.Print()

    
    def onPreferencesDialogClose (self, prefDialog):
        self.textEditor.setDefaultSettings()
    

    def UpdateView (self, page):
        self.textEditor.SetText (self._currentpage.content)
        self.textEditor.EmptyUndoBuffer()
        self.textEditor.SetReadOnly (page.readonly)
    

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
        return  self.textEditor.GetText()


    def GetSearchPanel (self):
        return self.textEditor.searchPanel


    def _isEnabledTool (self, tool):
        return True
