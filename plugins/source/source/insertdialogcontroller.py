#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.commands import attachFiles, testreadonly
import outwiker.core.exceptions

from .misc import getDefaultStyle, fillStyleComboBox


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
        self._dialog.attachButton.Bind (wx.EVT_BUTTON, handler=self.__onAttach)


    def __onfileChecked (self, event):
        """
        Обработчик события при установке/снятии флажка "Вставить текст программы из файла"
        """
        self.updateFileChecked()


    def updateFileChecked (self):
        """
        Обновление интерфейса после установки/удаления флажка "Вставить текст программы из файла"
        """
        self.enableFileGuiElements (self._dialog.fileCheckBox.IsChecked())
        self.loadLanguagesState()


    @testreadonly
    def __onAttach (self, event):
        """
        Обработчик события при нажатии на кнопку для прикрепления файла
        """
        if self._page.readonly:
            raise outwiker.core.exceptions.ReadonlyException

        # Кусок ниже практически полностью скопирован из функции outwiker.core.commands.attachFilesWithDialog
        dlg = wx.FileDialog (self._dialog, 
            style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
            files = dlg.GetPaths()
            files.sort()
            attachFiles (self._dialog, self._page, files)

            self._loadAttachmentState()

            # Выберем только что добавленный файл
            newfile = os.path.basename (files[0])
            if newfile in self._dialog.attachmentComboBox.GetItems():
                self._dialog.attachmentComboBox.SetStringSelection (newfile)

            self._dialog.fileCheckBox.SetValue (True)
            self.updateFileChecked()

        dlg.Destroy()


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
        styleStr = self._getStyleParam()
        parentbg = self._getParentBg()
        linenum = self._getLineNum()

        startCommand = u'(:source{lang}{tabwidth}{style}{parentbg}{linenum}:)\n'.format (lang=langStr,
                tabwidth=tabWidthStr,
                style=styleStr,
                parentbg=parentbg,
                linenum=linenum)

        endCommand = u'\n(:sourceend:)'

        return (startCommand, endCommand)


    def _getTabWidthParam (self):
        if self._dialog.tabWidth != 0:
            return u' tabwidth="{0}"'.format(self._dialog.tabWidth)
        else:
            return u''


    def _getParentBg (self):
        if self._dialog.parentbg:
            return u' parentbg'

        return u''


    def _getLineNum (self):
        if self._dialog.lineNum:
            return u' linenum'

        return u''


    def _getStyleParam (self):
        return u'' if self._dialog.style == getDefaultStyle (self._config) else ' style="{style}"'.format (style=self._dialog.style)


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

        styleStr = self._getStyleParam()
        parentbg = self._getParentBg()
        linenum = self._getLineNum()

        startCommand = u'(:source{file}{lang}{encoding}{tabwidth}{style}{parentbg}{linenum}:)'.format (file=fnameStr,
                lang=langStr, 
                encoding=encodingStr,
                tabwidth=tabWidthStr,
                style=styleStr,
                parentbg=parentbg,
                linenum=linenum)

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
        self._loadStyleState()
        self._loadParentBgState()

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


    def _loadStyleState (self):
        fillStyleComboBox (self._config, 
                self._dialog.styleComboBox, 
                self._config.style.value.strip())


    def _loadParentBgState (self):
        self._dialog.parentBgCheckBox.SetValue (self._config.parentbg.value)


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
            self._config.defaultLanguage.value = self._dialog.language

        currentWidth, currentHeight = self._dialog.GetSizeTuple ()
        self._config.dialogWidth.value = currentWidth
        self._config.dialogHeight.value = currentHeight
        self._config.style.value = self._dialog.style
        self._config.parentbg.value = self._dialog.parentbg


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
