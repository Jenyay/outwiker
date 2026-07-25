# -*- coding: utf-8 -*-

import os.path
from pathlib import Path

import wx

from outwiker.api.app.attachment import attachFiles
from outwiker.api.core.attachment import Attachment
from outwiker.api.core.tree import testreadonly
from outwiker.api.core.attachment import getHiddenFilter, notFilter
from outwiker.api.core.exceptions import ReadonlyException

from .misc import getDefaultStyle, fillStyleComboBox
from .insertdialog import InsertDialog
from .langlist import LangList
from .i18n import get_
from .gui.filterlistdialog import FilterListDialog


class InsertDialogController:
    """
    Controller class for InsertDialog
    """

    def __init__(self, page, dialog: InsertDialog, config):
        """
        page - current page
        dialog - InsertDialog instance to show to the user.
        config - SourceConfig instance
        """
        self._page = page
        self._dialog = dialog
        self._config = config

        global _
        _ = get_()

        self._langList = LangList(_)

        self.MIN_TAB_WIDTH = 0
        self.MAX_TAB_WIDTH = 50

        self.AUTO_LANGUAGE = _("Auto")

    def _bindEvents(self):
        self._dialog.fileCheckBox.Bind(wx.EVT_CHECKBOX, handler=self._onfileChecked)
        self._dialog.attachButton.Bind(wx.EVT_BUTTON, handler=self._onAttach)
        self._dialog.languageComboBox.Bind(wx.EVT_COMBOBOX, handler=self._onLangSelect)

    def _onLangSelect(self, event):
        count = self._dialog.languageComboBox.GetCount()
        sel_index = self._dialog.languageComboBox.GetSelection()

        if sel_index == count - 1:
            self._addNewLang()

    def _addNewLang(self):
        current_langs = self._getLangList()
        lang_list = [
            lang_name
            for lang_name in self._langList.allNames()
            if lang_name not in current_langs
        ]
        lang_list.sort(key=str.lower)

        with FilterListDialog(
            self._dialog, lang_list, _("Add other language")
        ) as dialog:
            dialog.SetSize((300, 450))
            if dialog.ShowModal() == wx.ID_OK:
                new_lang_name = dialog.selectedLanguage
                new_lang_designation = self._langList.getDesignation(new_lang_name)
                self._config.languageList.value = self._config.languageList.value + [
                    new_lang_designation
                ]
                self._config.defaultLanguage.value = new_lang_designation

            self.loadLanguagesState()

    def _onfileChecked(self, event):
        """
        Event handler for checkbox toggle
            "Insert source text from file"
        """
        self.updateFileChecked()

    def updateFileChecked(self):
        """
        Update interface after checkbox is checked/unchecked
            "Insert source text from file"
        """
        self.enableFileGuiElements(self._dialog.fileCheckBox.IsChecked())
        self.loadLanguagesState()

    @testreadonly
    def _onAttach(self, event):
        """
        Event handler for file attachment button
        """
        if self._page.readonly:
            raise ReadonlyException()

        # Кусок ниже практически полностью скопирован из функции
        # outwiker.core.commands.attachFilesWithDialog
        dlg = wx.FileDialog(
            self._dialog, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        )

        if dlg.ShowModal() == wx.ID_OK:
            files = sorted(dlg.GetPaths())
            attachFiles(self._dialog, self._page, files)

            self._updateFilesList()

            # Выберем только что добавленный файл
            newfile = os.path.basename(files[0])
            self._dialog.attachmentComboBox.SetValue(newfile)

            self._dialog.fileCheckBox.SetValue(True)
            self.updateFileChecked()

        dlg.Destroy()

    def showDialog(self):
        """
        Show dialog and return the result of ShowModal()
        """
        self.loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self.saveState()

        return result

    def _getTabWidthParam(self):
        if self._dialog.tabWidth != 0:
            return ' tabwidth="{0}"'.format(self._dialog.tabWidth)
        else:
            return ""

    def _getParentBg(self):
        if self._dialog.parentbg:
            return " parentbg"

        return ""

    def _getLineNum(self):
        if self._dialog.lineNum:
            return " linenum"

        return ""

    def _getStyleParam(self):
        return (
            ""
            if self._dialog.style == getDefaultStyle(self._config)
            else ' style="{style}"'.format(style=self._dialog.style)
        )

    def _getCommonParams(self):
        """
        Get common parameters for both inline and file-based source code
        """
        commonparams = "{tabwidth}{style}{parentbg}{linenum}"

        tabWidthStr = self._getTabWidthParam()
        styleStr = self._getStyleParam()
        parentbg = self._getParentBg()
        linenum = self._getLineNum()

        return commonparams.format(
            tabwidth=tabWidthStr, style=styleStr, parentbg=parentbg, linenum=linenum
        )

    def _getStringsForText(self):
        """
        Returns a tuple of strings for formatting source code
            from text (not from file)
        """
        langStr = ' lang="{language}"'.format(
            language=self._langList.getDesignation(self._dialog.language)
        )

        commonparams = self._getCommonParams()

        startCommand = "(:source{lang}{commonparams}:)\n".format(
            lang=langStr, commonparams=commonparams
        )

        endCommand = "\n(:sourceend:)"

        return (startCommand, endCommand)

    def _getStringsForAttachment(self):
        """
        Returns a tuple of strings for formatting source code
            from attached files
        """
        fname = self._dialog.attachment
        encoding = self._dialog.encoding
        language = (
            None
            if self._dialog.languageComboBox.GetSelection() == 0
            else self._langList.getDesignation(self._dialog.language)
        )

        fnameStr = ' file="Attach:{fname}"'.format(fname=fname)
        encodingStr = (
            ""
            if encoding == "utf8"
            else ' encoding="{encoding}"'.format(encoding=encoding)
        )

        langStr = "" if language is None else ' lang="{lang}"'.format(lang=language)

        commonparams = self._getCommonParams()

        startCommand = "(:source{file}{encoding}{lang}{commonparams}:)".format(
            file=fnameStr, encoding=encodingStr, lang=langStr, commonparams=commonparams
        )

        endCommand = "(:sourceend:)"

        return (startCommand, endCommand)

    def getCommandStrings(self):
        """
        Returns a tuple of two strings describing the start and end of the command
        """
        if self._dialog.insertFromFile:
            return self._getStringsForAttachment()
        else:
            return self._getStringsForText()

    def _getLangList(self):
        languages = [
            self._langList.getLangName(item)
            for item in self._config.languageList.value
            if len(item.strip()) > 0
        ]

        # Если не выбран ни один из языков, добавляем "text"
        if len(languages) == 0:
            languages = ["text"]

        languages.sort()
        return languages

    def loadState(self):
        """
        Load settings and apply them to the dialog
        """
        self._loadTabWidthState()
        self.loadLanguagesState()
        self._loadEncodingState()
        self._updateFilesList()
        self._loadStyleState()

        self._dialog.parentBgCheckBox.SetValue(self._config.parentbg.value)
        self._dialog.lineNumCheckBox.SetValue(self._config.lineNum.value)

        self._updateDialogSize()
        self.enableFileGuiElements(False)

        self._bindEvents()

    def _updateDialogSize(self):
        """
        Update dialog size
        """
        currentWidth, currentHeight = self._dialog.GetSize()
        dialogWidth = max(self._config.dialogWidth.value, currentWidth)
        dialogHeight = max(self._config.dialogHeight.value, currentHeight)

        self._dialog.SetClientSize(dialogWidth, dialogHeight)

    def _updateFilesList(self):
        attach = Attachment(self._page)
        attach_path = Path(attach.getAttachPath(create=False))
        self._dialog.attachmentComboBox.Clear()
        if attach_path.exists():
            files_filter = notFilter(getHiddenFilter(self._page))
            self._dialog.attachmentComboBox.SetRootDir(attach_path)
            self._dialog.attachmentComboBox.SetFilterFunc(files_filter)

    def _loadStyleState(self):
        fillStyleComboBox(
            self._config, self._dialog.styleComboBox, self._config.style.value.strip()
        )

    def _loadEncodingState(self):
        """
        Fill encoding list
        """
        self._dialog.encodingComboBox.AppendItems(self.getEncodingList())
        self._dialog.encodingComboBox.SetSelection(0)

    def _loadTabWidthState(self):
        """
        Configure tab width GUI elements
        """
        self._dialog.tabWidthSpin.SetRange(self.MIN_TAB_WIDTH, self.MAX_TAB_WIDTH)
        self._dialog.tabWidthSpin.SetValue(0)

    def loadLanguagesState(self):
        """
        Fill programming languages list
        """
        languages = self._getLangList() + [_("Other...")]

        if self._dialog.insertFromFile:
            languages = [self.AUTO_LANGUAGE] + languages

        self._dialog.languageComboBox.Clear()
        self._dialog.languageComboBox.AppendItems(languages)

        if self._dialog.insertFromFile:
            self._dialog.languageComboBox.SetSelection(0)
        else:
            try:
                default_lang = self._langList.getLangName(
                    self._config.defaultLanguage.value.lower().strip()
                )

                selindex = languages.index(default_lang)
                self._dialog.languageComboBox.SetSelection(selindex)
            except ValueError:
                self._dialog.languageComboBox.SetSelection(0)

    def saveState(self):
        """
        Save dialog settings
        """
        if (
            not self._dialog.insertFromFile
            or self._dialog.languageComboBox.GetSelection() != 0
        ):
            self._config.defaultLanguage.value = self._langList.getDesignation(
                self._dialog.language
            )

        currentWidth, currentHeight = self._dialog.GetClientSize()
        self._config.dialogWidth.value = currentWidth
        self._config.dialogHeight.value = currentHeight
        self._config.style.value = self._dialog.style
        self._config.parentbg.value = self._dialog.parentbg
        self._config.lineNum.value = self._dialog.lineNum

    def enableFileGuiElements(self, enabled):
        """
        Enable or disable GUI elements related to attached files
        """
        self._dialog.attachmentLabel.Enable(enabled)
        self._dialog.attachmentComboBox.Enable(enabled)
        self._dialog.encodingLabel.Enable(enabled)
        self._dialog.encodingComboBox.Enable(enabled)

    def getEncodingList(self):
        return [
            "utf8",
            "cp1250",
            "cp1251",
            "cp1252",
            "cp866",
            "koi8_r",
            "mac_cyrillic",
            "ascii",
            "latin_1",
        ]
