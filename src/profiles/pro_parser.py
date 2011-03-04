#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import cProfile

from core.tree import RootWikiPage, WikiDocument
from pages.wiki.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from test.utils import removeWiki


class ParseSample (object):
	def __init__ (self, fname):
		self.filesPath = u"../test/samplefiles/"

		self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
		self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

		with open (fname) as fp:
			self.content = unicode (fp.read (), "utf8")

		self.__createWiki()

		self.parser = Parser(self.testPage, maxSizeThumb = 250)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])

		self.testPage = self.rootwiki[u"Страница 2"]
		self.testPage.content = self.content
		
		files = [u"accept.png", u"add.png", u"anchor.png", u"filename.tmp", 
				u"файл с пробелами.tmp", u"картинка с пробелами.png", 
				"image.jpg", "image.jpeg", "image.png", "image.tif", "image.tiff", "image.gif", "first.jpg", "first_rotate.jpg"]

		fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

		# Прикрепим к двум страницам файлы
		self.testPage.attach (fullFilesPath)

	
	def run (self):
		result = self.parser.toHtml (self.testPage.content)

		removeWiki (self.path)
