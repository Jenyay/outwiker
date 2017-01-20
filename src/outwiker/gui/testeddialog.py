# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.tester import Tester


class TestedDialog(wx.Dialog):
    """
    Диалог, который можно тестировать через Unit Test,
    поскольку ему можно заранее установить результат
    будущего вызова метода ShowModal
    """
    def __init__(self, *args, **kwargs):
        super(TestedDialog, self).__init__(*args, **kwargs)

    def ShowModal(self):
        result = Tester.dialogTester.runNext(self)
        if result is not None:
            event = wx.CommandEvent(wx.EVT_BUTTON.typeId, result)
            wx.PostEvent(self, event)

        return super(TestedDialog, self).ShowModal()


class TestedFileDialog(wx.FileDialog):
    """
    Диалог для выбора файлов, который можно тестировать
    """
    def __init__(self, *args, **kwargs):
        super(TestedFileDialog, self).__init__(*args, **kwargs)

        # Занчение используется для тестирования
        # (для принудительной установки выбранного файла)
        self._testedValue = None

    def ShowModal(self):
        result = Tester.dialogTester.runNext(self)
        if result is not None:
            return result

        return super(TestedFileDialog, self).ShowModal()

    def SetPathForTest(self, value):
        """
        Установить якобы выбранныый файл,
        путь до которого будет возвращем методом GetPath()
        """
        self._testedValue = value

    def GetPath(self):
        return (self._testedValue if self._testedValue is not None
                else super(TestedFileDialog, self).GetPath())
