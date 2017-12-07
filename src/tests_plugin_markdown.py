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
    loop = wx.GUIEventLoop()
    wx.GUIEventLoop.SetActive(loop)
    wx.Log.SetLogLevel(0)

    import unittest

    from test.plugins.markdown.test_markdown import MarkdownTest
    from test.plugins.markdown.test_loading import MarkdownLoadingTest
    from test.plugins.markdown.test_linkcreator import LinkCreatorTest
    from test.plugins.markdown.test_markdown_polyactions import MarkdownPolyactionsTest
    from test.plugins.markdown.test_imagedialog import MarkdownImageDialogTest

    unittest.main()
