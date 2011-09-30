#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
import time

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.config import Config

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.pages.wiki.emptycontent import EmptyContent

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


	def testCacheRename (self):
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

		# Изменили заголовок
		self.testPage.title = u"Новый заголовок"

		# Добавим файл
		self.assertFalse (generator.canReadFromCache())
		generator.makeHtml ()
		self.assertTrue (generator.canReadFromCache())


	def testCacheEmpty1 (self):
		emptycontent = EmptyContent (Application.config)
		self.testPage.content = u""

		# Только создали страницу, кешировать нельзя
		generator = HtmlGenerator (self.testPage)
		self.assertFalse (generator.canReadFromCache())
		generator.makeHtml ()

		# Страница пустая, изменился шаблон для путой записи
		emptycontent.content = u"1111"
		self.assertFalse (generator.canReadFromCache())
		generator.makeHtml ()

		# Изменилось содержимое страницы
		self.testPage.content = u"Бла-бла-бла"
		self.assertFalse (generator.canReadFromCache())
		generator.makeHtml ()

		self.assertTrue (generator.canReadFromCache())
		generator.makeHtml ()

		# Изменился шаблон страницы, но страница уже не пустая
		emptycontent.content = u"2222"
		self.assertTrue (generator.canReadFromCache())


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


	def testCacheSubpages (self):
		"""
		Проверка кэширования при добавлении новых подстраниц
		"""
		# Только создали страницу, кешировать нельзя
		generator = HtmlGenerator (self.testPage)
		self.assertFalse (generator.canReadFromCache())

		generator.makeHtml ()
		self.assertTrue (generator.canReadFromCache())

		# Добавляем новую подстраницу
		WikiPageFactory.create (self.testPage, u"Подстраница 1", [])
		self.assertFalse (generator.canReadFromCache())

		generator.makeHtml ()
		self.assertTrue (generator.canReadFromCache())


	def testEmpty1 (self):
		#config = Config (self.configpath)
		text = u"бла-бла-бла"

		content = EmptyContent (Application.config)
		content.content = text

		# Очистим содержимое, чтобы использовать EmptyContent
		self.testPage.content = u""

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml()

		# Проверим, что в результирующем файле есть содержимое text
		with open (htmlpath) as fp:
			result = unicode (fp.read(), "utf8")

		self.assertTrue (text in result)


	def testEmpty2 (self):
		#config = Config (self.configpath)
		text = u"(:attachlist:)"

		content = EmptyContent (Application.config)
		content.content = text

		# Очистим содержимое, чтобы использовать EmptyContent
		self.testPage.content = u""

		generator = HtmlGenerator (self.testPage)
		htmlpath = generator.makeHtml()

		# Проверим, что в результирующем файле есть содержимое text
		with open (htmlpath) as fp:
			result = unicode (fp.read(), "utf8")

		self.assertTrue (u"image.jpg" in result)
