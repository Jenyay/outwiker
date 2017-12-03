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

    from test.plugins.datagraph.test_loading import DataGraphLoadingTest
    from test.plugins.datagraph.test_paramsparsing import ParamsParsingTest
    from test.plugins.datagraph.test_graphbuilder import GraphBuilderTest
    from test.plugins.datagraph.test_datasources import StringSourceTest, FileSourceTest
    from test.plugins.datagraph.test_command_plot_highcharts import CommandPlotHighchartsTest

    unittest.main()
