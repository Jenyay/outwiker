# -*- coding: utf-8 -*-

import os.path

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.commands import attachFiles, testreadonly
import outwiker.core.exceptions

from .misc import getDefaultStyle, fillStyleComboBox
from .insertdialog import InsertDialog
from .langlist import LangList
from .i18n import get_
from .gui.filterlistdialog import FilterListDialog


class InsertDialogController(object):
    """
    Класс для управления диалогом InsertDialog
    """

    def __init__(self, page, dialog: InsertDialog, config):
        """
        page - текущая страница
        dialog - экземпляр класса InsertDialog,
            который надо будет показать пользователю.
        config - экземпляр класса SourceConfig
        """
        self._page = page
        self._dialog = dialog
        self._config = config

        global _
        _ = get_()

        self._langList = LangList(_)

        self.MIN_TAB_WIDTH = 0
        self.MAX_TAB_WIDTH = 50

        self.AUTO_LANGUAGE = _(u"Auto")

    def _bindEvents(self):
        self._dialog.fileCheckBox.Bind(wx.EVT_CHECKBOX,
                                       handler=self._onfileChecked)
        self._dialog.attachButton.Bind(wx.EVT_BUTTON,
                                       handler=self._onAttach)
        self._dialog.languageComboBox.Bind(wx.EVT_COMBOBOX,
                                           handler=self._onLangSelect)

    def _onLangSelect(self, event):
        count = self._dialog.languageComboBox.GetCount()
        sel_index = self._dialog.languageComboBox.GetSelection()

        if sel_index == count - 1:
            self._addNewLang()

    def _addNewLang(self):
        current_langs = self._getLangList()
        lang_list = [lang_name
                     for lang_name in self._langList.allNames()
                     if lang_name not in current_langs]
        lang_list.sort(key=str.lower)

        with FilterListDialog(self._dialog,
                              lang_list,
                              _('Add other language')) as dialog:
            dialog.SetSize((300, 450))
            if dialog.ShowModal() == wx.ID_OK:
                new_lang_name = dialog.selectedLanguage
                new_lang_designation = self._langList.getDesignation(new_lang_name)
                self._config.languageList.value = self._config.languageList.value + [new_lang_designation]
                self._config.defaultLanguage.value = new_lang_designation

            self.loadLanguagesState()

    def _onfileChecked(self, event):
        """
        Обработчик события при установке/снятии флажка
            "Вставить текст программы из файла"
        """
        self.updateFileChecked()

    def updateFileChecked(self):
        """
        Обновление интерфейса после установки/удаления флажка
            "Вставить текст программы из файла"
        """
        self.enableFileGuiElements(self._dialog.fileCheckBox.IsChecked())
        self.loadLanguagesState()

    @testreadonly
    def _onAttach(self, event):
        """
        Обработчик события при нажатии на кнопку для прикрепления файла
        """
        if self._page.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        # Кусок ниже практически полностью скопирован из функции
        # outwiker.core.commands.attachFilesWithDialog
        dlg = wx.FileDialog(
            self._dialog,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        )

        if dlg.ShowModal() == wx.ID_OK:
            files = sorted(dlg.GetPaths())
            attachFiles(self._dialog, self._page, files)

            self._loadAttachmentState()

            # Выберем только что добавленный файл
            newfile = os.path.basename(files[0])
            if newfile in self._dialog.attachmentComboBox.GetItems():
                self._dialog.attachmentComboBox.SetStringSelection(newfile)

            self._dialog.fileCheckBox.SetValue(True)
            self.updateFileChecked()

        dlg.Destroy()

    def showDialog(self):
        """
        Метод показывает диалог и возвращает результат метода
            ShowModal() диалога
        """
        self.loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self.saveState()

        return result

    def _getTabWidthParam(self):
        if self._dialog.tabWidth != 0:
            return u' tabwidth="{0}"'.format(self._dialog.tabWidth)
        else:
            return u''

    def _getParentBg(self):
        if self._dialog.parentbg:
            return u' parentbg'

        return u''

    def _getLineNum(self):
        if self._dialog.lineNum:
            return u' linenum'

        return u''

    def _getStyleParam(self):
        return (u''
                if self._dialog.style == getDefaultStyle(self._config)
                else ' style="{style}"'.format(style=self._dialog.style))

    def _getCommonParams(self):
        """
        Получить список параметров, общий для исходников,
            вставляемых в виде текста и из файла
        """
        commonparams = u'{tabwidth}{style}{parentbg}{linenum}'

        tabWidthStr = self._getTabWidthParam()
        styleStr = self._getStyleParam()
        parentbg = self._getParentBg()
        linenum = self._getLineNum()

        return commonparams.format(tabwidth=tabWidthStr,
                                   style=styleStr,
                                   parentbg=parentbg,
                                   linenum=linenum)

    def _getStringsForText(self):
        """
        Возвращает кортеж строк для случая оформления исходников
            из текста (не из файла)
        """
        langStr = u' lang="{language}"'.format(
            language=self._langList.getDesignation(self._dialog.language))

        commonparams = self._getCommonParams()

        startCommand = u'(:source{lang}{commonparams}:)\n'.format(
            lang=langStr,
            commonparams=commonparams)

        endCommand = u'\n(:sourceend:)'

        return(startCommand, endCommand)

    def _getStringsForAttachment(self):
        """
        Возвращает кортеж строк для случая оформления исходников
            из прикрепленных файлов
        """
        fname = self._dialog.attachment
        encoding = self._dialog.encoding
        language = (None
                    if self._dialog.languageComboBox.GetSelection() == 0
                    else self._langList.getDesignation(self._dialog.language))

        fnameStr = u' file="Attach:{fname}"'.format(fname=fname)
        encodingStr = (
            u''
            if encoding == "utf8"
            else u' encoding="{encoding}"'.format(encoding=encoding)
        )

        langStr = (u''
                   if language is None
                   else u' lang="{lang}"'.format(lang=language))

        commonparams = self._getCommonParams()

        startCommand = u'(:source{file}{encoding}{lang}{commonparams}:)'.format(file=fnameStr,
                                                                                encoding=encodingStr,
                                                                                lang=langStr,
                                                                                commonparams=commonparams)

        endCommand = u'(:sourceend:)'

        return(startCommand, endCommand)

    def getCommandStrings(self):
        """
        Возвращает кортеж из двух строк, описывающих начало и конец команды
        """
        if self._dialog.insertFromFile:
            return self._getStringsForAttachment()
        else:
            return self._getStringsForText()

    def _getLangList(self):
        languages = [self._langList.getLangName(item)
                     for item
                     in self._config.languageList.value
                     if len(item.strip()) > 0]

        # Если не выбран ни один из языков, добавляем "text"
        if len(languages) == 0:
            languages = [u"text"]

        languages.sort()
        return languages

    def loadState(self):
        """
        Загрузить настройки и установить их в диалоге
        """
        self._loadTabWidthState()
        self.loadLanguagesState()
        self._loadEncodingState()
        self._loadAttachmentState()
        self._loadStyleState()

        self._dialog.parentBgCheckBox.SetValue(self._config.parentbg.value)
        self._dialog.lineNumCheckBox.SetValue(self._config.lineNum.value)

        self._updateDialogSize()
        self.enableFileGuiElements(False)

        self._bindEvents()

    def _updateDialogSize(self):
        """
        Изменение размера диалога
        """
        currentWidth, currentHeight = self._dialog.GetSize()
        dialogWidth = max(self._config.dialogWidth.value, currentWidth)
        dialogHeight = max(self._config.dialogHeight.value, currentHeight)

        self._dialog.SetClientSize(dialogWidth, dialogHeight)

    def _loadAttachmentState(self):
        attach = Attachment(self._page)
        files = sorted(attach.getAttachRelative())

        self._dialog.attachmentComboBox.Clear()
        self._dialog.attachmentComboBox.AppendItems(files)

        if len(files) > 0:
            self._dialog.attachmentComboBox.SetSelection(0)

    def _loadStyleState(self):
        fillStyleComboBox(self._config,
                          self._dialog.styleComboBox,
                          self._config.style.value.strip())

    def _loadEncodingState(self):
        """
        Заполнение списка кодировок
        """
        self._dialog.encodingComboBox.AppendItems(self.getEncodingList())
        self._dialog.encodingComboBox.SetSelection(0)

    def _loadTabWidthState(self):
        """
        Настройки элементов интерфейса, связанных с шириной табуляции
        """
        self._dialog.tabWidthSpin.SetRange(self.MIN_TAB_WIDTH,
                                           self.MAX_TAB_WIDTH)
        self._dialog.tabWidthSpin.SetValue(0)

    def loadLanguagesState(self):
        """
        Заполнение списка языков программирования
        """
        languages = self._getLangList() + [_('Other...')]

        if self._dialog.insertFromFile:
            languages = [self.AUTO_LANGUAGE] + languages

        self._dialog.languageComboBox.Clear()
        self._dialog.languageComboBox.AppendItems(languages)

        if self._dialog.insertFromFile:
            self._dialog.languageComboBox.SetSelection(0)
        else:
            try:
                default_lang = self._langList.getLangName(
                    self._config.defaultLanguage.value.lower().strip())

                selindex = languages.index(default_lang)
                self._dialog.languageComboBox.SetSelection(selindex)
            except ValueError:
                self._dialog.languageComboBox.SetSelection(0)

    def saveState(self):
        """
        Сохранить настройки диалога
        """
        if (not self._dialog.insertFromFile or
                self._dialog.languageComboBox.GetSelection() != 0):
            self._config.defaultLanguage.value = self._langList.getDesignation(self._dialog.language)

        currentWidth, currentHeight = self._dialog.GetClientSize()
        self._config.dialogWidth.value = currentWidth
        self._config.dialogHeight.value = currentHeight
        self._config.style.value = self._dialog.style
        self._config.parentbg.value = self._dialog.parentbg
        self._config.lineNum.value = self._dialog.lineNum

    def enableFileGuiElements(self, enabled):
        """
        Активировать или дизактивировать элементы управления,
            связанные с прикрепленными файлами
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
            "latin_1"
        ]
