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

    from test.plugins.tableofcontents.test_toc_parser import TOC_ParserTest
    from test.plugins.tableofcontents.test_toc_generator import TOC_GeneratorTest
    from test.plugins.tableofcontents.test_toc_wikimaker import TOC_WikiMakerTest
    from test.plugins.tableofcontents.test_loading import TOCLoadingTest

    unittest.main()
