# -*- coding: utf-8 -*-

import math
from datetime import datetime, timedelta
import os.path

import wx
import wx.lib.newevent

import outwiker.core.system
from outwiker.core.application import Application
from outwiker.core.spellchecker import SpellChecker
from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from outwiker.core.events import EditorPopupMenuParams
from outwiker.gui.controls.texteditorbase import TextEditorBase
from outwiker.gui.guiconfig import EditorConfig
from outwiker.gui.texteditormenu import TextEditorMenu
from outwiker.core.events import EditorStyleNeededParams


ApplyStyleEvent, EVT_APPLY_STYLE = wx.lib.newevent.NewEvent()


class TextEditor(TextEditorBase):
    _fontConfigSection = "Font"

    def __init__(self, parent, *args, **kwds):
        super(TextEditor, self).__init__(parent)

        self._config = EditorConfig(Application.config)

        self._enableSpellChecking = True
        self._spellChecker = None

        self.SPELL_ERROR_INDICATOR = 0

        self._spellErrorText = None
        self._spellSuggestList = []

        self._spellMaxSuggest = 10
        self._suggestMenuItems = []
        self._spellStartByteError = -1
        self._spellEndByteError = -1

        # Уже были установлены стили текста(раскраска)
        self._styleSet = False

        self.__stylebytes = None
        self.__indicatorsbytes = None

        # Начинаем раскраску кода не менее чем через это время
        # с момента его изменения
        self._DELAY = timedelta(milliseconds=300)

        # Время последней модификации текста страницы.
        # Используется для замера времени после модификации,
        # чтобы не парсить текст после каждой введенной буквы
        self._lastEdit = datetime.now() - self._DELAY * 2

        self.__showlinenumbers = self._config.lineNumbers.value

        self.setDefaultSettings()
        self.__bindEvents()

    def __bindEvents(self):
        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onCopyFromEditor,
                           id=wx.ID_COPY)
        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onCutFromEditor,
                           id=wx.ID_CUT)
        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onPasteToEditor,
                           id=wx.ID_PASTE)
        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onUndo,
                           id=wx.ID_UNDO)
        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onRedo,
                           id=wx.ID_REDO)
        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onSelectAll,
                           id=wx.ID_SELECTALL)

        self.textCtrl.Bind(wx.EVT_CONTEXT_MENU, self.__onContextMenu)

        # self.textCtrl.Bind(wx.stc.EVT_STC_STYLENEEDED, self._onStyleNeeded)
        self.textCtrl.Bind(wx.EVT_IDLE, self._onStyleNeeded)
        self.Bind(EVT_APPLY_STYLE, self._onApplyStyle)

        # При перехвате этого сообщения в других классах,
        # нужно вызывать event.Skip(), чтобы это сообщение дошло сюда
        self.textCtrl.Bind(wx.stc.EVT_STC_CHANGE, self.__onChange)

    @property
    def config(self):
        return self._config

    @property
    def enableSpellChecking(self):
        return self._enableSpellChecking

    @enableSpellChecking.setter
    def enableSpellChecking(self, value):
        self._enableSpellChecking = value
        self._styleSet = False

    def __onChange(self, event):
        self._styleSet = False
        self._lastEdit = datetime.now()
        self.__setMarginWidth(self.textCtrl)

    def __onCopyFromEditor(self, event):
        self.textCtrl.Copy()

    def __onCutFromEditor(self, event):
        self.textCtrl.Cut()

    def __onPasteToEditor(self, event):
        self.textCtrl.Paste()

    def __onUndo(self, event):
        self.textCtrl.Undo()

    def __onRedo(self, event):
        self.textCtrl.Redo()

    def __onSelectAll(self, event):
        self.textCtrl.SelectAll()

    def setDefaultSettings(self):
        """
        Установить стили и настройки по умолчанию в контрол StyledTextCtrl
        """
        self._setDefaultSettings()
        self._spellChecker = self.getSpellChecker()

        size = self._config.fontSize.value
        faceName = self._config.fontName.value
        isBold = self._config.fontIsBold.value
        isItalic = self._config.fontIsItalic.value
        fontColor = self._config.fontColor.value
        backColor = self._config.backColor.value

        self.__showlinenumbers = self._config.lineNumbers.value

        self.textCtrl.StyleSetSize(wx.stc.STC_STYLE_DEFAULT, size)
        self.textCtrl.StyleSetFaceName(wx.stc.STC_STYLE_DEFAULT, faceName)
        self.textCtrl.StyleSetBold(wx.stc.STC_STYLE_DEFAULT, isBold)
        self.textCtrl.StyleSetItalic(wx.stc.STC_STYLE_DEFAULT, isItalic)
        self.textCtrl.StyleSetForeground(wx.stc.STC_STYLE_DEFAULT, fontColor)
        self.textCtrl.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT, backColor)

        self.textCtrl.SetCaretForeground(fontColor)
        self.textCtrl.SetCaretLineBack(backColor)

        self._setDefaultHotKeys()

        self.__setMarginWidth(self.textCtrl)
        self.textCtrl.SetTabWidth(self._config.tabWidth.value)

        self.enableSpellChecking = self._config.spellEnabled.value
        self._spellChecker.skipWordsWithNumbers = self.config.spellSkipDigits.value

        self.textCtrl.IndicatorSetStyle(self.SPELL_ERROR_INDICATOR,
                                        wx.stc.STC_INDIC_SQUIGGLE)
        self.textCtrl.IndicatorSetForeground(self.SPELL_ERROR_INDICATOR, "red")
        self._styleSet = False

    def _setDefaultHotKeys(self):
        self.textCtrl.CmdKeyClearAll()

        # Code from Wikidpad sources
        # Default mapping based on Scintilla's "KeyMap.cxx" file
        defaultHotKeys = (
            (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_NORM,     wx.stc.STC_CMD_LINEDOWN),
            (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_LINEDOWNEXTEND),
            (wx.stc.STC_KEY_DOWN,        wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_LINESCROLLDOWN),
            (wx.stc.STC_KEY_UP,          wx.stc.STC_SCMOD_NORM,     wx.stc.STC_CMD_LINEUP),
            (wx.stc.STC_KEY_UP,          wx.stc.STC_SCMOD_SHIFT,    wx.stc.STC_CMD_LINEUPEXTEND),
            (wx.stc.STC_KEY_UP,          wx.stc.STC_SCMOD_CTRL,     wx.stc.STC_CMD_LINESCROLLUP),
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

        map(lambda key: self.textCtrl.CmdKeyAssign(key[0], key[1], key[2]),
            defaultHotKeys)

        if self._config.homeEndKeys.value == EditorConfig.HOME_END_OF_LINE:
            # Клавиши Home / End переносят курсор на начало / конец строки
            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_HOME,
                                       0,
                                       wx.stc.STC_CMD_HOMEDISPLAY)

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_HOME,
                                       wx.stc.STC_SCMOD_ALT,
                                       wx.stc.STC_CMD_HOME)

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_END,
                                       0,
                                       wx.stc.STC_CMD_LINEENDDISPLAY)

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_END,
                                       wx.stc.STC_SCMOD_ALT,
                                       wx.stc.STC_CMD_LINEEND)
        else:
            # Клавиши Home / End переносят курсор на начало / конец абзаца
            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_HOME,
                                       0,
                                       wx.stc.STC_CMD_HOME)

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_HOME,
                                       wx.stc.STC_SCMOD_ALT,
                                       wx.stc.STC_CMD_HOMEDISPLAY)

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_END,
                                       0,
                                       wx.stc.STC_CMD_LINEEND)

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_END,
                                       wx.stc.STC_SCMOD_ALT,
                                       wx.stc.STC_CMD_LINEENDDISPLAY)

    def __setMarginWidth(self, editor):
        """
        Установить размер левой области, где пишутся номера строк в
        зависимости от шрифта
        """
        if self.__showlinenumbers:
            editor.SetMarginWidth(0, self.__getMarginWidth())
            editor.SetMarginWidth(1, 5)
        else:
            editor.SetMarginWidth(0, 0)
            editor.SetMarginWidth(1, 8)

    def __getMarginWidth(self):
        """
        Расчет размера серой области с номером строк
        """
        fontSize = self._config.fontSize.value
        linescount = len(self.GetText().split("\n"))

        if linescount == 0:
            width = 10
        else:
            # Количество десятичных цифр в числе строк
            digits = int(math.log10(linescount) + 1)
            width = int(1.2 * fontSize * digits)

        return width

    def runSpellChecking(self, stylelist, fullText, start, end):
        errors = self._spellChecker.findErrors(fullText[start: end])

        for word, err_start, err_end in errors:
            self._helper.setSpellError(stylelist,
                                       fullText,
                                       err_start + start,
                                       err_end + start)

    def _onStyleNeeded(self, event):
        if (not self._styleSet and
                datetime.now() - self._lastEdit >= self._DELAY):
            page = Application.selectedPage
            text = self._getTextForParse()
            params = EditorStyleNeededParams(self,
                                             text,
                                             self._enableSpellChecking)
            Application.onEditorStyleNeeded(page, params)
            self._styleSet = True

    def _onApplyStyle(self, event):
        if event.text == self._getTextForParse():
            startByte = self._helper.calcBytePos(event.text, event.start)
            endByte = self._helper.calcBytePos(event.text, event.end)
            lenBytes = endByte - startByte

            textlength = self._helper.calcByteLen(event.text)
            self.__stylebytes = [0] * textlength

            if event.stylebytes is not None:
                self.__stylebytes = event.stylebytes

            if event.indicatorsbytes is not None:
                self.__stylebytes = [item1 | item2
                                     for item1, item2
                                     in zip(self.__stylebytes,
                                            event.indicatorsbytes)]

            stylebytesstr = "".join([chr(byte) for byte in self.__stylebytes])


            if event.stylebytes is not None:
                self.textCtrl.StartStyling(startByte,
                                           0xff ^ wx.stc.STC_INDICS_MASK)
                self.textCtrl.SetStyleBytes(lenBytes,
                                            stylebytesstr[startByte:endByte])

            if event.indicatorsbytes is not None:
                self.textCtrl.StartStyling(startByte, wx.stc.STC_INDICS_MASK)
                self.textCtrl.SetStyleBytes(lenBytes,
                                            stylebytesstr[startByte:endByte])

            self._styleSet = True

    def getSpellChecker(self):
        langlist = self._getDictsFromConfig()
        spellDirList = outwiker.core.system.getSpellDirList()

        spellChecker = SpellChecker(Application, langlist, spellDirList)
        spellChecker.addCustomDict(os.path.join(spellDirList[-1], CUSTOM_DICT_FILE_NAME))

        return spellChecker

    def _getDictsFromConfig(self):
        dictsStr = self._config.spellCheckerDicts.value
        return [item.strip()
                for item
                in dictsStr.split(',')
                if item.strip()]

    def __onContextMenu(self, event):
        point = self.textCtrl.ScreenToClient(event.GetPosition())
        pos_byte = self.textCtrl.PositionFromPoint(point)

        popupMenu = TextEditorMenu()
        self._appendSpellMenuItems(popupMenu, pos_byte)

        Application.onEditorPopupMenu(
            Application.selectedPage,
            EditorPopupMenuParams(self, popupMenu, point, pos_byte)
        )

        self.textCtrl.PopupMenu(popupMenu)
        popupMenu.Destroy()

    def getCachedStyleBytes(self):
        return self.__stylebytes

    def __onAddWordToDict(self, event):
        if self._spellErrorText is not None:
            self.__addWordToDict(self._spellErrorText)

    def __onAddWordLowerToDict(self, event):
        if self._spellErrorText is not None:
            self.__addWordToDict(self._spellErrorText.lower())

    def __addWordToDict(self, word):
        self._spellChecker.addToCustomDict(0, word)
        self._spellErrorText = None
        self._styleSet = False

    def _appendSpellMenuItems(self, menu, pos_byte):
        stylebytes = self.getCachedStyleBytes()
        if stylebytes is None:
            return

        stylebytes_len = len(stylebytes)

        if (stylebytes is None or
                pos_byte >= stylebytes_len or
                stylebytes[pos_byte] & self._helper.SPELL_ERROR_INDICATOR_MASK == 0):
            return

        endSpellError = startSpellError = pos_byte

        while (startSpellError >= 0 and
               stylebytes[startSpellError] & self._helper.SPELL_ERROR_INDICATOR_MASK != 0):
            startSpellError -= 1

        while (endSpellError < stylebytes_len and
               stylebytes[endSpellError] & self._helper.SPELL_ERROR_INDICATOR_MASK != 0):
            endSpellError += 1

        self._spellStartByteError = startSpellError + 1
        self._spellEndByteError = endSpellError
        self._spellErrorText = self.textCtrl.GetTextRange(
            self._spellStartByteError,
            self._spellEndByteError)

        self._spellSuggestList = self._spellChecker.getSuggest(self._spellErrorText)[:self._spellMaxSuggest]

        menu.AppendSeparator()
        self._suggestMenuItems = menu.AppendSpellSubmenu(self._spellErrorText,
                                                         self._spellSuggestList)

        for menuItem in self._suggestMenuItems:
            self.textCtrl.Bind(wx.EVT_MENU, self.__onSpellSuggest, menuItem)

        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onAddWordToDict,
                           id=menu.ID_ADD_WORD)

        self.textCtrl.Bind(wx.EVT_MENU,
                           self.__onAddWordLowerToDict,
                           id=menu.ID_ADD_WORD_LOWER)

    def __onSpellSuggest(self, event):
        word = event.GetEventObject().GetLabelText(event.GetId())

        self.textCtrl.SetSelection(self._spellStartByteError,
                                   self._spellEndByteError)
        self.textCtrl.ReplaceSelection(word)
