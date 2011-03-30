#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from core.tree import WikiDocument
from core.application import Application
from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parser.command import Command
from pages.wiki.parserfactory import ParserFactory
from pages.wiki.parser.commandbloggers import LjUserCommand, LjCommunityCommand
from utils import removeWiki


class WikiBloggersCommandTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.filesPath = u"../test/samplefiles/"
		self.__createWiki()
		
		factory = ParserFactory()
		self.parser = factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
		self.testPage = self.rootwiki[u"Страница 2"]
		

	def tearDown(self):
		removeWiki (self.path)


	def testLjUserCommand1 (self):
		command = LjUserCommand (self.parser)
		params = "jenyay_test"

		result_right =u"""<span class='ljuser ljuser-name_jenyay_test' lj:user='jenyay_test' style='white-space:nowrap'><a href='http://jenyay-test.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=2' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://jenyay-test.livejournal.com/'><b>jenyay_test</b></a></span>"""

		result = command.execute (params, u"")

		self.assertEqual (result, result_right)


	def testLjUserCommand2 (self):
		text = u"(:ljuser jenyay_test:)"

		result_right = u"""<span class='ljuser ljuser-name_jenyay_test' lj:user='jenyay_test' style='white-space:nowrap'><a href='http://jenyay-test.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=2' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://jenyay-test.livejournal.com/'><b>jenyay_test</b></a></span>"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right)


	def testLjCommunityCommand1 (self):
		command = LjCommunityCommand (self.parser)
		params = "ljournalist"

		result_right =u"""<span class='ljuser ljuser-name_ljournalist' lj:user='ljournalist' style='white-space:nowrap'><a href='http://community.livejournal.com/ljournalist/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=2' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://community.livejournal.com/ljournalist/'><b>ljournalist</b></a></span>"""

		result = command.execute (params, u"")

		self.assertEqual (result, result_right)


	def testLjCommunityCommand2 (self):
		text = u"(:ljcomm ljournalist:)"

		result_right = u"""<span class='ljuser ljuser-name_ljournalist' lj:user='ljournalist' style='white-space:nowrap'><a href='http://community.livejournal.com/ljournalist/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=2' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://community.livejournal.com/ljournalist/'><b>ljournalist</b></a></span>"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right)
