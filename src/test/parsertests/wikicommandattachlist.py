#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import unittest

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment

from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.parser.commandattachlist import AttachListCommand
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.thumbnails import Thumbnails
from outwiker.pages.wiki.wikipage import WikiPageFactory

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



	def _attachFiles (self):
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


	def _compareResult (self, titles, names, result):
		attachdir = u"__attach"
		template = u'<A HREF="{path}">{title}</A>\n'

		result_right = u"".join ([template.format (path = os.path.join (attachdir, name).replace ("\\", "/"), title=title) 
			for (name, title) in zip (names, titles) ] ).rstrip()

		self.assertEqual (result_right, result)


	def testCommand1 (self):
		self._attachFiles ()
		cmd = AttachListCommand (self.parser)
		result = cmd.execute (u"", u"")

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)
	

	
	def testParse1 (self):
		self._attachFiles ()
		text = u"(:attachlist:)"
		result = self.parser.toHtml (text)

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)


	def testParse2 (self):
		self._attachFiles ()
		# Тест на то, что игнорируется директория __thumb
		thumb = Thumbnails (self.testPage)
		thumb.getThumbPath (True)

		text = u"(:attachlist:)"
		result = self.parser.toHtml (text)

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)


	def testCommandSortByName (self):
		self._attachFiles ()
		cmd = AttachListCommand (self.parser)
		result = cmd.execute (u"sort=name", u"")

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)


	def testParseSortByName (self):
		self._attachFiles ()
		text = u"(:attachlist sort=name:)"
		result = self.parser.toHtml (text)

		titles = [u"[dir]", u"[for_sort]", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"add.png", u"anchor.png", u"image.jpg", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)


	def testCommandSortDescendName (self):
		self._attachFiles ()
		cmd = AttachListCommand (self.parser)
		result = cmd.execute (u"sort=descendname", u"")

		titles = [u"[for_sort]", u"[dir]", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]
		names = [u"for_sort", u"dir", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]

		self._compareResult (titles, names, result)


	def testParseSortDescendName (self):
		self._attachFiles ()
		text = u"(:attachlist sort=descendname:)"
		result = self.parser.toHtml (text)

		titles = [u"[for_sort]", u"[dir]", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]
		names = [u"for_sort", u"dir", u"файл с пробелами.tmp", u"image.jpg", u"anchor.png", u"add.png"]

		self._compareResult (titles, names, result)


	def testParseSortByExt (self):
		self._attachFiles ()
		text = u"(:attachlist sort=ext:)"
		result = self.parser.toHtml (text)

		titles = [u"[dir]", u"[for_sort]", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]
		names = [u"dir", u"for_sort", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)


	def testParseSortDescendExt (self):
		self._attachFiles ()
		text = u"(:attachlist sort=descendext:)"
		result = self.parser.toHtml (text)

		titles = [u"[for_sort]", u"[dir]", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]
		names = [u"for_sort", u"dir", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]

		self._compareResult (titles, names, result)


	def testParseSortBySize (self):
		self._attachFiles ()
		text = u"(:attachlist sort=size:)"
		result = self.parser.toHtml (text)

		titles = [u"[dir]", u"[for_sort]", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]
		names = [u"dir", u"for_sort", u"файл с пробелами.tmp", u"anchor.png", u"add.png", u"image.jpg"]

		self._compareResult (titles, names, result)


	def testParseSortDescendSize (self):
		self._attachFiles ()
		text = u"(:attachlist sort=descendsize:)"
		result = self.parser.toHtml (text)

		titles = [u"[for_sort]", u"[dir]", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]
		names = [u"for_sort", u"dir", u"image.jpg", u"add.png", u"anchor.png", u"файл с пробелами.tmp"]

		self._compareResult (titles, names, result)


	def testParseSortByDate (self):
		files = [u"add.png", u"Anchor.png", 
				u"image2.png", u"image.png", 
				u"add.png2", u"файл с пробелами.tmp", 
				u"filename"]

		fullFilesPath = [os.path.join (u"../test/samplefiles/for_sort", fname) for fname in files]


		attach = Attachment (self.testPage)
		attach.attach (fullFilesPath)

		os.utime (attach.getFullPath (files[3]), (1000000000, 1000000000))
		os.utime (attach.getFullPath (files[0]), (1000000000, 1100000000))
		os.utime (attach.getFullPath (files[2]), (1000000000, 1200000000))
		os.utime (attach.getFullPath (files[6]), (1000000000, 1300000000))
		os.utime (attach.getFullPath (files[4]), (1000000000, 1400000000))
		os.utime (attach.getFullPath (files[5]), (1000000000, 1500000000))
		os.utime (attach.getFullPath (files[1]), (1000000000, 1600000000))

		text = u"(:attachlist sort=date:)"
		result = self.parser.toHtml (text)

		names = [files[3], files[0], files[2], files[6], files[4], files[5], files[1]]
		titles = names[:]

		self._compareResult (titles, names, result)


	def testParseSortDescendDate (self):
		files = [u"add.png", u"Anchor.png", 
				u"image2.png", u"image.png", 
				u"add.png2", u"файл с пробелами.tmp", 
				u"filename"]

		fullFilesPath = [os.path.join (u"../test/samplefiles/for_sort", fname) for fname in files]


		attach = Attachment (self.testPage)
		attach.attach (fullFilesPath)

		os.utime (attach.getFullPath (files[3]), (1000000000, 1000000000))
		os.utime (attach.getFullPath (files[0]), (1000000000, 1100000000))
		os.utime (attach.getFullPath (files[2]), (1000000000, 1200000000))
		os.utime (attach.getFullPath (files[6]), (1000000000, 1300000000))
		os.utime (attach.getFullPath (files[4]), (1000000000, 1400000000))
		os.utime (attach.getFullPath (files[5]), (1000000000, 1500000000))
		os.utime (attach.getFullPath (files[1]), (1000000000, 1600000000))

		text = u"(:attachlist sort=descenddate:)"
		result = self.parser.toHtml (text)

		names = [files[1], files[5], files[4], files[6], files[2], files[0], files[3]]
		titles = names[:]

		self._compareResult (titles, names, result)

