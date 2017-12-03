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

    from test.plugins.diagrammer.test_diagrammer import DiagrammerTest
    from test.plugins.diagrammer.test_insertnode import InsertNodeTest
    from test.plugins.diagrammer.test_insertdiagram import InsertDiagramTest
    from test.plugins.diagrammer.test_insertedge import InsertEdgeTest
    from test.plugins.diagrammer.test_insertgroup import InsertGroupTest
    from test.plugins.diagrammer.test_loading import DiagrammerLoadingTest

    unittest.main()
