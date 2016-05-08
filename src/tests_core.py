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

    app = wx.App(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)

    import unittest

    from test.treeloading import (WikiPagesTest,
                                  SubWikiTest,
                                  TextPageAttachmentTest)
    from test.treeloading_readonly import ReadonlyLoadTest, ReadonlyChangeTest
    from test.treecreation import TextPageCreationTest
    from test.treemanualedit import ManualEditTest
    from test.bookmarks import BookmarksTest
    from test.treeconfigpages import ConfigPagesTest
    from test.invalidwiki import InvalidWikiTest
    from test.factory import FactorySelectorTest
    from test.titletester import PageTitleTesterTest
    from test.tags import TagsListTest
    from test.pagedatetime import PageDateTimeTest

    from test.pagemove import MoveTest
    from test.attachment import AttachmentTest
    from test.pagerename import RenameTest
    from test.pageremove import RemovePagesTest
    from test.pageorder import PageOrderTest

    from test.thumbmakerwx import ThumbmakerWxTest
    from test.thumbmakerpil import ThumbmakerPilTest
    from test.pagethumbmaker import PageThumbmakerTest
    from test.thumbnails import ThumbnailsTest
    from test.htmlimproverbr import BrHtmlImproverTest
    from test.htmlimproverfactory import HtmlImproverFactoryTest
    from test.htmltemplate import HtmlTemplateTest
    from test.htmlpage.htmlpages import HtmlPagesTest

    from test.event import EventTest, EventsTest
    from test.config import (ConfigTest,
                             ConfigOptionsTest,
                             TrayConfigTest,
                             EditorConfigTest)

    from test.recent import RecentWikiTest
    from test.search import SearcherTest, SearchPageTest
    from test.localsearch import LocalSearchTest
    from test.i18n import I18nTest
    from test.version import VersionTest, StatusTest
    from test.treesort import TreeSortTest
    from test.emptycontent import EmptyContentTest
    from test.hotkey import HotKeyTest
    from test.hotkeyparser import HotKeyParserTest
    from test.hotkeyconfig import HotKeyConfigTest
    from test.history import HistoryTest
    from test.commandline import CommandLineTest
    from test.pageuiddepot import PageUidDepotTest
    from test.loader import PluginsLoaderTest
    from test.iconscollection import IconsCollectionTest
    from test.iconmaker import IconMakerTest
    from test.dicttostr import DictToStrTest

    from test.spellchecker.dictsfinder import DictsFinderTest
    from test.spellchecker.spellchecker import SpellCheckerTest

    from test.styles.styles import StylesTest
    from test.styles.styleslist import StylesListTest

    unittest.main()
