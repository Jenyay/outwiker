#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import unittest

from pages.wiki.wikithumbmaker import WikiThumbmaker
from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from test.utils import removeWiki, getImageSize


class WikiThumbmakerTest (unittest.TestCase):
	def setUp (self):
		self.thumbmaker = WikiThumbmaker()

		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])
	

	def tearDown(self):
		removeWiki (self.path)
	

	def testThumbDir (self):
		page = self.rootwiki[u"Страница 1"]

		self.assertEqual (self.thumbmaker.getThumbPath (page), os.path.join (page.getAttachPath(), self.thumbmaker.thumbsDir) )
	

	def testThumbByWidthJpeg (self):
		images_dir = "../test/images"

		fname_in = "first.jpg"
		page = self.rootwiki[u"Страница 1"]

		page.attach ([os.path.join (images_dir, fname_in) ] )

		newwidth = 250
		newheight = 182

		thumb_fname = self.thumbmaker.createThumbByWidth (page, fname_in, newwidth)
		thumb_path = os.path.join (page.path, thumb_fname)

		(width, height) = getImageSize (thumb_path)
		
		self.assertTrue (os.path.exists (thumb_path), thumb_path)
		self.assertEqual (width, newwidth)
		self.assertEqual (height, newheight)
	

	def testThumbByWidthPng (self):
		images_dir = "../test/images"

		fname_in = "outwiker_1.1.0_02.png"
		page = self.rootwiki[u"Страница 1"]

		page.attach ([os.path.join (images_dir, fname_in) ] )

		newwidth = 250
		newheight = 215

		thumb_fname = self.thumbmaker.createThumbByWidth (page, fname_in, newwidth)
		thumb_path = os.path.join (page.path, thumb_fname)

		(width, height) = getImageSize (thumb_path)
		
		self.assertTrue (os.path.exists (thumb_path), thumb_path)
		self.assertEqual (width, newwidth)
		self.assertEqual (height, newheight)
