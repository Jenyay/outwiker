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

    from test.plugins.hackpage.test_loading import HackPage_LoadingTest
    from test.plugins.hackpage.test_changepageuid import HackPage_ChangePageUidTest
    from test.plugins.hackpage.test_setalias import HackPage_SetAliasTest
    from test.plugins.hackpage.test_changetitle import HackPage_ChangeTitleTest

    unittest.main()
