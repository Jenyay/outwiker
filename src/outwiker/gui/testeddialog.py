# -*- coding: UTF-8 -*-

import wx


class TestedDialog (wx.Dialog):
    """
    Диалог, который можно тестировать через Unit Test, поскольку ему можно заранее установить результат будущего вызова метода ShowModal
    """
    def __init__ (self, *args, **kwargs):
        kwargs["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME

        super (TestedDialog, self).__init__ (*args, **kwargs)
        self.__modalResult = None


    def SetModalResult (self, result):
        """
        Установить будущий результат вызова ShowModal
        """
        self.__modalResult = result


    def ShowModal (self):
        if self.__modalResult is not None:
            return self.__modalResult

        return super (TestedDialog, self).ShowModal()
