# -*- coding: utf-8 -*-

import codecs
import cgi

import wx
import wx.lib.newevent
from wx.stc import StyledTextCtrl

import outwiker.core.system
from outwiker.core.textprinter import TextPrinter
from outwiker.gui.searchreplacecontroller import SearchReplaceController
from outwiker.gui.searchreplacepanel import SearchReplacePanel
from outwiker.gui.texteditorhelper import TextEditorHelper


class TextEditorBase(wx.Panel):
    '''
    Added in outwiker.gui 1.3
    '''
    def __init__(self, parent):
        super(TextEditorBase, self).__init__(parent, style=0)
        self.textCtrl = StyledTextCtrl(self, -1)

        # Создание панели поиска и ее контроллера
        self._searchPanel = SearchReplacePanel(self)
        self._searchPanelController = SearchReplaceController(
            self._searchPanel,
            self)
        self._searchPanel.setController(self._searchPanelController)

        self._do_layout()

        self.__createCoders()
        self._helper = TextEditorHelper()
        self._bind()
        self._setDefaultSettings()

    def _bind(self):
        self.textCtrl.Bind(wx.EVT_KEY_DOWN, self.__onKeyDown)
        # self.textCtrl.Bind(wx.EVT_CHAR, self.__OnChar_ImeWorkaround)
        # self.textCtrl.Bind(wx.EVT_CHAR, self.__onChar)
        # self.textCtrl.Bind(wx.EVT_CHAR_HOOK, self.__onCharHook)
        # self.textCtrl.Bind(wx.stc.EVT_STC_CHARADDED, self.__onCharAdded)
        # self.textCtrl.Bind(wx.stc.EVT_STC_KEY, self.__onStcKey)

    def _do_layout(self):
        mainSizer = wx.FlexGridSizer(rows=2, cols=0, vgap=0, hgap=0)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        mainSizer.Add(self.textCtrl, 0, wx.EXPAND, 0)
        mainSizer.Add(self._searchPanel, 0, wx.EXPAND, 0)
        self.SetSizer(mainSizer)

        self._searchPanel.Hide()
        self.Layout()

    def __createCoders(self):
        encoding = outwiker.core.system.getOS().inputEncoding
        self.mbcsEnc = codecs.getencoder(encoding)

    # def __onStcKey(self, event):
    #     print '__onStcKey'

    # def __onCharAdded(self, event):
    #     print '__onCharAdded'
        # print type(event)
        # print dir(event)
        # from outwiker.core.application import Application
        # wx.PostEvent(Application.mainWindow, event)
        # event.StopPropagation()

    # def __onChar(self, event):
    #     print '__onChar'
    #     event.Skip()

    # def __onCharHook(self, event):
    #     print '__onCharHook'
        # key = event.GetKeyCode()
        # print key
        # event.ResumePropagation(20)
        # event.Skip()
        # event.DoAllowNextEvent()
        # event.Skip()
        # from outwiker.core.application import Application
        # wx.PostEvent(Application.mainWindow, event)

    def __onKeyDown(self, event):
        # print '__onKeyDown'
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self._searchPanel.Close()

        event.Skip()

    # def __OnChar_ImeWorkaround(self, evt):
    #     """
    #     Обработка клавиш вручную, чтобы не было проблем с вводом русских букв в Linux.
    #     Основа кода взята из Wikidpad (WikiTxtCtrl.py -> OnChar_ImeWorkaround)
    #     """
    #     print '__OnChar_ImeWorkaround'
    #     key = evt.GetKeyCode()
    #
    #     # Return if this doesn't seem to be a real character input
    #     if evt.ControlDown() or (0 < key < 32):
    #         evt.Skip()
    #         return
    #
    #     if key >= wx.WXK_START and evt.GetUnicodeKey() != key:
    #         evt.Skip()
    #         return
    #
    #     unichar = unichr(evt.GetUnicodeKey())
    #
    #     self.textCtrl.ReplaceSelection(self.mbcsEnc (unichar, "replace")[0])

    def _setDefaultSettings(self):
        self.textCtrl.SetEndAtLastLine(False)
        self.textCtrl.StyleClearAll()
        self.textCtrl.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.textCtrl.SetWrapVisualFlags(wx.stc.STC_WRAPVISUALFLAG_END)
        self.textCtrl.SetTabWidth(4)
        self._setDefaultHotKeys()

    def _setDefaultHotKeys(self):
        self.textCtrl.CmdKeyClearAll()

        # Clear Cmd keys for Ubuntu
        for key in list(range(ord('A'), ord('Z') + 1)) + list(range(ord('0'), ord('9') + 1)):
            self.textCtrl.CmdKeyClear(key, wx.stc.STC_SCMOD_ALT | wx.stc.STC_SCMOD_CTRL)
            self.textCtrl.CmdKeyClear(key, wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT | wx.stc.STC_SCMOD_CTRL)

        self.textCtrl.CmdKeyClear(wx.stc.STC_KEY_UP, wx.stc.STC_SCMOD_CTRL)
        self.textCtrl.CmdKeyClear(wx.stc.STC_KEY_DOWN, wx.stc.STC_SCMOD_CTRL)

        # Code from Wikidpad sources
        # Default mapping based on Scintilla's "KeyMap.cxx" file
        defaultHotKeys = (
            (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_NORM,     wx.stc.STC_CMD_LINEDOWN),
            (wx.stc.STC_KEY_UP,          wx.stc.STC_SCMOD_NORM,     wx.stc.STC_CMD_LINEUP),
            # (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_LINESCROLLDOWN),
            # (wx.stc.STC_KEY_UP,          wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_LINESCROLLUP),
            (wx.stc.STC_KEY_UP,          wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_LINEUPEXTEND),
            (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_LINEDOWNEXTEND),

            (ord('['),            wx.stc.STC_SCMOD_CTRL,            wx.stc.STC_CMD_PARAUP),
            (ord('['),            wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_PARAUPEXTEND),
            (ord(']'),            wx.stc.STC_SCMOD_CTRL,        wx.stc.STC_CMD_PARADOWN),
            (ord(']'),            wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_PARADOWNEXTEND),
            (wx.stc.STC_KEY_LEFT,        wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_CHARLEFT),
            (wx.stc.STC_KEY_LEFT,        wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_CHARLEFTEXTEND),
            # (wx.stc.STC_KEY_LEFT,        wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_WORDLEFT),
            # (wx.stc.STC_KEY_LEFT,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_WORDLEFTEXTEND),
            (wx.stc.STC_KEY_RIGHT,        wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_CHARRIGHT),
            (wx.stc.STC_KEY_RIGHT,        wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_CHARRIGHTEXTEND),
            # (wx.stc.STC_KEY_RIGHT,        wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_WORDRIGHT),
            # (wx.stc.STC_KEY_RIGHT,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_WORDRIGHTEXTEND),
            (ord('/'),        wx.stc.STC_SCMOD_CTRL,        wx.stc.STC_CMD_WORDPARTLEFT),
            (ord('/'),        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_WORDPARTLEFTEXTEND),
            (ord('\\'),        wx.stc.STC_SCMOD_CTRL,        wx.stc.STC_CMD_WORDPARTRIGHT),
            (ord('\\'),        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_WORDPARTRIGHTEXTEND),
            (wx.stc.STC_KEY_HOME,        wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_VCHOME),
            (wx.stc.STC_KEY_HOME,         wx.stc.STC_SCMOD_SHIFT,     wx.stc.STC_CMD_VCHOMEEXTEND),
            (wx.stc.STC_KEY_HOME,         wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_DOCUMENTSTART),
            (wx.stc.STC_KEY_HOME,         wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_DOCUMENTSTARTEXTEND),
            (wx.stc.STC_KEY_HOME,         wx.stc.STC_SCMOD_ALT,     wx.stc.STC_CMD_HOMEDISPLAY),
            (wx.stc.STC_KEY_END,         wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_LINEEND),
            (wx.stc.STC_KEY_END,         wx.stc.STC_SCMOD_SHIFT,     wx.stc.STC_CMD_LINEENDEXTEND),
            (wx.stc.STC_KEY_END,         wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_DOCUMENTEND),
            (wx.stc.STC_KEY_END,         wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_DOCUMENTENDEXTEND),
            (wx.stc.STC_KEY_END,         wx.stc.STC_SCMOD_ALT,     wx.stc.STC_CMD_LINEENDDISPLAY),
            (wx.stc.STC_KEY_PRIOR,        wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_PAGEUP),
            (wx.stc.STC_KEY_PRIOR,        wx.stc.STC_SCMOD_SHIFT,     wx.stc.STC_CMD_PAGEUPEXTEND),
            (wx.stc.STC_KEY_NEXT,         wx.stc.STC_SCMOD_NORM,     wx.stc.STC_CMD_PAGEDOWN),
            (wx.stc.STC_KEY_NEXT,         wx.stc.STC_SCMOD_SHIFT,     wx.stc.STC_CMD_PAGEDOWNEXTEND),
            (wx.stc.STC_KEY_DELETE,     wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_CLEAR),
            (wx.stc.STC_KEY_INSERT,         wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_EDITTOGGLEOVERTYPE),
            (wx.stc.STC_KEY_ESCAPE,      wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_CANCEL),
            (wx.stc.STC_KEY_BACK,        wx.stc.STC_SCMOD_NORM,     wx.stc.STC_CMD_DELETEBACK),
            (wx.stc.STC_KEY_BACK,        wx.stc.STC_SCMOD_SHIFT,     wx.stc.STC_CMD_DELETEBACK),
            (wx.stc.STC_KEY_BACK,         wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_UNDO),
            (ord('Z'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_UNDO),
            (ord('Y'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_REDO),
            (ord('A'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_SELECTALL),

            (wx.stc.STC_KEY_INSERT,             wx.stc.STC_SCMOD_CTRL | wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_COPY),
            (wx.stc.STC_KEY_INSERT,             wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_PASTE),
            (ord('C'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_COPY),
            (ord('X'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_CUT),
            (ord('V'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_PASTE),

            (wx.stc.STC_KEY_TAB,        wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_TAB),
            (wx.stc.STC_KEY_TAB,        wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_BACKTAB),
            (wx.stc.STC_KEY_RETURN,     wx.stc.STC_SCMOD_NORM,    wx.stc.STC_CMD_NEWLINE),
            (wx.stc.STC_KEY_RETURN,     wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_NEWLINE),
            (wx.stc.STC_KEY_ADD,         wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_ZOOMIN),
            (wx.stc.STC_KEY_SUBTRACT,    wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_ZOOMOUT),
            (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_LINEDOWNRECTEXTEND),
            (wx.stc.STC_KEY_UP,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_LINEUPRECTEXTEND),
            (wx.stc.STC_KEY_LEFT,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_CHARLEFTRECTEXTEND),
            (wx.stc.STC_KEY_RIGHT,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_CHARRIGHTRECTEXTEND),
            (wx.stc.STC_KEY_HOME,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_VCHOMERECTEXTEND),
            (wx.stc.STC_KEY_END,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_LINEENDRECTEXTEND),
            (wx.stc.STC_KEY_PRIOR,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_PAGEUPRECTEXTEND),
            (wx.stc.STC_KEY_NEXT,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_ALT,    wx.stc.STC_CMD_PAGEDOWNRECTEXTEND),

            # (wx.stc.STC_KEY_DELETE,    wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_DELLINERIGHT),
            # (wx.stc.STC_KEY_BACK,        wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_DELLINELEFT),
            # (wx.stc.STC_KEY_BACK,        wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_DELWORDLEFT),
            # (wx.stc.STC_KEY_DELETE,     wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_DELWORDRIGHT),
            # (wx.stc.STC_KEY_DIVIDE,    wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_SETZOOM),
            #        (ord('L'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_LINECUT),
            #        (ord('L'),             wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_LINEDELETE),
            #        (ord('T'),             wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_LINECOPY),
            #        (ord('T'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_LINETRANSPOSE),
            #        (ord('D'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_SELECTIONDUPLICATE),
            #        (ord('U'),             wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_LOWERCASE),
            #        (ord('U'),             wx.stc.STC_SCMOD_SHIFT | wx.stc.STC_SCMOD_CTRL,    wx.stc.STC_CMD_UPPERCASE),
        )

        list(map(lambda key: self.textCtrl.CmdKeyAssign(*key), defaultHotKeys))

    @property
    def searchPanel(self):
        """
        Возвращает контроллер панели поиска
        """
        return self._searchPanelController

    def Print(self):
        selectedtext = self.textCtrl.GetSelectedText()
        text = self.textCtrl.GetText()

        printer = TextPrinter(self)
        printer.printout(text if len(selectedtext) == 0 else selectedtext)

    def getPosChar(self, posBytes):
        return len(self.textCtrl.GetTextRange(0, posBytes))

    def AddText(self, text):
        self.textCtrl.AddText(text)

    def replaceText(self, text):
        self.textCtrl.ReplaceSelection(text)

    def toddleLinePrefix(self, line, prefix):
        """
        If line with number "line" starts with prefix, prefix will be removed
        else prefix will be added.

        Added in OutWiker 2.0.0.795.
        """
        assert line < self.GetLineCount()
        line_text = self.GetLine(line)
        if line_text.startswith(prefix):
            line_text = line_text[len(prefix):]
        else:
            line_text = prefix + line_text
        self.SetLine(line, line_text)

    def toddleSelectedLinesPrefix(self, prefix):
        """
        Apply toddleLinePrefix method to selected lines

        Added in OutWiker 2.0.0.795.
        """
        self.BeginUndoAction()
        old_sel_start = self.GetSelectionStart()
        old_sel_end = self.GetSelectionEnd()

        first_line, last_line = self.GetSelectionLines()
        list(map(lambda n: self.toddleLinePrefix(n, prefix),
            range(first_line, last_line + 1)))

        if old_sel_start != old_sel_end:
            new_sel_start = self.GetLineStartPosition(first_line)
            new_sel_end = self.GetLineEndPosition(last_line)
        else:
            new_sel_start = new_sel_end = self.GetLineEndPosition(last_line)

        self.SetSelection(new_sel_start, new_sel_end)
        self.EndUndoAction()

    def turnText(self, lefttext, righttext):
        selText = self.textCtrl.GetSelectedText()
        newtext = lefttext + selText + righttext
        self.textCtrl.ReplaceSelection(newtext)

        currPos = self.GetSelectionEnd()
        if len(selText) == 0:
            """
            Если не оборачиваем текст, а делаем пустой тег, то поместим каретку до закрывающегося тега
            """
            newpos = currPos - len(righttext)
            self.SetSelection(newpos, newpos)
        else:
            self.SetSelection(currPos - len(selText) - len(righttext),
                              currPos - len(righttext))

    def escapeHtml(self):
        selText = self.textCtrl.GetSelectedText()
        text = cgi.escape(selText, quote=False)
        self.textCtrl.ReplaceSelection(text)

    def SetReadOnly(self, readonly):
        self.textCtrl.SetReadOnly(readonly)

    def GetReadOnly(self):
        return self.textCtrl.GetReadOnly()

    def GetText(self):
        return self.textCtrl.GetText()

    def SetText(self, text):
        self.textCtrl.SetText(text)

    def EmptyUndoBuffer(self):
        self.textCtrl.EmptyUndoBuffer()

    def GetSelectedText(self):
        return self.textCtrl.GetSelectedText()

    def GetCurrentLine(self):
        return self.textCtrl.GetCurrentLine()

    def ScrollToLine(self, line):
        self.textCtrl.ScrollToLine(line)

    def SetSelection(self, start, end):
        """
        start и end в символах, а не в байтах, в отличие от исходного
        StyledTextCtrl
        """
        startText = self.GetText()[:start]
        endText = self.GetText()[:end]

        firstByte = self._helper.calcByteLen(startText)
        endByte = self._helper.calcByteLen(endText)

        self.textCtrl.SetSelection(firstByte, endByte)

    def GotoPos(self, pos):
        pos_bytes = self._helper.calcBytePos(self.GetText(), pos)
        self.textCtrl.GotoPos(pos_bytes)

    def GetCurrentPosition(self):
        """
        Возвращает номер символа(а не байта), перед которых находится курсор
        """
        return self._calcCharPos(self.textCtrl.GetCurrentPos())

    def GetSelectionStart(self):
        """
        Возвращает позицию начала выбранной области в символах, а не в байтах
        """
        return self._calcCharPos(self.textCtrl.GetSelectionStart())

    def GetSelectionLines(self):
        """
        Return tuple (first selected line, last selected line)

        Added in OutWiker 2.0.0.795.
        """
        start_bytes = self.textCtrl.GetSelectionStart()
        end_bytes = self.textCtrl.GetSelectionEnd()
        return (self.textCtrl.LineFromPosition(start_bytes),
                self.textCtrl.LineFromPosition(end_bytes))

    def GetSelectionEnd(self):
        """
        Возвращает позицию конца выбранной области в символах, а не в байтах
        """
        return self._calcCharPos(self.textCtrl.GetSelectionEnd())

    def SetFocus(self):
        self.textCtrl.SetFocus()
        self.textCtrl.SetSTCFocus(True)

    def GetLine(self, line):
        """
        Return line with the "line" number. \n included.
        Added in OutWiker 2.0.0.795
        """
        return self.textCtrl.GetLine(line)

    def SetLine(self, line, newline):
        """
        Replace line with the number "line" newline.
        Newline will be ended with "\n" else line will be joined with next line

        Added in OutWiker 2.0.0.795
        """
        linecount = self.GetLineCount()
        assert line < linecount

        line_start_bytes = self.textCtrl.PositionFromLine(line)
        line_end_bytes = self.textCtrl.PositionFromLine(line + 1)
        self.textCtrl.Replace(line_start_bytes, line_end_bytes, newline)

    def GetLineCount(self):
        return self.textCtrl.GetLineCount()

    def GetLineStartPosition(self, line):
        """
        Retrieve the position at the start of a line in symbols (not bytes)

        Added in OutWiker 2.0.0.795
        """
        return self._calcCharPos(self.textCtrl.PositionFromLine(line))

    def GetLineEndPosition(self, line):
        """
        Get the position after the last visible characters on a line
            in symbols (not bytes)

        Added in OutWiker 2.0.0.795
        """
        return self._calcCharPos(self.textCtrl.GetLineEndPosition(line))

    def MoveSelectedLinesUp(self):
        """
        Move the selected lines up one line,
        shifting the line above after the selection.

        Added in OutWiker 2.0.0.795
        """
        self.textCtrl.MoveSelectedLinesUp()

    def MoveSelectedLinesDown(self):
        """
        Move the selected lines down one line,
        shifting the line below before the selection.

        Added in OutWiker 2.0.0.795
        """
        self.textCtrl.MoveSelectedLinesDown()

    def LineDuplicate(self):
        """
        Duplicate the current line.

        Added in OutWiker 2.0.0.795
        """
        self.textCtrl.LineDuplicate()

    def LineDelete(self):
        """
        Delete the current line.

        Added in OutWiker 2.0.0.795
        """
        self.textCtrl.LineDelete()

    def BeginUndoAction(self):
        """
        Added in OutWiker 2.0.0.797
        """
        self.textCtrl.BeginUndoAction()

    def EndUndoAction(self):
        """
        Added in OutWiker 2.0.0.797
        """
        self.textCtrl.EndUndoAction()

    def JoinLines(self):
        """
        Join selected lines

        Added in OutWiker 2.0.0.797
        """
        first_line, last_line = self.GetSelectionLines()
        if first_line != last_line:
            last_line -= 1

        self.BeginUndoAction()

        for _ in range(first_line, last_line + 1):
            line = self.GetLine(first_line).replace(u'\r\n', u'\n')
            if line.endswith(u'\n'):
                newline = line[:-1]
                self.SetLine(first_line, newline)

        new_sel_pos = self.GetLineEndPosition(first_line)
        self.SetSelection(new_sel_pos, new_sel_pos)

        self.EndUndoAction()

    def DelWordLeft(self):
        """
        Added in OutWiker 2.0.0.797
        """
        self.textCtrl.DelWordLeft()

    def DelWordRight(self):
        """
        Added in OutWiker 2.0.0.797
        """
        self.textCtrl.DelWordRight()

    def DelLineLeft(self):
        """
        Delete back from the current position to the start of the line

        Added in OutWiker 2.0.0.797
        """
        self.textCtrl.DelLineLeft()

    def DelLineRight(self):
        """
        Delete forwards from the current position to the end of the line

        Added in OutWiker 2.0.0.797
        """
        self.textCtrl.DelLineRight()

    def WordLeft(self):
        """
        Added in outwiker.gui 1.2
        """
        self.textCtrl.WordLeft()

    def WordRight(self):
        """
        Added in outwiker.gui 1.2
        """
        self.textCtrl.WordRight()

    def WordLeftEnd(self):
        """
        Added in outwiker.gui 1.2
        """
        self.textCtrl.WordLeftEnd()

    def WordRightEnd(self):
        """
        Added in outwiker.gui 1.2
        """
        self.textCtrl.WordRightEnd()

    def WordLeftExtend(self):
        """
        Added in outwiker.gui 1.2
        """
        self.textCtrl.WordLeftExtend()

    def WordRightExtend(self):
        """
        Added in outwiker.gui 1.2
        """
        self.textCtrl.WordRightExtend()

    def GotoWordStart(self):
        """
        Added in outwiker.gui 1.2
        """
        self.WordRight()
        self.WordLeft()

    def GotoWordEnd(self):
        """
        Added in outwiker.gui 1.2
        """
        self.WordLeftEnd()
        self.WordRightEnd()

    def ScrollLineToCursor(self):
        """
        Added in outwiker.gui 1.1
        """
        maxlines = self.textCtrl.LinesOnScreen()
        line = self.GetCurrentLine()
        if line >= maxlines:
            delta = min(10, maxlines / 3)
            line -= delta
            if line < 0:
                line = 0
            self.ScrollToLine(line)

    def WordStartPosition(self, pos):
        """
        Added in outwiker.gui 1.2
        """
        pos_bytes = self._helper.calcBytePos(self.GetText(), pos)
        result_bytes = self.textCtrl.WordStartPosition(pos_bytes, True)
        return self.getPosChar(result_bytes)

    def WordEndPosition(self, pos):
        """
        Added in outwiker.gui 1.2
        """
        pos_bytes = self._helper.calcBytePos(self.GetText(), pos)
        result_bytes = self.textCtrl.WordEndPosition(pos_bytes, True)
        return self.getPosChar(result_bytes)

    def GetWord(self, pos):
        pos_bytes = self._helper.calcBytePos(self.GetText(), pos)
        word_start_bytes = self.textCtrl.WordStartPosition(pos_bytes, True)
        word_end_bytes = self.textCtrl.WordEndPosition(pos_bytes, True)
        word = self.textCtrl.GetTextRange(word_start_bytes, word_end_bytes)
        return word

    def _calcCharPos(self, pos_bytes):
        """
        Пересчет позиции в байтах в позицию в символах
        """
        text_left = self.textCtrl.GetTextRange(0, pos_bytes)
        currpos = len(text_left)
        return currpos

    def _getTextForParse(self):
        # Табуляция в редакторе считается за несколько символов
        return self.textCtrl.GetText().replace("\t", " ")
