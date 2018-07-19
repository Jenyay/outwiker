# -*- coding: utf-8 -*-

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


class TestedStandardDialogMixin(object):
    def __init__(self, *args, **kwargs):
        self._testedValue = None
        super().__init__(*args, **kwargs)

    def ShowModal(self):
        result = Tester.dialogTester.runNext(self)
        if result is not None:
            return result

        return super().ShowModal()

    def SetDataForTest(self, value):
        self._testedValue = value


class TestedFileDialog(TestedStandardDialogMixin, wx.FileDialog):
    """
    Диалог для выбора файлов, который можно тестировать
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def GetPath(self):
        return (self._testedValue if self._testedValue is not None
                else super(TestedFileDialog, self).GetPath())
