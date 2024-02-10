# -*- coding: utf-8 -*-

import math
from datetime import datetime, timedelta
import os.path
from typing import List

import wx
import wx.lib.newevent

import outwiker.core.system
from outwiker.core.application import Application
from outwiker.core.spellchecker.spellchecker import SpellChecker
from outwiker.core.spellchecker.defines import CUSTOM_DICT_FILE_NAME
from outwiker.core.events import (
    EditorPopupMenuParams,
    TextEditorKeyDownParams,
    TextEditorCaretMoveParams,
)
from outwiker.gui.controls.texteditorbase import TextEditorBase
from outwiker.gui.guiconfig import EditorConfig
from outwiker.gui.texteditormenu import TextEditorMenu
from outwiker.gui.editorfilesdroptarget import EditorFilesDropTarget
from outwiker.core.events import EditorStyleNeededParams


ApplyStyleEvent, EVT_APPLY_STYLE = wx.lib.newevent.NewEvent()


class TextEditor(TextEditorBase):
    _fontConfigSection = "Font"

    def __init__(self, parent):
        super().__init__(parent)
        self.SPELL_ERROR_INDICATOR = wx.stc.STC_INDIC_SQUIGGLE

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

        self._oldStartSelection = None
        self._oldEndSelection = None

        # Уже были установлены стили текста (раскраска)
        self._styleSet = False

        self.__stylebytes = None

        # Начинаем раскраску кода не менее чем через это время
        # с момента его изменения
        self._DELAY = timedelta(milliseconds=300)

        # Время последней модификации текста страницы.
        # Используется для замера времени после модификации,
        # чтобы не парсить текст после каждой введенной буквы
        self._lastEdit = datetime.now() - self._DELAY * 2

        self.__showlinenumbers = self._config.lineNumbers.value
        self.dropTarget = EditorFilesDropTarget(Application, self)

        self.setDefaultSettings()
        self.__bindEvents()

    def __bindEvents(self):
        self.textCtrl.Bind(wx.EVT_CONTEXT_MENU, self.__onContextMenu)
        self.textCtrl.Bind(wx.EVT_IDLE, self._onStyleNeeded)
        self.textCtrl.Bind(wx.EVT_LEFT_DOWN, self._onMouseLeftDown)
        self.textCtrl.Bind(wx.EVT_LEFT_UP, self._onMouseLeftUp)
        self.textCtrl.Bind(wx.EVT_KEY_UP, self._onKeyUp)

        self.Bind(EVT_APPLY_STYLE, self._onApplyStyle)

        # При перехвате этого сообщения в других классах,
        # нужно вызывать event.Skip(), чтобы это сообщение дошло сюда
        self.textCtrl.Bind(wx.stc.EVT_STC_MODIFIED, self.__onModified)

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

    def __onModified(self, event):
        self._styleSet = False
        self._lastEdit = datetime.now()
        self._updateMarginWidth()
        event.Skip()

    def setDefaultSettings(self):
        """
        Установить стили и настройки по умолчанию в контрол StyledTextCtrl
        """
        self._setDefaultSettings()

        size = self._config.fontSize.value
        faceName = self._config.fontName.value
        isBold = self._config.fontIsBold.value
        isItalic = self._config.fontIsItalic.value
        fontColor = self._config.fontColor.value
        backColor = self._config.backColor.value
        selBackColor = self._config.selBackColor.value
        marginBackColor = self._config.marginBackColor.value

        self.__showlinenumbers = self._config.lineNumbers.value

        self.textCtrl.StyleSetSize(wx.stc.STC_STYLE_DEFAULT, size)
        self.textCtrl.StyleSetFaceName(wx.stc.STC_STYLE_DEFAULT, faceName)
        self.textCtrl.StyleSetBold(wx.stc.STC_STYLE_DEFAULT, isBold)
        self.textCtrl.StyleSetItalic(wx.stc.STC_STYLE_DEFAULT, isItalic)
        self.textCtrl.StyleSetForeground(wx.stc.STC_STYLE_DEFAULT, fontColor)
        self.textCtrl.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT, backColor)
        self.textCtrl.StyleSetBackground(wx.stc.STC_STYLE_LINENUMBER, marginBackColor)

        self.textCtrl.SetSelBackground(1, selBackColor)

        self.textCtrl.SetCaretForeground(fontColor)
        self.textCtrl.SetCaretLineBackground(backColor)

        self._setHotKeys()

        self._updateMarginWidth()
        self.textCtrl.SetTabWidth(self._config.tabWidth.value)

        self.enableSpellChecking = self._config.spellEnabled.value
        self.getSpellChecker().skipWordsWithNumbers = self.config.spellSkipDigits.value

        self.textCtrl.IndicatorSetStyle(
            self.SPELL_ERROR_INDICATOR, wx.stc.STC_INDIC_SQUIGGLE
        )
        self.textCtrl.IndicatorSetForeground(self.SPELL_ERROR_INDICATOR, "red")
        self._styleSet = False

    def _setHotKeys(self):
        if self._config.homeEndKeys.value == EditorConfig.HOME_END_OF_LINE:
            # Клавиши Home / End переносят курсор на начало / конец строки
            self.textCtrl.CmdKeyAssign(
                wx.stc.STC_KEY_HOME, 0, wx.stc.STC_CMD_HOMEDISPLAY
            )

            self.textCtrl.CmdKeyAssign(
                wx.stc.STC_KEY_HOME, wx.stc.STC_SCMOD_ALT, wx.stc.STC_CMD_HOME
            )

            self.textCtrl.CmdKeyAssign(
                wx.stc.STC_KEY_END, 0, wx.stc.STC_CMD_LINEENDDISPLAY
            )

            self.textCtrl.CmdKeyAssign(
                wx.stc.STC_KEY_END, wx.stc.STC_SCMOD_ALT, wx.stc.STC_CMD_LINEEND
            )
        else:
            # Клавиши Home / End переносят курсор на начало / конец абзаца
            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_HOME, 0, wx.stc.STC_CMD_HOME)

            self.textCtrl.CmdKeyAssign(
                wx.stc.STC_KEY_HOME, wx.stc.STC_SCMOD_ALT, wx.stc.STC_CMD_HOMEDISPLAY
            )

            self.textCtrl.CmdKeyAssign(wx.stc.STC_KEY_END, 0, wx.stc.STC_CMD_LINEEND)

            self.textCtrl.CmdKeyAssign(
                wx.stc.STC_KEY_END, wx.stc.STC_SCMOD_ALT, wx.stc.STC_CMD_LINEENDDISPLAY
            )

    def markSpellErrors(self, spellStatusFlags: List[bool]):
        """
               spellStatusFlags - list for every character (!) to set or clear
        spell errors indicators. True for no spell error, False for spell error.
        """
        if not spellStatusFlags:
            return

        text = self._getTextForParse()
        self.textCtrl.SetIndicatorCurrent(self.SPELL_ERROR_INDICATOR)
        start_pos = 0
        flag = spellStatusFlags[start_pos]
        while True:
            start_pos_bytes = self._helper.calcBytePos(text, start_pos)
            try:
                end_pos = spellStatusFlags.index(not flag, start_pos)
                end_pos_bytes = self._helper.calcBytePos(text, end_pos)

                self._setClearSpellError(flag, start_pos_bytes, end_pos_bytes)
                flag = not flag
                start_pos = end_pos
            except ValueError:
                end_pos_bytes = self._helper.calcByteLen(text)
                self._setClearSpellError(flag, start_pos_bytes, end_pos_bytes)
                break

    def _setClearSpellError(self, spellStatus, start_pos_bytes, end_pos_bytes):
        if spellStatus:
            self.textCtrl.IndicatorClearRange(
                start_pos_bytes, end_pos_bytes - start_pos_bytes
            )
        else:
            self.textCtrl.IndicatorFillRange(
                start_pos_bytes, end_pos_bytes - start_pos_bytes
            )

    def clearSpellChecking(self):
        text = self._getTextForParse()
        len_bytes = self._helper.calcByteLen(text)
        self.textCtrl.IndicatorClearRange(0, len_bytes)

    def _onStyleNeeded(self, _event):
        if not self._styleSet and datetime.now() - self._lastEdit >= self._DELAY:
            page = Application.selectedPage
            text = self._getTextForParse()
            params = EditorStyleNeededParams(self, text, self._enableSpellChecking)
            Application.onEditorStyleNeeded(page, params)
            self._styleSet = True

    def _onApplyStyle(self, event: ApplyStyleEvent):
        """
        Call back function for EVT_APPLY_STYLE
        """

        if event.text == self._getTextForParse():
            lenBytes = len(event.styleBytes)

            textlength = self._helper.calcByteLen(event.text)
            self.__stylebytes = [0] * textlength

            if event.styleBytes is not None:
                self.__stylebytes = event.styleBytes

            stylebytesstr = "".join([chr(byte) for byte in self.__stylebytes])

            if event.styleBytes is not None:
                self.textCtrl.StartStyling(0)
                self.textCtrl.SetStyleBytes(lenBytes, stylebytesstr.encode())

            self._styleSet = True

    def getSpellChecker(self):
        if self._spellChecker is None:
            langlist = self._getDictsFromConfig()
            spellDirList = outwiker.core.system.getSpellDirList()

            spellChecker = SpellChecker(langlist, spellDirList)
            spellChecker.addCustomDict(
                os.path.join(spellDirList[-1], CUSTOM_DICT_FILE_NAME)
            )

            self._spellChecker = spellChecker

        return self._spellChecker

    def _getDictsFromConfig(self):
        dictsStr = self._config.spellCheckerDicts.value
        return [item.strip() for item in dictsStr.split(",") if item.strip()]

    def __onContextMenu(self, event):
        point = self.textCtrl.ScreenToClient(event.GetPosition())
        pos_byte = self.textCtrl.PositionFromPoint(point)

        popupMenu = TextEditorMenu()
        self._appendSpellMenuItems(popupMenu, pos_byte)

        Application.onEditorPopupMenu(
            Application.selectedPage,
            EditorPopupMenuParams(self, popupMenu, point, pos_byte),
        )

        self.textCtrl.PopupMenu(popupMenu)
        popupMenu.Destroy()

    def getCachedStyleBytes(self):
        return self.__stylebytes

    def __onAddWordToDict(self, _event):
        if self._spellErrorText is not None:
            self.__addWordToDict(self._spellErrorText)

    def __onAddWordLowerToDict(self, _event):
        if self._spellErrorText is not None:
            self.__addWordToDict(self._spellErrorText.lower())

    def __addWordToDict(self, word):
        self.getSpellChecker().addToCustomDict(0, word)
        self._spellErrorText = None
        self._styleSet = False

    def _appendSpellMenuItems(self, menu, pos_byte):
        if not self.textCtrl.IndicatorValueAt(self.SPELL_ERROR_INDICATOR, pos_byte):
            return

        self._spellStartByteError = self.textCtrl.IndicatorStart(
            self.SPELL_ERROR_INDICATOR, pos_byte
        )
        self._spellEndByteError = self.textCtrl.IndicatorEnd(
            self.SPELL_ERROR_INDICATOR, pos_byte
        )

        self._spellErrorText = self.textCtrl.GetTextRange(
            self._spellStartByteError, self._spellEndByteError
        )

        spellChecker = self.getSpellChecker()
        self._spellSuggestList = spellChecker.getSuggest(self._spellErrorText)[
            : self._spellMaxSuggest
        ]

        menu.AppendSeparator()
        self._suggestMenuItems = menu.AppendSpellSubmenu(
            self._spellErrorText, self._spellSuggestList
        )

        for menuItem in self._suggestMenuItems:
            self.textCtrl.Bind(wx.EVT_MENU, self.__onSpellSuggest, menuItem)

        self.textCtrl.Bind(wx.EVT_MENU, self.__onAddWordToDict, id=menu.ID_ADD_WORD)

        self.textCtrl.Bind(
            wx.EVT_MENU, self.__onAddWordLowerToDict, id=menu.ID_ADD_WORD_LOWER
        )

    def __onSpellSuggest(self, event):
        word = event.GetEventObject().GetLabelText(event.GetId())

        self.textCtrl.SetSelection(self._spellStartByteError, self._spellEndByteError)
        self.textCtrl.ReplaceSelection(word)

    def onKeyDown(self, event: wx.KeyEvent):
        eventParams = TextEditorKeyDownParams(
            self,
            event.GetKeyCode(),
            event.GetUnicodeKey(),
            event.ControlDown(),
            event.ShiftDown(),
            event.AltDown(),
            event.CmdDown(),
            event.MetaDown(),
        )
        Application.onTextEditorKeyDown(Application.selectedPage, eventParams)

        if not eventParams.disableOutput:
            super().onKeyDown(event)

        self._checkCaretMoving()

    def _onKeyUp(self, _event):
        self._checkCaretMoving()

    def _checkCaretMoving(self):
        new_start_selection = self.GetSelectionStart()
        new_end_selection = self.GetSelectionEnd()

        if (
            self._oldStartSelection != new_start_selection
            or self._oldEndSelection != new_end_selection
        ):
            self._oldStartSelection = new_start_selection
            self._oldEndSelection = new_end_selection
            event_params = TextEditorCaretMoveParams(
                self, new_start_selection, new_end_selection
            )
            Application.onTextEditorCaretMove(Application.selectedPage, event_params)

    def _onMouseLeftDown(self, event):
        self._checkCaretMoving()
        event.Skip()

    def _onMouseLeftUp(self, event):
        self._checkCaretMoving()
        event.Skip()

    def _updateMarginWidth(self):
        """
        Установить размер левой области, где пишутся номера строк в
        зависимости от шрифта
        """
        if self.__showlinenumbers:
            self.textCtrl.SetMarginWidth(0, self.__getMarginWidth())
            self.textCtrl.SetMarginWidth(1, 5)
        else:
            self.textCtrl.SetMarginWidth(0, 0)
            self.textCtrl.SetMarginWidth(1, 0)

    def __getMarginWidth(self):
        """
        Расчет размера серой области с номером строк
        """
        linescount = self.textCtrl.GetLineCount()

        if linescount == 0:
            width = 10
        else:
            # Количество десятичных цифр в числе строк
            digits = int(math.log10(linescount) + 1)
            text = "_" + "9" * digits
            width = self.textCtrl.TextWidth(wx.stc.STC_STYLE_LINENUMBER, text)

        return width
