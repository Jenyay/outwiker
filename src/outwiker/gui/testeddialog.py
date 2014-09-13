# -*- coding: UTF-8 -*-

import wx

from .tester import Tester


class TestedDialog (wx.Dialog):
    """
    Диалог, который можно тестировать через Unit Test, поскольку ему можно заранее установить результат будущего вызова метода ShowModal
    """
    def __init__ (self, *args, **kwargs):
        kwargs["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME

        super (TestedDialog, self).__init__ (*args, **kwargs)


    def ShowModal (self):
        func = Tester.dialogTester.pop()
        if func is not None:
            return func (self)

        return super (TestedDialog, self).ShowModal()



class TestedFileDialog (wx.FileDialog):
    """
    Диалог для выбора файлов, который можно тестировать
    """
    def __init__ (self, *args, **kwargs):
        super (TestedFileDialog, self).__init__ (*args, **kwargs)

        # Занчение используется для тестирования (для принудительной установки выбранного файла)
        self._testedValue = None


    def ShowModal (self):
        func = Tester.dialogTester.pop()
        if func is not None:
            return func (self)

        return super (TestedFileDialog, self).ShowModal()


    def SetPathForTest (self, value):
        """
        Установить якобы выбранныый файл, путь до которого будет возвращем методом GetPath()
        """
        self._testedValue = value


    def GetPath (self):
        return self._testedValue if self._testedValue is not None else super (TestedFileDialog, self).GetPath()
