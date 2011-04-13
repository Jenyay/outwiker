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
	class testApp(wx.App):
		def __init__(self, *args, **kwds):
			wx.App.__init__ (self, *args, **kwds)

	app = testApp(redirect=False)

	import unittest

	from test.wikiloading import WikiPagesTest, SubWikiTest
	from test.wikiloading_readonly import ReadonlyLoadTest, ReadonlyChangeTest
	from test.wikicreation import TextPageCreationTest, ConfigPagesTest, BookmarksTest
	from test.invalidwiki import InvalidWikiTest
	from test.factory import FactorySelectorTest

	from test.pagemove import MoveTest
	from test.attachment import AttachmentTest
	from test.pagerename import RenameTest
	from test.pageremove import RemovePagesTest
	from test.pageorder import PageOrderTest

	from test.parserfont import ParserFontTest
	from test.parserformat import ParserFormatTest
	from test.parsermisc import ParserMiscTest
	from test.parserlink import ParserLinkTest
	from test.parserattach import ParserAttachTest
	from test.parserimages import ParserImagesTest
	from test.parserheading import ParserHeadingTest
	from test.parserthumb import ParserThumbTest
	from test.parseralign import ParserAlignTest
	from test.parserlist import ParserListTest
	from test.parsertable import ParserTableTest
	from test.parseradhoc import ParserAdHocTest
	from test.parserurl import ParserUrlTest
	from test.parsertex import ParserTexTest
	from test.parserlinebreak import ParserLineBreakTest

	from test.wikicommands import WikiCommandsTest
	from test.wikicommandinclude import WikiIncludeCommandTest
	from test.wikicommandbloggers import WikiBloggersCommandTest
	from test.wikicommandchildlist import WikiChildListCommandTest
	from test.wikicommandattachlist import WikiAttachListCommandTest

	from test.wxthumbmaker import WxThumbmakerTest
	from test.pagethumbmaker import PageThumbmakerTest
	from test.thumbnails import ThumbnailsTest
	from test.htmlimprover_test import HtmlImproverTest
	from test.wikihtmlgenerator import WikiHtmlGeneratorTest	

	from test.utils import removeWiki
	from test.event import EventTest, EventsTest
	from test.config import ConfigTest, ConfigOptionsTest, TrayConfigTest, EditorConfigTest
	from test.recent import RecentWikiTest
	from test.search import SearcherTest, TagsListTest, SearchPageTest
	from test.localsearch import LocalSearchTest	
	from test.i18n import I18nTest
	from test.version import VersionTest, StatusTest
	from test.commands import CommandsTest


	unittest.main()
