#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.preferences.configelements import IntegerElement

class InsertDialogController (object):
    """
    Класс для управления диалогом InsertDialog
    """
    def __init__ (self, dialog, config):
        """
        dialog - экземпляр класса InsertDialog, который надо будет показать пользователю.
        config - экземпляр класса SourceConfig
        """
        self._dialog = dialog
        self._config = config

        self.MIN_TAB_WIDTH = 1
        self.MAX_TAB_WIDTH = 50

        # Результат работы диалога
        # Если пользователь в диалоге нажал кнопку Cancel, _result = None,
        # иначе хранит кортеж из двух значений: (начало команды, завершение команды)
        self._result = None


    @property
    def result (self):
        """
        Результат работы диалога
        Если пользователь в диалоге нажал кнопку Cancel, _result = None, иначе возвращает кортеж из двух значений: (начало команды, завершение команды)
        """
        return self._result


    def showDialog (self):
        """
        Метод показывает диалог и возвращает кортеж из двух строк, которыми надо будет обернуть выделенный текст
        Если пользователь нажимает кнопку "Cancel", возвращается None
        """
        self._resultStr = None

        self.loadState()

        if self._dialog.ShowModal() == wx.ID_OK:
            self.saveState()
            self._resultStr = self._createCommandStrings (self._dialog)

        return self._resultStr


    def _createCommandStrings (self, dialog):
        startCommand = u'(:source lang="{language}" tabwidth={tabwidth}:)\n'.format (
                language=dialog.language,
                tabwidth=dialog.tabWidth
                )

        endCommand = u'\n(:sourceend:)'

        return (startCommand, endCommand)


    def loadState (self):
        """
        Загрузить настройки и установить их в диалоге
        """
        self._tabWidthOption = IntegerElement (
                self._config.tabWidth, 
                self._dialog.tabWidthSpin, 
                self.MIN_TAB_WIDTH, 
                self.MAX_TAB_WIDTH
                )

        languages = [item for item in self._config.languageList.value if len (item.strip()) > 0]

        # Если не выбран ни один из языков, добавляем "text"
        if len (languages) == 0:
            languages = [u"text"]

        self._dialog.languageComboBox.Clear()
        self._dialog.languageComboBox.AppendItems (languages)

        try:
            selindex = languages.index (self._config.defaultLanguage.value.lower().strip())
            self._dialog.languageComboBox.SetSelection (selindex)
        except ValueError:
            self._dialog.languageComboBox.SetSelection (0)


    def saveState (self):
        """
        Сохранить настройки диалога
        """
        self._tabWidthOption.save()
        self._config.defaultLanguage.value = self._dialog.languageComboBox.GetValue()
