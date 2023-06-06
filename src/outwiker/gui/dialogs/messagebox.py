# -*- coding: utf-8 -*-

import wx

from outwiker.gui.tester import Tester


def MessageBox(*args, **kwargs):
    """
    Замена стандартного MessageBox. Перед показом диалога отключает
    приложение от события EVT_ACTIVATE_APP.
    """
    result = Tester.dialogTester.runNext(None)
    if result is not None:
        return result

    wx.GetApp().unbindActivateApp()
    result = wx.MessageBox(*args, **kwargs)
    wx.GetApp().bindActivateApp()

    return result
