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
from pages.wiki.thumbnails import Thumbnails
from pages.wiki.texrender import getTexRender
from pages.wiki.parserfactory import ParserFactory


class ParserTexTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.filesPath = u"../test/samplefiles/"

		self.url1 = u"http://example.com"
		self.url2 = u"http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"

		self.__createWiki()
		
		factory = ParserFactory()
		self.testPage = self.rootwiki[u"Страница 2"]
		self.parser = factory.make (self.testPage, Application.config)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)
		WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
		

	def tearDown(self):
		removeWiki (self.path)
	

	def testTex1 (self):
		thumb = Thumbnails (self.parser.page)
		texrender = getTexRender(thumb.getThumbPath (True))

		eqn = u"y = f(x)"
		text = u"{$ %s $}" % (eqn)

		fname = texrender.getImageName (eqn)
		path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

		result_right = u'<IMG SRC="{0}">'.format (path)

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result, result)

		full_path = os.path.join (self.parser.page.path, path)
		self.assertTrue (os.path.exists (full_path), full_path )


	def testTex2 (self):
		thumb = Thumbnails (self.parser.page)
		texrender = getTexRender(thumb.getThumbPath (True))

		eqn1 = u"y = f(x)"
		eqn2 = u"y = e^x"
		eqn3 = u"y = \sum_{i=0}\pi"

		text = u"""бла-бла-бла
* бла-бла-бла {$ %s $} 1111
* бла-бла-бла {$ %s $} 222
* бла-бла-бла {$ %s $} 333""" % (eqn1, eqn2, eqn3)

		fname1 = texrender.getImageName (eqn1)
		fname2 = texrender.getImageName (eqn2)
		fname3 = texrender.getImageName (eqn3)

		path1 = os.path.join (Thumbnails.getRelativeThumbDir(), fname1)
		path2 = os.path.join (Thumbnails.getRelativeThumbDir(), fname2)
		path3 = os.path.join (Thumbnails.getRelativeThumbDir(), fname3)

		result_right = u'''бла-бла-бла
<UL><LI>бла-бла-бла <IMG SRC="{path1}"> 1111</LI><LI>бла-бла-бла <IMG SRC="{path2}"> 222</LI><LI>бла-бла-бла <IMG SRC="{path3}"> 333</LI></UL>'''.format (**locals())


		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result, result)

		full_path1 = os.path.join (self.parser.page.path, path1)
		full_path2 = os.path.join (self.parser.page.path, path2)
		full_path3 = os.path.join (self.parser.page.path, path3)

		self.assertTrue (os.path.exists (full_path1), full_path1)
		self.assertTrue (os.path.exists (full_path2), full_path2)
		self.assertTrue (os.path.exists (full_path3), full_path3)


	def testTex3 (self):
		thumb = Thumbnails (self.parser.page)
		texrender = getTexRender(thumb.getThumbPath (True))

		eqn = u"y = f(x)"
		text = u"[[{$ %s $} -> http://jenyay.net]]" % (eqn)

		fname = texrender.getImageName (eqn)
		path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

		result_right = u'<A HREF="http://jenyay.net"><IMG SRC="{0}"></A>'.format (path)

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result, result)

		full_path = os.path.join (self.parser.page.path, path)
		self.assertTrue (os.path.exists (full_path), full_path )


	def testTex4 (self):
		thumb = Thumbnails (self.parser.page)
		texrender = getTexRender(thumb.getThumbPath (True))

		eqn = u"y = f(x)"
		text = u"[[http://jenyay.net | {$ %s $}]]" % (eqn)

		fname = texrender.getImageName (eqn)
		path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

		result_right = u'<A HREF="http://jenyay.net"><IMG SRC="{0}"></A>'.format (path)

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result, result)

		full_path = os.path.join (self.parser.page.path, path)
		self.assertTrue (os.path.exists (full_path), full_path )


	def testTexRussian (self):
		thumb = Thumbnails (self.parser.page)
		texrender = getTexRender(thumb.getThumbPath (True))

		eqn = u"y = бла-бла-бла"
		text = u"{$ %s $}" % (eqn)

		fname = texrender.getImageName (eqn)
		path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

		result_right = u'<IMG SRC="{0}">'.format (path)

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result, result)

		full_path = os.path.join (self.parser.page.path, path)
		self.assertTrue (os.path.exists (full_path), full_path )



	
