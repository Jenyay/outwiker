#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parser.command import Command
from pages.wiki.parserfactory import ParserFactory
from pages.wiki.parser.commandbloggers import LjUserCommand, LjCommunityCommand
from test.utils import removeWiki


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
		params = "a_str"

		result_right =u"""<span class='ljuser ljuser-name_a_str' lj:user='a_str' style='white-space:nowrap'><a href='http://a-str.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=3' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://a-str.livejournal.com/'><b>a_str</b></a></span>"""

		result = command.execute (params, u"")

		self.assertEqual (result, result_right)


	def testLjUserCommand2 (self):
		text = u"(:ljuser a_str:)"

		result_right = u"""<span class='ljuser ljuser-name_a_str' lj:user='a_str' style='white-space:nowrap'><a href='http://a-str.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=3' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://a-str.livejournal.com/'><b>a_str</b></a></span>"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right)


	def testLjCommunityCommand1 (self):
		command = LjCommunityCommand (self.parser)
		params = "american_gangst"

		result_right =u"""<span class='ljuser ljuser-name_american_gangst' lj:user='american_gangst' style='white-space:nowrap'><a href='http://american-gangst.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=3' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://american-gangst.livejournal.com/'><b>american_gangst</b></a></span>"""

		result = command.execute (params, u"")

		self.assertEqual (result, result_right)


	def testLjCommunityCommand2 (self):
		text = u"(:ljcomm american_gangst:)"

		result_right = u"""<span class='ljuser ljuser-name_american_gangst' lj:user='american_gangst' style='white-space:nowrap'><a href='http://american-gangst.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=3' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://american-gangst.livejournal.com/'><b>american_gangst</b></a></span>"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right)
