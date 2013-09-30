#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""
import os

import wxversion

try:
    wxversion.select("2.8")
except wxversion.VersionError:
    if os.name == "nt":
        pass
    else:
        raise

import wx

from outwiker.core.application import Application

Application.init ("../test/testconfig.ini")

if __name__ == '__main__':
    app = wx.PySimpleApp(redirect=False)

    def emptyFunc():
        pass

    app.bindActivateApp = emptyFunc
    app.unbindActivateApp = emptyFunc
    loop = wx.EventLoop()
    wx.EventLoop.SetActive(loop)

    import unittest

    from test.treeloading import WikiPagesTest, SubWikiTest, TextPageAttachmentTest
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

    from test.parsertests.tokennames import TokenNamesTest
    from test.parsertests.parserfont import ParserFontTest
    from test.parsertests.parserformat import ParserFormatTest
    from test.parsertests.parsermisc import ParserMiscTest
    from test.parsertests.parserlink import ParserLinkTest
    from test.parsertests.parserattach import ParserAttachTest
    from test.parsertests.parserimages import ParserImagesTest
    from test.parsertests.parserheading import ParserHeadingTest
    from test.parsertests.parserthumb import ParserThumbTest
    from test.parsertests.parseralign import ParserAlignTest
    from test.parsertests.parserlist import ParserListTest
    from test.parsertests.parsertable import ParserTableTest
    from test.parsertests.parseradhoc import ParserAdHocTest
    from test.parsertests.parserurl import ParserUrlTest
    from test.parsertests.parsertex import ParserTexTest
    from test.parsertests.parserlinebreak import ParserLineBreakTest

    from test.parsertests.wikicommands import WikiCommandsTest
    from test.parsertests.wikicommandinclude import WikiIncludeCommandTest
    from test.parsertests.wikicommandchildlist import WikiChildListCommandTest
    from test.parsertests.wikicommandattachlist import WikiAttachListCommandTest
    from test.parsertests.wikicommandcounter import WikiCounterCommandTest

    from test.wxthumbmaker import WxThumbmakerTest
    from test.pagethumbmaker import PageThumbmakerTest
    from test.thumbnails import ThumbnailsTest
    from test.htmlimprover import HtmlImproverTest
    from test.wikihtmlgenerator import WikiHtmlGeneratorTest
    from test.wikihash import WikiHashTest
    from test.htmltemplate import HtmlTemplateTest
    from test.htmlpages import HtmlPagesTest
    from test.wikilinkcreator import WikiLinkCreatorTest

    from test.utils import removeWiki
    from test.event import EventTest, EventsTest
    from test.config import ConfigTest, ConfigOptionsTest, TrayConfigTest, EditorConfigTest
    from test.recent import RecentWikiTest
    from test.search import SearcherTest, SearchPageTest
    from test.localsearch import LocalSearchTest
    from test.i18n import I18nTest
    from test.version import VersionTest, StatusTest
    from test.treesort import TreeSortTest
    from test.emptycontent import EmptyContentTest
    from test.hotkey import HotKeyTest

    #from test.guitests.tray import TrayNormalTest#, TrayIconizedTest
    from test.guitests.mainid import MainIdTest
    from test.guitests.mainwnd import MainWndTest
    from test.guitests.bookmarks import BookmarksGuiTest
    from test.guitests.attach import AttachPanelTest
    from test.guitests.tree import TreeTest
    from test.guitests.pagepanel import PagePanelTest
    from test.guitests.tagspanel import TagsPanelTest
    from test.guitests.tabs import TabsTest
    from test.guitests.linkdialogcontrollertest import LinkDialogControllerTest
    from test.guitests.thumbdialogcontrollertest import ThumbDialogControllerTest
    from test.guitests.wikipagepanel import WikiPagePanelTest
    from test.guitests.htmlpagepanel import HtmlPagePanelTest
    from test.guitests.actioncontroller import ActionControllerTest
    from test.guitests.mainpanes import MainPanesTest
    from test.guitests.fullscreen import FullScreenTest

    from test.plugins.loader import PluginsLoaderTest
    from test.plugins.testwikicommand import PluginWikiCommandTest
    from test.plugins.style import StylePluginTest
    from test.plugins.export2html import Export2HtmlTest
    from test.plugins.spoiler import SpoilerPluginTest
    from test.plugins.livejournal import LivejournalPluginTest
    from test.plugins.lightbox import LightboxPluginTest
    from test.plugins.thumblist import ThumbListPluginTest
    from test.plugins.pagestatistics import PageStatisticsTest
    from test.plugins.treestatistics import TreeStatisticsTest
    from test.plugins.updatenotifier import UpdateNotifierTest

    from test.plugins.source.source import SourcePluginTest
    from test.plugins.source.sourceencoding import SourceEncodingPluginTest
    from test.plugins.source.sourcefile import SourceFilePluginTest
    from test.plugins.source.sourcegui import SourceGuiPluginTest
    from test.plugins.source.sourceattachment import SourceAttachmentPluginTest
    from test.plugins.source.sourcestyle import SourceStyleTest

    from test.styles.styles import StylesTest
    from test.styles.styleslist import StylesListTest

    if os.name == "nt":
        from test.guitests.uriidentifiers import UriIdentifierIETest
    else:
        from test.guitests.uriidentifiers import UriIdentifierWebKitTest

    #f = open('tests.log', "w")
    #runner = unittest.TextTestRunner(f)
    #unittest.main(testRunner=runner)
    unittest.main()
