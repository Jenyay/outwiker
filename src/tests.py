#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""
import gettext
import os
import core.system

langdir = os.path.join (core.system.getCurrentDir(), u'locale')
lang = gettext.translation(u'outwiker', langdir, languages=["en"])
lang.install(unicode=1)


if __name__ == '__main__':
	import unittest

	from test.wikiloading import WikiPagesTest, SubWikiTest

	from test.wikicreation import TextPageAttachmentTest, TextPageCreationTest, \
			ConfigPagesTest, BookmarksTest, RemovePagesTest, RenameTest

	from test.utils import removeWiki
	from test.event import EventTest, EventsTest
	from test.factory import FactorySelectorTest
	from test.invalidwiki import InvalidWikiTest
	from test.config import ConfigTest, ConfigOptionsTest
	from test.recent import RecentWikiTest
	from test.search import SearcherTest, TagsListTest, SearchPageTest
	from test.localsearch import LocalSearchTest
	from test.movepages import MoveTest
	from test.parser import ParserTest
	from test.htmlimprover_test import HtmlImproverTest
	from test.wikiloading_readonly import ReadonlyLoadTest, ReadonlyChangeTest

	unittest.main()
