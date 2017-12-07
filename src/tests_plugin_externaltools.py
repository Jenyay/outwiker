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

    from test.plugins.externaltools.test_loading import ExternalToolsLoadingTest
    from test.plugins.externaltools.test_commandexec import CommandExecTest
    from test.plugins.externaltools.test_commandexecparser import CommandExecParserTest
    from test.plugins.externaltools.test_commandexeccontroller import CommandExecControllerTest
    from test.plugins.externaltools.test_execdialog import ExecDialogTest

    unittest.main()
