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

    from test.actions.test_wikidate import WikiDateActionTest
    from test.actions.test_wikiactions import WikiActionsTest
    from test.actions.test_sortpages import SortPagesTest
    from test.actions.test_actiontabs import ActionTabsTest
    from test.actions.test_htmlactions import HtmlActionsTest
    from test.actions.test_insertdate import InsertDateTest
    from test.actions.test_polyaction import PolyActionTest
    from test.actions.test_globalsearch import GlobalSearchActionTest
    from test.actions.test_description import DescriptionActionTest
    from test.actions.test_applystyle import ApplyStyleActionTest
    from test.actions.test_moveupdown import MovePageUpDownActionTest
    from test.actions.test_moving import MovingActionTest
    from test.actions.test_editor_polyactions import (
        WikiEditorPolyactionsTest,
        HtmlEditorPolyactionsTest,
        TextEditorPolyactionsTest,
    )

    unittest.main()
