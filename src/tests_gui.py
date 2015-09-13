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

    from test.guitests.mainwnd import MainWndTest
    from test.guitests.bookmarks import BookmarksGuiTest
    from test.guitests.attach import AttachPanelTest
    from test.guitests.tree import TreeTest
    from test.guitests.pagepanel import PagePanelTest
    from test.guitests.tagspanel import TagsPanelTest
    from test.guitests.tabs import TabsTest
    from test.guitests.linkdialogcontrollertest import LinkDialogControllerTest
    from test.guitests.thumbdialogcontrollertest import ThumbDialogControllerTest
    from test.guitests.textpageview import TextPageViewTest
    from test.guitests.actioncontroller import ActionControllerTest
    from test.guitests.mainpanes import MainPanesTest
    from test.guitests.fullscreen import FullScreenTest
    from test.guitests.texteditor import TextEditorTest
    from test.guitests.fileicons import FileIconsTestUnix
    from test.guitests.stcstyleparser import StcStyleParserTest
    from test.guitests.childlistdialog import ChildListDialogTest
    from test.guitests.attachlistdialog import AttachListDialogTest
    from test.guitests.includedialog import IncludeDialogTest
    from test.guitests.removepage import RemovePageGuiTest
    from test.guitests.renamepage import RenamePageGuiTest
    from test.guitests.movepage import MovePageGuiTest
    from test.guitests.openwiki import OpenWikiGuiTest
    from test.guitests.newwiki import NewWikiGuiTest
    from test.guitests.pagetabs import PageTabsTest
    from test.guitests.fileicons import FileIconsTestWindows
    from test.guitests.uriidentifiers import UriIdentifierIETest
    from test.guitests.uriidentifiers import UriIdentifierWebKitTest

    from test.guitests.htmlpage.htmlpageview import HtmlPageViewTest
    from test.guitests.htmlpage.htmltabledialog import HtmlTableDialogTest
    from test.guitests.htmlpage.htmltablerowsdialog import HtmlTableRowsDialogTest
    from test.guitests.htmlpage.htmltableactions import HtmlTableActionsTest

    from test.guitests.wikipage.wikipageview import WikiPageViewTest
    from test.guitests.wikipage.wikitabledialog import WikiTableDialogTest
    from test.guitests.wikipage.wikitablerowsdialog import WikiTableRowsDialogTest
    from test.guitests.wikipage.wikitableactions import WikiTableActionsTest

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
