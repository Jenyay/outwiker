#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from core.tree import WikiDocument
from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from test.utils import removeWiki
from core.application import Application
from pages.wiki.parser.command import Command
from pages.wiki.parserfactory import ParserFactory


class WikiIncludeCommandTest (unittest.TestCase):
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
		
		files = [u"text_utf8.txt", u"text_utf8.txt2", u"image.gif", 
				u"текст_utf8.txt", u"text_1251.txt", u"html.txt", 
				u"html_1251.txt", u"wiki.txt"]

		fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.testPage.attach (fullFilesPath)
	

	def tearDown(self):
		removeWiki (self.path)


	def testIncludeCommand1 (self):
		text = u"""бла-бла-бла
(:include Attach:text_utf8.txt :)"""

		result_right = u"""бла-бла-бла
Текст в 
кодировке UTF-8"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand2 (self):
		text = u"""бла-бла-бла
(:include Attach:text_utf8.txt param param1="www" :)"""

		result_right = u"""бла-бла-бла
Текст в 
кодировке UTF-8"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand3 (self):
		text = u"""бла-бла-бла
(:include Attach:text_utf8.txt2:)"""

		result_right = u"""бла-бла-бла
Текст2 в 
кодировке UTF-8"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand4 (self):
		text = u"""бла-бла-бла
(:include Attach:text_utf8.txt2 param param1="www":)"""

		result_right = u"""бла-бла-бла
Текст2 в 
кодировке UTF-8"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand5 (self):
		text = u"""бла-бла-бла
(:include Attach:текст_utf8.txt param param1="www":)"""

		result_right = u"""бла-бла-бла
Текст в 
кодировке UTF-8"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand6 (self):
		text = u"""бла-бла-бла
(:include Attach:текст_utf8.txt :)"""

		result_right = u"""бла-бла-бла
Текст в 
кодировке UTF-8"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand7 (self):
		text = u"""бла-бла-бла
(:include Attach:text_1251.txt encoding=cp1251 :)"""

		result_right = u"""бла-бла-бла
Это текст
в кодировке 1251"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand8 (self):
		text = u"""бла-бла-бла
(:include Attach:text_1251.txt encoding = "cp1251" :)"""

		result_right = u"""бла-бла-бла
Это текст
в кодировке 1251"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand9 (self):
		text = u"""бла-бла-бла
(:include Attach:text_1251.txt encoding="cp1251" :)"""

		result_right = u"""бла-бла-бла
Это текст
в кодировке 1251"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand10 (self):
		text = u"""бла-бла-бла (:include Attach:html.txt htmlescape:)"""

		result_right = u"""бла-бла-бла &lt;B&gt;Это текст с HTML-тегами&lt;/B&gt;"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommand11 (self):
		text = u"""бла-бла-бла (:include Attach:html_1251.txt htmlescape encoding="cp1251":)"""

		result_right = u"""бла-бла-бла &lt;B&gt;Это текст с HTML-тегами&lt;/B&gt;"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)
		

	def testIncludeCommand12 (self):
		text = u"""бла-бла-бла (:include Attach:wiki.txt wikiparse:)"""

		result_right = u"""бла-бла-бла <B>Этот текст содержит вики-нотацию</B>"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommandInvalid1 (self):
		text = u"""бла-бла-бла(:include Attach:text_utf8_1.txt :)"""

		result_right = u"""бла-бла-бла"""

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommandInvalid2 (self):
		text = u"""бла-бла-бла(:include Attach:image.gif :)"""

		result_right = u"""бла-бла-бла""" + _(u"<B>Encoding error in file image.gif</B>")

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)


	def testIncludeCommandInvalid3 (self):
		text = u"""бла-бла-бла(:include Attach:image.gif encoding=base64 :)"""

		result_right = u"""бла-бла-бла""" + _(u"<B>Encoding error in file image.gif</B>")

		result = self.parser.toHtml (text)
		self.assertEqual (result, result_right, result)
