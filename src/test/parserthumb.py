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


class ParserThumbTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.filesPath = u"../test/samplefiles/"

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


	def testThumbWidthJpg (self):
		text = u'бла-бла-бла \nкхм % width = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_width_100_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbWidthJpg2 (self):
		text = u'бла-бла-бла \nкхм % thumb width = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_width_100_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbWidthJpeg (self):
		text = u'бла-бла-бла \nкхм % width = 100 px % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_width_100_image.jpeg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpeg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.jpeg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))

	
	def testThumbWidthGif (self):
		text = u'бла-бла-бла \nкхм % width = 100 px % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_width_100_image.png")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.gif"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbWidthPng (self):
		text = u'бла-бла-бла \nкхм % width = 100 px % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_width_100_image.png")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.png"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbHeightJpg (self):
		text = u'бла-бла-бла \nкхм % height = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_height_100_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))

	
	def testThumbHeightJpg2 (self):
		text = u'бла-бла-бла \nкхм % thumb height = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_height_100_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format(path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))


	def testThumbHeightJpeg (self):
		text = u'бла-бла-бла \nкхм % height = 100 px % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_height_100_image.jpeg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpeg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.jpeg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))

	
	def testThumbHeightGif (self):
		text = u'бла-бла-бла \nкхм % height = 100 px % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_height_100_image.png")
		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.gif"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbHeightPng (self):
		text = u'бла-бла-бла \nкхм % height = 100 px % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_height_100_image.png")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.png"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbJpg (self):
		text = u'бла-бла-бла \nкхм % thumb % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))

	
	def testThumbJpeg (self):
		text = u'бла-бла-бла \nкхм % thumb % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.jpeg")
		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpeg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.jpeg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))


	def testThumbPng (self):
		text = u'бла-бла-бла \nкхм % thumb % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.png")
		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.png"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))

	
	def testThumbGif (self):
		text = u'бла-бла-бла \nкхм % thumb % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.png")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.gif"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path = path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
	

	def testThumbMaxSizeJpg (self):
		text = u'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))


	def testThumbMaxSizeJpg2 (self):
		text = u'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.jpg")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.jpg"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.jpg")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))

	
	def testThumbMaxSizePng (self):
		text = u'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.png")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.png"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))


	def testThumbMaxSizeGif (self):
		text = u'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
		path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.png")

		result = u'бла-бла-бла \nкхм <A HREF="__attach/image.gif"><IMG SRC="{path}"></A> бла-бла-бла\nбла-бла-бла'.format (path=path)

		self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

		path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.png")
		self.assertTrue (os.path.exists (path), path.encode (self.encoding))
