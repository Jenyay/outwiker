#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""
from gettext import NullTranslations

import wx


if __name__ == '__main__':
    NullTranslations().install()

    from outwiker.core.application import Application
    Application.init("../test/testconfig.ini")

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.GUIEventLoop()
    wx.GUIEventLoop.SetActive(loop)
    wx.Log.SetLogLevel(0)

    import unittest

    from test.plugins.counter.test_counter import CounterTest
    from test.plugins.counter.test_counterdialog import CounterDialogTest
    from test.plugins.counter.test_loading import CounterLoadingTest

    unittest.main()
