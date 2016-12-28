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

    from test.plugins.source.test_source import SourcePluginTest
    from test.plugins.source.test_sourceencoding import SourceEncodingPluginTest
    from test.plugins.source.test_sourcefile import SourceFilePluginTest
    from test.plugins.source.test_sourcegui import SourceGuiPluginTest
    from test.plugins.source.test_sourceattachment import SourceAttachmentPluginTest
    from test.plugins.source.test_sourcestyle import SourceStyleTest
    from test.plugins.source.test_loading import SourceLoadingTest

    unittest.main()
