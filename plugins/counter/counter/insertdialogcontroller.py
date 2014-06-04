# -*- coding: UTF-8 -*-

import os.path

import wx

import outwiker.core.exceptions

from .config import CounterConfig


class InsertDialogController (object):
    """
    Класс для управления диалогом InsertDialog
    """
    def __init__ (self, dialog, config):
        """
        dialog - экземпляр класса InsertDialog, который надо будет показать пользователю.
        config - экземпляр класса Config
        """
        self._dialog = dialog
        self._config = CounterConfig (config)


    def showDialog (self):
        """
        Метод показывает диалог и возвращает строку, соответствующую выбранным настройкам
        Если пользователь нажимает кнопку "Cancel", возвращается None
        """
        self.loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self.saveState()

        return result


    def getCommandString (self):
        """
        Возвращает строку, соответствующую выбранным настройкам в диалоге
        """
        name = self._getNameParam ()

        result = u"(:counter{name}:)".format (
                name = name)

        return result


    def _getNameParam (self):
        """
        Возвращает параметр команды (:counter:), соответствующий введенному имени счетчика в диалоге
        """
        name = self._dialog.counterName.strip()
        result = u' name="{}"'.format (name) if len (name) != 0 else u''

        return result



    def loadState (self):
        """
        Загрузить настройки и установить их в диалоге
        """
        self._updateDialogSize()


    def _updateDialogSize (self):
        """
        Изменение размера диалога
        """
        currentWidth, currentHeight = self._dialog.GetSizeTuple ()
        dialogWidth = max (self._config.dialogWidth.value, currentWidth)
        dialogHeight = max (self._config.dialogHeight.value, currentHeight)

        self._dialog.SetSizeWH (dialogWidth, dialogHeight)


    def saveState (self):
        """
        Сохранить настройки диалога
        """
        currentWidth, currentHeight = self._dialog.GetSizeTuple ()
        self._config.dialogWidth.value = currentWidth
        self._config.dialogHeight.value = currentHeight
