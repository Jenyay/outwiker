#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from utils import removeWiki

from core.tree import WikiDocument
from core.attachment import Attachment
from core.application import Application

from pages.wiki.parser.wikiparser import Parser
from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.parserfactory import ParserFactory


class ParserLinkTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "866"

		self.filesPath = u"../test/samplefiles/"

		self.url1 = u"http://example.com"
		self.url2 = u"http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"

		self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
		self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

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
		
		files = [u"accept.png", u"add.png", u"anchor.png", u"filename.tmp", 
				u"файл с пробелами.tmp", u"картинка с пробелами.png", 
				u"image.jpg", u"image.jpeg", u"image.png", u"image.tif", u"image.tiff", u"image.gif",
				u"image_01.JPG", u"dir", u"dir.xxx", u"dir.png"]

		fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

		self.attach_page2 = Attachment (self.rootwiki[u"Страница 2"])

		# Прикрепим к двум страницам файлы
		Attachment (self.testPage).attach (fullFilesPath)
	

	def tearDown(self):
		removeWiki (self.path)


	def testUrl1 (self):
		text = u"бла-бла-бла \n%s бла-бла-бла\nбла-бла-бла" % (self.url1)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testUrl2 (self):
		text = u"бла-бла-бла \ntest %s бла-бла-бла\nбла-бла-бла" % (self.url2)
		result = u'бла-бла-бла \ntest <A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, self.url2)

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testLink1 (self):
		text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.url1)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testLink2 (self):
		text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (self.url2)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, self.url2)

		self.assertEqual (self.parser.toHtml (text), result)


	def testLink3 (self):
		url = "http://jenyay.net/social/feed.png"

		text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (url)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (url, url)

		self.assertEqual (self.parser.toHtml (text), result)


	def testLink4 (self):
		text = u"[[http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431 | Ссылко]]"
		result = u'<A HREF="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</A>'

		self.assertEqual (self.parser.toHtml (text), result)

	
	def testLink5 (self):
		text = u"[[Ссылко -> http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431]]"
		result = u'<A HREF="http://rapidshare.com/#!download|514l34|373912473|ansys_hfss_12.1_with_fix.part1.rar|100431">Ссылко</A>'

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testCommentLink1 (self):
		comment = u"Ссылко"
		text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

		self.assertEqual (self.parser.toHtml (text), result)


	def testCommentLink2 (self):
		comment = u"Ссылко"
		text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, comment)

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testCommentLink3 (self):
		comment = u"Ссылко с '''полужирным''' текстом"
		text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (self.url2, comment)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, u"Ссылко с <B>полужирным</B> текстом")

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testCommentLink4 (self):
		comment = u"Ссылко с '''полужирным''' текстом"
		text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, self.url2)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url2, u"Ссылко с <B>полужирным</B> текстом")

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testCommentLink5 (self):
		text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (self.url1, self.url1)
		result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (self.url1, self.url1)

		self.assertEqual (self.parser.toHtml (text), result)
	

	def testPageLinks (self):
		for link in self.pagelinks:
			text = u"бла-бла-бла \n[[%s]] бла-бла-бла\nбла-бла-бла" % (link)
			result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (link, link)

			self.assertEqual (self.parser.toHtml (text), result)


	def testNoFormatLinks1 (self):
		for link in self.pagelinks:
			text = u"бла-бла-бла \n[[%s | [='''ля-ля-ля'''=] ]] бла-бла-бла\nбла-бла-бла" % (link)
			result = u"бла-бла-бла \n<A HREF=\"%s\">'''ля-ля-ля'''</A> бла-бла-бла\nбла-бла-бла" % (link)

			self.assertEqual (self.parser.toHtml (text), result)


	def testNoFormatLinks2 (self):
		for link in self.pagelinks:
			text = u"бла-бла-бла \n[[[='''ля-ля-ля'''=] -> %s]] бла-бла-бла\nбла-бла-бла" % (link)
			result = u"бла-бла-бла \n<A HREF=\"%s\">'''ля-ля-ля'''</A> бла-бла-бла\nбла-бла-бла" % (link)

			self.assertEqual (self.parser.toHtml (text), result)


	def testTexLinks1 (self):
		for link in self.pagelinks:
			text = u"бла-бла-бла \n[[%s | {$e^x$} ]] бла-бла-бла\nбла-бла-бла" % (link)
			result_begin = u'бла-бла-бла \n<A HREF="%s"><IMG SRC="__attach\__thumb\eqn_' % (link)

			self.assertTrue (self.parser.toHtml (text).startswith (result_begin) )


	def testTexLinks2 (self):
		for link in self.pagelinks:
			text = u"бла-бла-бла \n[[{$e^x$} -> %s]] бла-бла-бла\nбла-бла-бла" % (link)
			result_begin = u'бла-бла-бла \n<A HREF="%s"><IMG SRC="__attach\__thumb\eqn_' % (link)

			self.assertTrue (self.parser.toHtml (text).startswith (result_begin) )
	

	def testPageCommentsLinks1 (self):
		for n in range ( len (self.pagelinks)):
			link = self.pagelinks[n]
			comment = self.pageComments[n]

			text = u"бла-бла-бла \n[[%s | %s]] бла-бла-бла\nбла-бла-бла" % (link, comment)
			result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (link, comment)

			self.assertEqual (self.parser.toHtml (text), result)
	

	def testPageCommentsLinks2 (self):
		for n in range ( len (self.pagelinks)):
			link = self.pagelinks[n]
			comment = self.pageComments[n]

			text = u"бла-бла-бла \n[[%s -> %s]] бла-бла-бла\nбла-бла-бла" % (comment, link)
			result = u'бла-бла-бла \n<A HREF="%s">%s</A> бла-бла-бла\nбла-бла-бла' % (link, comment)

			self.assertEqual (self.parser.toHtml (text), result)
