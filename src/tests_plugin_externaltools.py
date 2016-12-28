#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""

import os
from outwiker.core.defines import WX_VERSION

import wxversion

try:
    wxversion.select(WX_VERSION)
except wxversion.VersionError:
    if os.name == "nt":
        pass
    else:
        raise

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

    from test.plugins.externaltools.test_loading import ExternalToolsLoadingTest
    from test.plugins.externaltools.test_commandexec import CommandExecTest
    from test.plugins.externaltools.test_commandexecparser import CommandExecParserTest
    from test.plugins.externaltools.test_commandexeccontroller import CommandExecControllerTest
    from test.plugins.externaltools.test_execdialog import ExecDialogTest

    unittest.main()
