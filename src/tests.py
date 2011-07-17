#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""
import gettext
import os

import wx

import core.system
from core.application import Application

Application.init ("../test/testconfig.ini")

if __name__ == '__main__':
	app = wx.PySimpleApp(redirect=False)
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

	from test.pagemove import MoveTest
	from test.attachment import AttachmentTest
	from test.pagerename import RenameTest
	from test.pageremove import RemovePagesTest
	from test.pageorder import PageOrderTest

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
	from test.parsertests.wikicommandbloggers import WikiBloggersCommandTest
	from test.parsertests.wikicommandchildlist import WikiChildListCommandTest
	from test.parsertests.wikicommandattachlist import WikiAttachListCommandTest

	from test.wxthumbmaker import WxThumbmakerTest
	from test.pagethumbmaker import PageThumbmakerTest
	from test.thumbnails import ThumbnailsTest
	from test.htmlimprover import HtmlImproverTest
	from test.wikihtmlgenerator import WikiHtmlGeneratorTest
	from test.htmltemplate import HtmlTemplateTest

	from test.utils import removeWiki
	from test.event import EventTest, EventsTest
	from test.config import ConfigTest, ConfigOptionsTest, TrayConfigTest, EditorConfigTest
	from test.recent import RecentWikiTest
	from test.search import SearcherTest, TagsListTest, SearchPageTest
	from test.localsearch import LocalSearchTest
	from test.i18n import I18nTest
	from test.version import VersionTest, StatusTest
	from test.treesort import TreeSortTest
	from test.emptycontent import EmptyContentTest

	#from test.guitests.tray import TrayNormalTest#, TrayIconizedTest
	from test.guitests.mainid import MainIdTest
	from test.guitests.mainwnd import MainWndTest
	from test.guitests.bookmarks import BookmarksGuiTest
	from test.guitests.attach import AttachPanelTest
	from test.guitests.tree import TreeTest
	from test.guitests.pagepanel import PagePanelTest


	#f = open('tests.log', "w")
	#runner = unittest.TextTestRunner(f)
	#unittest.main(testRunner=runner)
	unittest.main()
