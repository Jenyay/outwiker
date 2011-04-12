#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import unittest

from core.tree import WikiDocument
from core.application import Application
from core.attachment import Attachment

from pages.wiki.parser.wikiparser import Parser
from pages.wiki.parser.commandattachlist import AttachListCommand
from pages.wiki.parserfactory import ParserFactory
from pages.wiki.thumbnails import Thumbnails
from pages.wiki.wikipage import WikiPageFactory

from test.utils import removeWiki



class WikiAttachListCommandTest (unittest.TestCase):
	def setUp(self):
		self.encoding = "utf8"

		self.__createWiki()
		self.testPage = self.rootwiki[u"Страница 1"]
		
		factory = ParserFactory()
		self.parser = factory.make (self.testPage, Application.config)

		filesPath = u"../test/samplefiles/"
		self.files = [u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir", u"for_sort"]
		self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]

		attach = Attachment (self.testPage)
		attach.attach (self.fullFilesPath)
	

	def __createWiki (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)
		WikiPageFactory.create (self.rootwiki, u"Страница 1", [])


	def tearDown(self):
		removeWiki (self.path)


	def testCommand1 (self):
		cmd = AttachListCommand (self.parser)
		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = cmd.execute (u"", u"")

		self.assertEqual (result_right, result)

	
	def testParse1 (self):
		text = u"(:attachlist:)"

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testParse2 (self):
		# Тест на то, что игнорируется директория __thumb
		thumb = Thumbnails (self.testPage)
		thumb.getThumbPath (True)

		text = u"(:attachlist:)"

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testCommandSortByName (self):
		cmd = AttachListCommand (self.parser)
		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = cmd.execute (u"sort=name", u"")

		self.assertEqual (result_right, result)


	def testParseSortByName (self):
		text = u"(:attachlist sort=name:)"

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testCommandSortDescendName (self):
		cmd = AttachListCommand (self.parser)
		titles = [u"[for_sort]", u"[dir]", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]
		names = [u"for_sort", u"dir", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = cmd.execute (u"sort=descendname", u"")

		self.assertEqual (result_right, result)


	def testParseSortDescendName (self):
		text = u"(:attachlist sort=descendname:)"

		titles = [u"[for_sort]", u"[dir]", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]
		names = [u"for_sort", u"dir", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testParseSortByExt (self):
		text = u"(:attachlist sort=ext:)"

		titles = [u"[dir]", u"[for_sort]", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testParseSortDescendExt (self):
		text = u"(:attachlist sort=descendext:)"

		titles = [u"[for_sort]", u"[dir]", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]
		names = [u"for_sort", u"dir", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testParseSortBySize (self):
		text = u"(:attachlist sort=size:)"

		titles = [u"[dir]", u"[for_sort]", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]
		names = [u"dir", u"for_sort", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	def testParseSortDescendSize (self):
		text = u"(:attachlist sort=descendsize:)"

		titles = [u"[for_sort]", u"[dir]", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]
		names = [u"for_sort", u"dir", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]

		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		result = self.parser.toHtml (text)

		self.assertEqual (result_right, result)


	
