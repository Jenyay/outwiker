#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
import time


from core.tree import WikiDocument
from core.attachment import Attachment
from core.application import Application
from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parserfactory import ParserFactory
from pages.wiki.htmlgenerator import HtmlGenerator
from utils import removeWiki


class WikiHtmlGeneratorTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "866"

		self.filesPath = u"../test/samplefiles/"
		self.__createWiki()
		
		factory = ParserFactory()
		self.parser = factory.make (self.testPage, Application.config)

		files = [u"image.jpg", u"dir"]

		fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

		self.attach_page2 = Attachment (self.rootwiki[u"Страница 2"])

		# Прикрепим к двум страницам файлы
		Attachment (self.testPage).attach (fullFilesPath)

		self.wikitext = u"""Бла-бла-бла
%thumb maxsize=250%Attach:image.jpg%%
Бла-бла-бла"""

		self.testPage.content = self.wikitext
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
		self.testPage = self.rootwiki[u"Страница 2"]
		

	def tearDown(self):
		removeWiki (self.path)


	def test1 (self):
		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml ()

		self.assertEqual (htmlpath, os.path.join (self.testPage.path, u"__content.html"))
		self.assertTrue (os.path.exists (htmlpath))


	def testCache1 (self):
		# Только создали страницу, кешировать нельзя
		generator = HtmlGenerator (self.testPage)
		self.assertFalse (generator.canReadFromCache())

		generator.makeHtml ()
		# После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
		self.assertTrue (generator.canReadFromCache())

		self.testPage.content = u"бла-бла-бла"

		# Изменили содержимое страницы, опять нельзя кешировать
		self.assertFalse (generator.canReadFromCache())
		generator.makeHtml ()
		self.assertTrue (generator.canReadFromCache())

		# Добавим файл
		attach = Attachment (self.testPage)
		attach.attach ([os.path.join (self.filesPath, u"add.png")])

		self.assertFalse (generator.canReadFromCache())
		generator.makeHtml ()
		self.assertTrue (generator.canReadFromCache())


	def testCache2 (self):
		# Только создали страницу, кешировать нельзя
		generator = HtmlGenerator (self.testPage)

		path = generator.makeHtml ()
		ftime = os.stat(path).st_mtime
		time.sleep (0.1)

		path2 = generator.makeHtml ()
		ftime2 = os.stat(path).st_mtime

		self.assertEqual (ftime, ftime2)
		time.sleep (0.1)

		# Изменили содержимое страницы, опять нельзя кешировать
		self.testPage.content = u"бла-бла-бла"
		path3 = generator.makeHtml ()
		ftime3 = os.stat(path).st_mtime

		self.assertNotEqual (ftime2, ftime3)
		time.sleep (0.1)

		path4 = generator.makeHtml ()
		ftime4 = os.stat(path).st_mtime

		self.assertEqual (ftime3, ftime4)
		time.sleep (0.1)

		# Добавим файл
		attach = Attachment (self.testPage)
		attach.attach ([os.path.join (self.filesPath, u"add.png")])

		path5 = generator.makeHtml ()
		ftime5 = os.stat(path).st_mtime

		self.assertNotEqual (ftime4, ftime5)
		time.sleep (0.1)

		path6 = generator.makeHtml ()
		ftime6 = os.stat(path).st_mtime

		self.assertEqual (ftime5, ftime6)


	def testCacheSubdir (self):
		attach = Attachment (self.testPage)

		# Только создали страницу, кешировать нельзя
		generator = HtmlGenerator (self.testPage)
		self.assertFalse (generator.canReadFromCache())

		generator.makeHtml ()
		# После того, как один раз сгенерили страницу, если ничего не изменилось, можно кешировать
		self.assertTrue (generator.canReadFromCache())

		# Добавим файл в dir
		with open (os.path.join (attach.getAttachPath(), "dir", "temp.tmp"), "w" ) as fp:
			fp.write ("bla-bla-bla")

		self.assertFalse (generator.canReadFromCache())

		# Добавим еще одну вложенную директорию
		subdir = os.path.join (attach.getAttachPath(), "dir", "subdir")
		os.mkdir (subdir)
		self.assertFalse (generator.canReadFromCache())

		generator.makeHtml ()

		# Добавим файл в dir/subdir
		with open (os.path.join (subdir, "temp2.tmp"), "w" ) as fp:
			fp.write ("bla-bla-bla")

		self.assertFalse (generator.canReadFromCache())
