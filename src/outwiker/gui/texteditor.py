# -*- coding: utf-8 -*-

import codecs
import os.path
import cgi
import math

import wx
from wx.stc import StyledTextCtrl

import outwiker.core.system
from outwiker.core.application import Application
from .guiconfig import EditorConfig
from outwiker.core.textprinter import TextPrinter
from .editorsearchpanel import EditorSearchPanel
from .mainid import MainId

class TextEditor(wx.Panel):
    _fontConfigSection = "Font"

    def __init__(self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.textCtrl = StyledTextCtrl(self, -1)
        self.searchPanel = EditorSearchPanel(self, -1)

        self.__do_layout()

        self.__createCoders()

        self.config = EditorConfig (Application.config)
        self.__showlinenumbers =  self.config.lineNumbers.value

        self.setDefaultSettings()
        self.searchPanel.setEditor (self, self.textCtrl)

        self.textCtrl.Bind(wx.EVT_MENU, self.__onCopyFromEditor, id = MainId.ID_COPY)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onCutFromEditor, id = MainId.ID_CUT)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onPasteToEditor, id = MainId.ID_PASTE)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onUndo, id = MainId.ID_UNDO)
        self.textCtrl.Bind(wx.EVT_MENU, self.__onRedo, id = MainId.ID_REDO)
        self.textCtrl.Bind (wx.EVT_CHAR, self.__OnChar_ImeWorkaround)
        self.textCtrl.Bind (wx.EVT_KEY_DOWN, self.__onKeyDown)

        # При перехвате этого сообщения в других классах, нужно вызывать event.Skip(), 
        # чтобы это сообщение дошло досюда
        self.textCtrl.Bind (wx.stc.EVT_STC_CHANGE, self.__onChange)


    def __onChange (self, event):
        self.__setMarginWidth (self.textCtrl)


    def Print (self):
        selectedtext = self.textCtrl.GetSelectedText()
        text = self.textCtrl.GetText()

        printer = TextPrinter (self)
        printer.printout (text if len (selectedtext) == 0 else selectedtext)


    def __onCopyFromEditor (self, event):
        self.textCtrl.Copy()


    def __onCutFromEditor (self, event):
        self.textCtrl.Cut()


    def __onPasteToEditor (self, event):
        self.textCtrl.Paste()

    
    def __onUndo (self, event):
        self.textCtrl.Undo()

    
    def __onRedo (self, event):
        self.textCtrl.Redo()


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.Add(self.textCtrl, 1, wx.EXPAND, 0)
        mainSizer.Add(self.searchPanel, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        self.searchPanel.Hide()
        self.Layout()


    def setDefaultSettings (self):
        """
        Установить шрифт по умолчанию в контрол StyledTextCtrl
        """
        size = self.config.fontSize.value
        faceName = self.config.fontName.value
        isBold = self.config.fontIsBold.value
        isItalic = self.config.fontIsItalic.value

        self.__showlinenumbers = self.config.lineNumbers.value

        self.textCtrl.StyleClearAll()

        self.textCtrl.StyleSetSize (wx.stc.STC_STYLE_DEFAULT, size)
        self.textCtrl.StyleSetFaceName (wx.stc.STC_STYLE_DEFAULT, faceName)
        self.textCtrl.StyleSetBold (wx.stc.STC_STYLE_DEFAULT, isBold)
        self.textCtrl.StyleSetItalic (wx.stc.STC_STYLE_DEFAULT, isItalic)

        self.textCtrl.StyleSetSize (0, size)
        self.textCtrl.StyleSetFaceName (0, faceName)
        self.textCtrl.StyleSetBold (0, isBold)
        self.textCtrl.StyleSetItalic (0, isItalic)

        # Заблокируем горячую клавишу Ctrl+D, чтобы использовать ее как добавление закладки
        self.textCtrl.CmdKeyClear (ord ("D"), wx.stc.STC_SCMOD_CTRL)
        self.textCtrl.CmdKeyClear (ord ("R"), wx.stc.STC_SCMOD_CTRL | wx.stc.STC_SCMOD_SHIFT)
        self.textCtrl.SetWrapMode (wx.stc.STC_WRAP_WORD)
        self.textCtrl.SetWrapVisualFlags (wx.stc.STC_WRAPVISUALFLAG_END)

        self.__setMarginWidth (self.textCtrl)
        self.textCtrl.SetTabWidth (self.config.tabWidth.value)


    def __setMarginWidth (self, editor):
        """
        Установить размер левой области, где пишутся номера строк в зависимости от шрифта
        """
        if self.__showlinenumbers:
            editor.SetMarginWidth (0, self.__getMarginWidth())
            editor.SetMarginWidth (1, 5)
        else:
            editor.SetMarginWidth (0, 0)
            editor.SetMarginWidth (1, 8)


    def __getMarginWidth (self):
        """
        Расчет размера серой области с номером строк
        """
        fontSize = self.config.fontSize.value
        linescount = len (self.GetText().split("\n"))

        if linescount == 0:
            width = 10
        else:
            # Количество десятичных цифр в числе строк
            digits = int (math.log10 (linescount) + 1)
            width = int (1.2 * fontSize * digits)

        return width
    

    def calcByteLen(self, text):
        """Посчитать длину строки в байтах, а не в символах"""
        return len(self.encoder(text)[0])


    def calcBytePos (self, text, pos):
        """Преобразовать позицию в символах в позицию в байтах"""
        return len(self.encoder (text[: pos] )[0] )


    def __createCoders (self):
        encoding = outwiker.core.system.getOS().inputEncoding

        self._mbcsDec = codecs.getdecoder(encoding)
        self.mbcsEnc = codecs.getencoder(encoding)
        self.encoder = codecs.getencoder("utf-8")
    

    def __onKeyDown (self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self.searchPanel.Close()

        event.Skip()


    def __OnChar_ImeWorkaround(self, evt):
        """
        Обработка клавиш вручную, чтобы не было проблем с вводом русских букв в Linux.
        Основа кода взята из Wikidpad (WikiTxtCtrl.py -> OnChar_ImeWorkaround)
        """
        key = evt.GetKeyCode()

        # Return if this doesn't seem to be a real character input
        if evt.ControlDown() or (0 < key < 32):
            evt.Skip()
            return

        if key >= wx.WXK_START and evt.GetUnicodeKey() != key:
            evt.Skip()
            return

        unichar = unichr(evt.GetUnicodeKey())

        self.textCtrl.ReplaceSelection(self.mbcsEnc (unichar, "replace")[0])


    def AddText (self, text):
        self.textCtrl.AddText (text)


    def replaceText (self, text):
        self.textCtrl.ReplaceSelection (text)


    def turnText (self, lefttext, righttext):
        selText = self.textCtrl.GetSelectedText()
        newtext = lefttext + selText + righttext
        self.textCtrl.ReplaceSelection (newtext)

        if len (selText) == 0:
            """
            Если не оборачиваем текст, а делаем пустой тег, то поместим каретку до закрывающегося тега
            """
            currPos = self.textCtrl.GetSelectionEnd()
            len_bytes = self.calcByteLen (righttext)

            newPos = currPos - len_bytes

            self.textCtrl.SetSelection (newPos, newPos)


    def escapeHtml (self):
        selText = self.textCtrl.GetSelectedText()
        text = cgi.escape (selText, quote=True)
        self.textCtrl.ReplaceSelection (text)


    def SetReadOnly (self, readonly):
        self.textCtrl.SetReadOnly (readonly)


    def GetText(self):
        return self.textCtrl.GetText()


    def SetText (self, text):
        self.textCtrl.SetText (text)


    def EmptyUndoBuffer (self):
        self.textCtrl.EmptyUndoBuffer()


    def GetSelectedText (self):
        return self.textCtrl.GetSelectedText()


    def SetSelection (self, start, end):
        startText = self.GetText()[:start]
        endText = self.GetText()[:end]

        firstByte = self.calcByteLen (startText)
        endByte = self.calcByteLen (endText)

        self.textCtrl.SetSelection (firstByte, endByte)
