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
