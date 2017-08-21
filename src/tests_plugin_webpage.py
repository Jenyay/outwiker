#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

    from test.plugins.webpage.test_webpage import WebPageTest
    from test.plugins.webpage.test_downloader import DownloaderTest
    from test.plugins.webpage.test_real import RealTest
    from test.plugins.webpage.test_loading import WebPageLoadingTest

    unittest.main()
