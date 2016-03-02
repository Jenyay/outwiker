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
    Application.init ("../test/testconfig.ini")

    app = wx.PySimpleApp(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)

    import unittest

    from test.actions.wikidate import WikiDateActionTest
    from test.actions.wikiactions import WikiActionsTest
    from test.actions.sortpages import SortPagesTest
    from test.actions.actiontabs import ActionTabsTest
    from test.actions.htmlactions import HtmlActionsTest
    from test.actions.insertdate import InsertDateTest
    from test.actions.polyaction import PolyActionTest
    from test.actions.globalsearch import GlobalSearchActionTest
    from test.actions.description import DescriptionActionTest
    from test.actions.applystyle import ApplyStyleActionTest
    from test.actions.moveupdown import MovePageUpDownActionTest
    from test.actions.moving import MovingActionTest

    unittest.main()
