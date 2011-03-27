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

	from test.wikicreation import TextPageAttachmentTest, TextPageCreationTest, \
			ConfigPagesTest, BookmarksTest, RemovePagesTest, RenameTest

	from test.utils import removeWiki
	from test.event import EventTest, EventsTest
	from test.factory import FactorySelectorTest
	from test.invalidwiki import InvalidWikiTest
	from test.config import ConfigTest, ConfigOptionsTest, TrayConfigTest, EditorConfigTest
	from test.recent import RecentWikiTest
	from test.search import SearcherTest, TagsListTest, SearchPageTest
	from test.localsearch import LocalSearchTest
	from test.movepages import MoveTest
	from test.parser import ParserTest
	from test.htmlimprover_test import HtmlImproverTest
	from test.wikiloading_readonly import ReadonlyLoadTest, ReadonlyChangeTest
	from test.i18n import I18nTest
	from test.version import VersionTest, StatusTest
	from test.pageorder import PageOrderTest
	from test.commands import CommandsTest
	from test.wxthumbmaker import WxThumbmakerTest
	from test.pagethumbmaker import PageThumbmakerTest
	from test.thumbnails import ThumbnailsTest
	from test.wikicommands import WikiCommandsTest
	from test.wikicommandinclude import WikiIncludeCommandTest
	from test.wikicommandbloggers import WikiBloggersCommandTest
	from test.wikicommandchildlist import WikiChildListCommandTest


	unittest.main()
