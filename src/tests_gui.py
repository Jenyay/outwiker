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


    from test.guitests.wikipage.test_wikipageview import WikiPageViewTest
    from test.guitests.wikipage.test_wikitabledialog import WikiTableDialogTest
    from test.guitests.wikipage.test_wikitablerowsdialog import WikiTableRowsDialogTest
    from test.guitests.wikipage.test_wikitableactions import WikiTableActionsTest

    unittest.main()
