#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

import wx


if __name__ == '__main__':
    from outwiker.core.application import Application
    Application.init("../test/testconfig.ini")

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)
    wx.Log.SetLogLevel(0)

    import unittest

    from test.plugins.updatenotifier.test_loading import UpdateNotifierLoadingTest
    from test.plugins.updatenotifier.test_versionlist import VersionListTest
    from test.plugins.updatenotifier.test_updatecontroller import UpdateControllerTest

    unittest.main()
