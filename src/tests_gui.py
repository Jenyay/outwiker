#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""

import wx


if __name__ == '__main__':
    from outwiker.core.application import Application
    Application.init ("../test/testconfig.ini")

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)
    wx.Log.SetLogLevel(0)

    import unittest

    from test.guitests.test_mainwnd import MainWndTest
    from test.guitests.test_bookmarks import BookmarksGuiTest
    from test.guitests.test_attach import AttachPanelTest
    from test.guitests.test_tree import TreeTest
    from test.guitests.test_pagepanel import PagePanelTest
    from test.guitests.test_tagspanel import TagsPanelTest
    from test.guitests.test_tabs import TabsTest
    from test.guitests.test_linkdialogcontrollertest import LinkDialogControllerTest
    from test.guitests.test_thumbdialogcontrollertest import ThumbDialogControllerTest
    from test.guitests.test_textpageview import TextPageViewTest
    from test.guitests.test_actioncontroller import ActionControllerTest
    from test.guitests.test_mainpanes import MainPanesTest
    from test.guitests.test_fullscreen import FullScreenTest
    from test.guitests.test_texteditor import TextEditorTest
    from test.guitests.test_fileicons import FileIconsTestUnix
    from test.guitests.test_stcstyleparser import StcStyleParserTest
    from test.guitests.test_childlistdialog import ChildListDialogTest
    from test.guitests.test_attachlistdialog import AttachListDialogTest
    from test.guitests.test_includedialog import IncludeDialogTest
    from test.guitests.test_removepage import RemovePageGuiTest
    from test.guitests.test_renamepage import RenamePageGuiTest
    from test.guitests.test_movepage import MovePageGuiTest
    from test.guitests.test_openwiki import OpenWikiGuiTest
    from test.guitests.test_newwiki import NewWikiGuiTest
    from test.guitests.test_pagetabs import PageTabsTest
    from test.guitests.test_fileicons import FileIconsTestWindows
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

    # import cProfile
    # import pstats
    # profile_fname = "../profiles/tests.profile"
    #
    # cProfile.run('unittest.main()', profile_fname)
    # stats = pstats.Stats(profile_fname)
    # stats.strip_dirs().sort_stats('cumtime').print_stats(100)
    # stats.strip_dirs().sort_stats('calls').print_stats(100)
    # stats.strip_dirs().sort_stats('time').print_stats(100)

    unittest.main()
