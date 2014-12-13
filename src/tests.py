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
    from test.parsertests.parserquote import ParserQuoteTest

    from test.parsertests.wikicommands import WikiCommandsTest
    from test.parsertests.wikicommandinclude import WikiIncludeCommandTest
    from test.parsertests.wikicommandchildlist import WikiChildListCommandTest
    from test.parsertests.wikicommandattachlist import WikiAttachListCommandTest
    from test.parsertests.wikicommanddates import WikiCommandDatesTest

    from test.thumbmakerwx import ThumbmakerWxTest
    from test.thumbmakerpil import ThumbmakerPilTest
    from test.pagethumbmaker import PageThumbmakerTest
    from test.thumbnails import ThumbnailsTest
    from test.htmlimprover import HtmlImproverTest
    from test.wikihtmlcache import WikiHtmlCacheTest
    from test.wikihtmlgenerator import WikiHtmlGeneratorTest
    from test.wikihash import WikiHashTest
    from test.htmltemplate import HtmlTemplateTest
    from test.htmlpages import HtmlPagesTest
    from test.wikilinkcreator import WikiLinkCreatorTest

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
    from test.hotkeyparser import HotKeyParserTest
    from test.hotkeyconfig import HotKeyConfigTest
    from test.history import HistoryTest
    from test.commandline import CommandLineTest
    from test.pageuiddepot import PageUidDepotTest
    from test.loader import PluginsLoaderTest
    from test.iconscollection import IconsCollectionTest
    from test.iconmaker import IconMakerTest

    # from test.guitests.tray import TrayNormalTest#, TrayIconizedTest
    from test.guitests.mainwnd import MainWndTest
    from test.guitests.bookmarks import BookmarksGuiTest
    from test.guitests.attach import AttachPanelTest
    from test.guitests.tree import TreeTest
    from test.guitests.pagepanel import PagePanelTest
    from test.guitests.tagspanel import TagsPanelTest
    from test.guitests.tabs import TabsTest
    from test.guitests.linkdialogcontrollertest import LinkDialogControllerTest
    from test.guitests.thumbdialogcontrollertest import ThumbDialogControllerTest
    from test.guitests.wikipageview import WikiPageViewTest
    from test.guitests.htmlpageview import HtmlPageViewTest
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

    if os.name == "nt":
        from test.guitests.fileicons import FileIconsTestWindows

    from test.plugins.template import TemplateTest
    from test.plugins.testplugin.testpage import TestPageTest
    from test.plugins.testplugin.testwikicommand import PluginWikiCommandTest

    from test.plugins.style.loading import StyleLoadingTest
    from test.plugins.style.style import StylePluginTest

    from test.plugins.export2html.export2html import Export2HtmlTest
    from test.plugins.export2html.loading import Export2HtmlLoadingTest

    from test.plugins.spoiler.loading import SpoilerLoadingTest
    from test.plugins.spoiler.spoiler import SpoilerPluginTest

    from test.plugins.livejournal.loading import LivejournalLoadingTest
    from test.plugins.livejournal.livejournal import LivejournalPluginTest

    from test.plugins.lightbox.loading import LightboxLoadingTest
    from test.plugins.lightbox.lightbox import LightboxPluginTest

    from test.plugins.thumbgallery.loading import ThumbGalleryLoadingTest
    from test.plugins.thumbgallery.thumblist import ThumbListPluginTest

    from test.plugins.statistics.loading import StatisticsLoadingTest
    from test.plugins.statistics.pagestatistics import PageStatisticsTest
    from test.plugins.statistics.treestatistics import TreeStatisticsTest

    from test.plugins.updatenotifier.loading import UpdateNotifierLoadingTest
    from test.plugins.updatenotifier.updatenotifier import UpdateNotifierTest

    from test.plugins.counter.counter import CounterTest
    from test.plugins.counter.counterdialog import CounterDialogTest
    from test.plugins.counter.loading import CounterLoadingTest

    from test.plugins.htmlheads.loading import HtmlHeadsLoadingTest
    from test.plugins.htmlheads.htmlheads import HtmlHeadsTest

    from test.plugins.changepageuid.changepageuid import ChangePageUidTest
    from test.plugins.changepageuid.loading import ChangePageUIDLoadingTest

    from test.plugins.sessions.loading import SessionsLoadingTest
    from test.plugins.sessions.sessions import SessionsTest

    from test.plugins.diagrammer.diagrammer import DiagrammerTest
    from test.plugins.diagrammer.insertnode import InsertNodeTest
    from test.plugins.diagrammer.insertdiagram import InsertDiagramTest
    from test.plugins.diagrammer.insertedge import InsertEdgeTest
    from test.plugins.diagrammer.insertgroup import InsertGroupTest
    from test.plugins.diagrammer.loading import DiagrammerLoadingTest

    from test.plugins.tableofcontents.toc_parser import TOC_ParserTest
    from test.plugins.tableofcontents.toc_generator import TOC_GeneratorTest
    from test.plugins.tableofcontents.toc_wikimaker import TOC_WikiMakerTest
    from test.plugins.tableofcontents.loading import TOCLoadingTest

    from test.plugins.source.source import SourcePluginTest
    from test.plugins.source.sourceencoding import SourceEncodingPluginTest
    from test.plugins.source.sourcefile import SourceFilePluginTest
    from test.plugins.source.sourcegui import SourceGuiPluginTest
    from test.plugins.source.sourceattachment import SourceAttachmentPluginTest
    from test.plugins.source.sourcestyle import SourceStyleTest
    from test.plugins.source.loading import SourceLoadingTest

    from test.plugins.datagraph.loading import DataGraphLoadingTest
    from test.plugins.datagraph.paramsparsing import ParamsParsingTest

    from test.styles.styles import StylesTest
    from test.styles.styleslist import StylesListTest

    if os.name == "nt":
        from test.guitests.uriidentifiers import UriIdentifierIETest
    else:
        from test.guitests.uriidentifiers import UriIdentifierWebKitTest

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
