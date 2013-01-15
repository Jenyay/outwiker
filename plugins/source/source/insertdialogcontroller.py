#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.preferences.configelements import IntegerElement
from outwiker.core.attachment import Attachment


class InsertDialogController (object):
    """
    Класс для управления диалогом InsertDialog
    """
    def __init__ (self, page, dialog, config):
        """
        page - текущая страница
        dialog - экземпляр класса InsertDialog, который надо будет показать пользователю.
        config - экземпляр класса SourceConfig
        """
        self._page = page
        self._dialog = dialog
        self._config = config

        self.MIN_TAB_WIDTH = 0
        self.MAX_TAB_WIDTH = 50

        self.AUTO_LANGUAGE = _(u"Auto")

        # Результат работы диалога
        # Если пользователь в диалоге нажал кнопку Cancel, _result = None,
        # иначе хранит кортеж из двух значений: (начало команды, завершение команды)
        self._result = None


    def __bindEvents (self):
        self._dialog.fileCheckBox.Bind (wx.EVT_CHECKBOX, handler=self.__onfileChecked)


    def __onfileChecked (self, event):
        enableFile = self._dialog.fileCheckBox.IsChecked()

        self.enableFileGuiElements (enableFile)
        self.loadLanguagesState()


    def showDialog (self):
        """
        Метод показывает диалог и возвращает кортеж из двух строк, которыми надо будет обернуть выделенный текст
        Если пользователь нажимает кнопку "Cancel", возвращается None
        """
        self.loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self.saveState()

        return result


    def _getStringsForText (self):
        """
        Возвращает кортеж строк для случая оформления исходников из текста (не из файла)
        """
        langStr = u' lang="{language}"'.format (language=self._dialog.language)
        tabWidthStr = self._getTabWidthParam()

        startCommand = u'(:source{lang}{tabwidth}:)\n'.format (lang=langStr,
                tabwidth=tabWidthStr)

        endCommand = u'\n(:sourceend:)'

        return (startCommand, endCommand)


    def _getTabWidthParam (self):
        if self._dialog.tabWidth != 0:
            return u' tabwidth="{0}"'.format(self._dialog.tabWidth)
        else:
            return u''


    def _getStringsForAttachment (self):
        """
        Возвращает кортеж строк для случая оформления исходников из прикрепленных файлов
        """
        fname = self._dialog.attachment
        encoding = self._dialog.encoding
        language = None if self._dialog.languageComboBox.GetSelection() == 0 else self._dialog.language

        fnameStr = u' file="Attach:{fname}"'.format (fname=fname)
        encodingStr = u'' if encoding == "utf8" else u' encoding="{encoding}"'.format (encoding=encoding)
        langStr = u'' if language == None else u' lang="{lang}"'.format (lang=language)
        tabWidthStr = self._getTabWidthParam()

        startCommand = u'(:source{file}{lang}{encoding}{tabwidth}:)'.format (file=fnameStr,
                lang=langStr, 
                encoding=encodingStr,
                tabwidth=tabWidthStr)

        endCommand = u'(:sourceend:)'

        return (startCommand, endCommand)


    def getCommandStrings (self):
        """
        Возвращает кортеж из двух строк, описывающих начало и конец команды
        """
        if self._dialog.insertFromFile:
            return self._getStringsForAttachment()
        else:
            return self._getStringsForText()


    def _getLangList (self):
        languages = [item for item in self._config.languageList.value if len (item.strip()) > 0]

        # Если не выбран ни один из языков, добавляем "text"
        if len (languages) == 0:
            languages = [u"text"]

        languages.sort()
        return languages


    def loadState (self):
        """
        Загрузить настройки и установить их в диалоге
        """
        self._loadTabWidthState()
        self.loadLanguagesState()
        self._loadEncodingState()
        self._loadAttachmentState()

        self._updateDialogSize()
        self.enableFileGuiElements (False)

        self.__bindEvents()


    def _updateDialogSize (self):
        """
        Изменение размера диалога
        """
        currentWidth, currentHeight = self._dialog.GetSizeTuple ()
        dialogWidth = max (self._config.dialogWidth.value, currentWidth)
        dialogHeight = max (self._config.dialogHeight.value, currentHeight)

        self._dialog.SetSizeWH (dialogWidth, dialogHeight)


    def _loadAttachmentState (self):
        attach = Attachment (self._page)
        files = attach.getAttachRelative()
        files.sort()

        self._dialog.attachmentComboBox.Clear()
        self._dialog.attachmentComboBox.AppendItems(files)

        if len (files) > 0:
            self._dialog.attachmentComboBox.SetSelection (0)


    def _loadEncodingState (self):
        """
        Заполнение списка кодировок
        """
        self._dialog.encodingComboBox.AppendItems (self.getEncodingList())
        self._dialog.encodingComboBox.SetSelection (0)


    def _loadTabWidthState (self):
        """
        Настройки элементов интерфейса, связанных с шириной табуляции
        """
        self._dialog.tabWidthSpin.SetRange (self.MIN_TAB_WIDTH, self.MAX_TAB_WIDTH)
        self._dialog.tabWidthSpin.SetValue (0)


    def loadLanguagesState (self):
        """
        Заполнение списка языков программирования
        """
        languages = self._getLangList()

        if self._dialog.insertFromFile:
            languages = [self.AUTO_LANGUAGE] + languages

        self._dialog.languageComboBox.Clear()
        self._dialog.languageComboBox.AppendItems (languages)

        if self._dialog.insertFromFile:
            self._dialog.languageComboBox.SetSelection (0)
        else:
            try:
                selindex = languages.index (self._config.defaultLanguage.value.lower().strip())
                self._dialog.languageComboBox.SetSelection (selindex)
            except ValueError:
                self._dialog.languageComboBox.SetSelection (0)


    def saveState (self):
        """
        Сохранить настройки диалога
        """
        if (not self._dialog.insertFromFile or 
                self._dialog.languageComboBox.GetSelection() != 0):
            self._config.defaultLanguage.value = self._dialog.languageComboBox.GetValue()

        currentWidth, currentHeight = self._dialog.GetSizeTuple ()
        self._config.dialogWidth.value = currentWidth
        self._config.dialogHeight.value = currentHeight


    def enableFileGuiElements (self, enabled):
        """
        Активировать или дизактивировать элементы управления, связанные с прикрепленными файлами
        """
        self._dialog.attachmentLabel.Enable (enabled)
        self._dialog.attachmentComboBox.Enable (enabled)
        self._dialog.encodingLabel.Enable (enabled)
        self._dialog.encodingComboBox.Enable (enabled)


    def getEncodingList (self):
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
