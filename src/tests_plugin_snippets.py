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

    from test.plugins.snippets.test_loading import SnippetsLoadingTest
    from test.plugins.snippets.test_snippetsloader import SnippetsLoaderTest
    from test.plugins.snippets.test_snippetparser import SnippetParserTest
    from test.plugins.snippets.test_varpanel import SnippetsVarPanelTest
    from test.plugins.snippets.test_vardialog import SnippetsVarDialogTest
    from test.plugins.snippets.test_vardialogcontroller import SnippetsVarDialogControllerTest
    from test.plugins.snippets.test_utils import SnippetsUtilsTest
    from test.plugins.snippets.test_wikicommand import SnippetsWikiCommandTest

    unittest.main()
