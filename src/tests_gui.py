#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""
from gettext import NullTranslations

import wx


if __name__ == '__main__':
    NullTranslations().install()

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

    from test.guitests.test_movepage import MovePageGuiTest
    from test.guitests.test_openwiki import OpenWikiGuiTest
    from test.guitests.test_newwiki import NewWikiGuiTest
    from test.guitests.test_pagetabs import PageTabsTest
    from test.guitests.test_uriidentifiers import UriIdentifierIETest
    from test.guitests.test_uriidentifiers import UriIdentifierWebKitTest
    from test.guitests.test_safeimagelist import SafeImageListTest
    from test.guitests.test_hotkeys import HotKeysTest
    from test.guitests.test_hotkeyctrl import HotkeyCtrlTest

    from test.guitests.htmlpage.test_htmlpageview import HtmlPageViewTest
    from test.guitests.htmlpage.test_htmltabledialog import HtmlTableDialogTest
    from test.guitests.htmlpage.test_htmltablerowsdialog import HtmlTableRowsDialogTest
    from test.guitests.htmlpage.test_htmltableactions import HtmlTableActionsTest

    from test.guitests.wikipage.test_wikipageview import WikiPageViewTest
    from test.guitests.wikipage.test_wikitabledialog import WikiTableDialogTest
    from test.guitests.wikipage.test_wikitablerowsdialog import WikiTableRowsDialogTest
    from test.guitests.wikipage.test_wikitableactions import WikiTableActionsTest

    unittest.main()
