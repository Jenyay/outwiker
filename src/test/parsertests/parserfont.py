#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application

from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parserfactory import ParserFactory


class ParserFontTest (unittest.TestCase):
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


	def testBold (self):
		text = u"'''Полужирный'''"
		result = u"<B>Полужирный</B>"

		self.assertEqual (self.parser.toHtml (text), result)


	def testItalic (self):
		text = u"''Курсив''"
		result = u"<I>Курсив</I>"

		self.assertEqual (self.parser.toHtml (text), result)

	
	def testBoldItalic (self):
		text = u"''''Полужирный курсив''''"
		result = u"<B><I>Полужирный курсив</I></B>"

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testComboBoldItalic (self):
		text = u"Обычный текст \n''курсив'' \n'''полужирный ''внутри \nкурсив'' ''' 111"
		result = u"Обычный текст \n<I>курсив</I> \n<B>полужирный <I>внутри \nкурсив</I> </B> 111"

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testUnderline (self):
		text = u'бла-бла-бла \nкхм {+ это подчеркивание+} %% бла-бла-бла\nбла-бла-бла'
		result = u'бла-бла-бла \nкхм <U> это подчеркивание</U> %% бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testStrike (self):
		text = u'бла-бла-бла \nкхм {-это зачеркнутый текст-} %% бла-бла-бла\nбла-бла-бла'
		result = u'бла-бла-бла \nкхм <STRIKE>это зачеркнутый текст</STRIKE> %% бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


	def testStrikeUnderline (self):
		text = u'бла-бла-бла \nкхм {-{+это зачеркнутый подчеркнутый текст+}-} %% бла-бла-бла\nбла-бла-бла'
		result = u'бла-бла-бла \nкхм <STRIKE><U>это зачеркнутый подчеркнутый текст</U></STRIKE> %% бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
	

	def testSuperscript (self):
		text = u"бла-бла-бла \nкхм '^ это верхний индекс^' бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм <SUP> это верхний индекс</SUP> бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

	
	def testSubscript (self):
		text = u"бла-бла-бла \nкхм '_ это нижний индекс_' бла-бла-бла\nбла-бла-бла"
		result = u'бла-бла-бла \nкхм <SUB> это нижний индекс</SUB> бла-бла-бла\nбла-бла-бла'

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
