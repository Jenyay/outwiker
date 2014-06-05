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
        name = self._getNameParam()
        parent = self._getParentParam()

        # Если не установлен родительский счетчик, нет смысла устанавливать разделитель
        separator = self._getSeparatorParam() if len (parent) != 0 else u""

        start = self._getStartParam()
        step = self._getStepParam()
        hide = self._getHideParam()

        result = u"(:counter{name}{parent}{separator}{start}{step}{hide}:)".format (
                name = name,
                parent = parent,
                separator = separator,
                start = start,
                step = step,
                hide = hide)

        return result


    def _getHideParam (self):
        result = u' hide' if self._dialog.hide else u''
        return result


    def _getStepParam (self):
        step = self._dialog.step
        result = u' step={}'.format (step) if step != 1 else u''

        return result


    def _getStartParam (self):
        """
        Возвращает параметр команды (:counter:), соответствующий тому, нужно ли счетчик сбрасывать к какому-то значению
        """
        result = u' start={}'.format (self._dialog.start) if self._dialog.reset else u''

        return result


    def _getNameParam (self):
        """
        Возвращает параметр команды (:counter:), соответствующий введенному имени счетчика в диалоге
        """
        name = self._dialog.counterName.strip()
        result = u' name="{}"'.format (name) if len (name) != 0 else u''

        return result


    def _getParentParam (self):
        """
        Возвращает параметр команды (:counter:), соответствующий введенному имени родительского счетчика в диалоге
        """
        parent = self._dialog.parentName.strip()
        result = u' parent="{}"'.format (parent) if len (parent) != 0 else u''

        return result


    def _getSeparatorParam (self):
        """
        Возвращает параметр команды (:counter:), соответствующий введенному разделителю родительского и текущего счетчиков в диалоге
        """
        separator = self._dialog.separator
        result = u' separator="{}"'.format (separator) if separator != u"." else u''

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
