#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Unit-тесты
"""

import unittest

from test.wikiloading import WikiPagesTest, SubWikiTest

from test.wikicreation import TextPageAttachmentTest, TextPageCreationTest, \
		ConfigPagesTest, BookmarksTest, RemovePagesTest, RenameTest

from test.utils import removeWiki
from test.event import EventTest, EventsTest
from test.factory import FactorySelectorTest
from test.invalidwiki import InvalidWikiTest
from test.config import ConfigTest
from test.recent import RecentWikiTest
from test.search import SearcherTest, TagsListTest, SearchPageTest
from test.localsearch import LocalSearchTest
from test.movepages import MoveTest
from test.parser import ParserTest


if __name__ == '__main__':
	unittest.main()
