#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import unittest

from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory, TextWikiPage
from core.attachment import Attachment
from core.application import Application
from test.utils import removeWiki

from gui.htmlcontrollerie import UriIdentifier
from gui.htmlcontrollerwebkit import UriIdentifierWebKit


class UriIdentifierTest (unittest.TestCase):
	"""
	Базовый класс для тестов идентификации сслок разными HTML-движками
	"""
	def setUp(self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		# - Страница 1
		#   - # Страница 5
		# - Страница 2
		#   - Страница 3
		#     - # Страница 4
		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"# Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"# Страница 5", [])

		filesPath = u"../test/samplefiles/"
		self.files = [u"accept.png", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir"]
		self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]

		Attachment (self.rootwiki[u"Страница 1"]).attach (self.fullFilesPath)
		Attachment (self.rootwiki[u"Страница 1/# Страница 5"]).attach (self.fullFilesPath)

		Application.wikiroot = None


	def tearDown(self):
		Application.wikiroot = None
		removeWiki (self.path)



class UriIdentifierIETest (UriIdentifierTest):
	"""
	Тесты идентификации ссылок для IE
	"""
	def testFindUriHttp (self):
		"""
		Тест на распознавание адресов, начинающихся с http
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"http://jenyay.net")

		self.assertEqual (url, u"http://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFindUriHttps (self):
		"""
		Тест на распознавание адресов, начинающихся с https
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"https://jenyay.net")

		self.assertEqual (url, u"https://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFindUriFtp (self):
		"""
		Тест на распознавание адресов, начинающихся с ftp
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"ftp://jenyay.net")

		self.assertEqual (url, u"ftp://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFindUriMailto (self):
		"""
		Тест на распознавание адресов, начинающихся с mailto
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"mailto://jenyay.net")

		self.assertEqual (url, u"mailto://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFullPageLink1 (self):
		"""
		Тест на распознавание ссылок на страницы по полному пути в вики
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"/Страница 1/Страница 2/Страница 3")

		self.assertEqual (url, None)
		self.assertEqual (page, self.rootwiki[u"/Страница 1/Страница 2/Страница 3"])
		self.assertEqual (filename, None)


	def testFullPageLink2 (self):
		"""
		Тест на распознавание ссылок на страницы, когда движок IE считает, что это ссылка на файл
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"x:\\Страница 1\\Страница 2\\Страница 3")

		self.assertEqual (url, None)
		self.assertEqual (page, self.rootwiki[u"/Страница 1/Страница 2/Страница 3"])
		self.assertEqual (filename, None)


	def testFullPageLink3 (self):
		"""
		Тест на распознавание ссылок на страницы, когда движок IE считает, что это ссылка на файл. 
		В пути есть символ "#"
		"""
		identifier = UriIdentifier (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"x:\\Страница 1\\Страница 2\\Страница 3\\# Страница 4")

		self.assertEqual (url, None)
		self.assertEqual (page, self.rootwiki[u"/Страница 1/Страница 2/Страница 3/# Страница 4"])
		self.assertEqual (filename, None)


	def testSubpath1 (self):
		"""
		Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на файл. 
		"""
		wikipage = self.rootwiki[u"Страница 1"]
		path = os.path.join (wikipage.path, u"Страница 2").replace ("/", "\\")

		identifier = UriIdentifier (wikipage)

		(url, page, filename) = identifier.identify (path)

		self.assertEqual (url, None)
		self.assertEqual (page, wikipage[u"Страница 2"])
		self.assertEqual (filename, None)


	def testAttachment1 (self):
		"""
		Тест на распознавание ссылок на вложенные файлы
		"""
		wikipage = self.rootwiki[u"Страница 1"]
		path = os.path.join (Attachment (wikipage).getAttachPath (), u"accept.png")

		identifier = UriIdentifier (wikipage)

		(url, page, filename) = identifier.identify (path)

		self.assertEqual (url, None)
		self.assertEqual (page, None)
		self.assertEqual (filename, path)


class UriIdentifierWebKitTest (UriIdentifierTest):
	"""
	Тесты идентификации ссылок для WebKit
	"""
	def testFindUriHttp (self):
		"""
		Тест на распознавание адресов, начинающихся с http
		"""
		identifier = UriIdentifierWebKit (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"http://jenyay.net")

		self.assertEqual (url, u"http://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFindUriHttps (self):
		"""
		Тест на распознавание адресов, начинающихся с https
		"""
		identifier = UriIdentifierWebKit (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"https://jenyay.net")

		self.assertEqual (url, u"https://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFindUriFtp (self):
		"""
		Тест на распознавание адресов, начинающихся с ftp
		"""
		identifier = UriIdentifierWebKit (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"ftp://jenyay.net")

		self.assertEqual (url, u"ftp://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFindUriMailto (self):
		"""
		Тест на распознавание адресов, начинающихся с mailto
		"""
		identifier = UriIdentifierWebKit (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"mailto://jenyay.net")

		self.assertEqual (url, u"mailto://jenyay.net")
		self.assertEqual (page, None)
		self.assertEqual (filename, None)


	def testFullPageLink1 (self):
		"""
		Тест на распознавание ссылок на страницы по полному пути в вики
		"""
		identifier = UriIdentifierWebKit (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"/Страница 1/Страница 2/Страница 3")

		self.assertEqual (url, None)
		self.assertEqual (page, self.rootwiki[u"/Страница 1/Страница 2/Страница 3"])
		self.assertEqual (filename, None)


	def testFullPageLink2 (self):
		"""
		Тест на распознавание ссылок на страницы по полному пути в вики
		"""
		identifier = UriIdentifierWebKit (self.rootwiki[u"Страница 1"])
		(url, page, filename) = identifier.identify (u"file:///Страница 2/Страница 3/Страница 4")

		self.assertEqual (url, None)
		self.assertEqual (page, self.rootwiki[u"/Страница 2/Страница 3/Страница 4"])
		self.assertEqual (filename, None)


	def testRelativePageLink1 (self):
		"""
		При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
		"""
		currentpage = self.rootwiki[u"Страница 1"]
		identifier = UriIdentifierWebKit (currentpage)
		link = u"file://{0}".format (os.path.join (currentpage.path, u"Страница 5") )

		(url, page, filename) = identifier.identify (link)

		self.assertEqual (url, None)
		self.assertEqual (page, currentpage[u"Страница 5"])
		self.assertEqual (page, self.rootwiki[u"/Страница 1/Страница 5"])
		self.assertEqual (filename, None)


	def testRelativePageLink2 (self):
		"""
		При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
		"""
		currentpage = self.rootwiki[u"Страница 1"]
		identifier = UriIdentifierWebKit (currentpage)
		link = u"file://{0}".format (os.path.join (currentpage.path, 
			u"Страница 2", u"Страница 3", u"Страница 4") )

		(url, page, filename) = identifier.identify (link)

		self.assertEqual (url, None)
		self.assertEqual (page, self.rootwiki[u"/Страница 2/Страница 3/Страница 4"])
		self.assertEqual (filename, None)


	def testAttachment1 (self):
		"""
		Тест на распознавание ссылок на вложенные файлы
		"""
		wikipage = self.rootwiki[u"Страница 1"]

		path = os.path.join (Attachment (wikipage).getAttachPath (), 
				u"accept.png")

		href = "".join ([u"file://", path] )

		identifier = UriIdentifierWebKit (wikipage)

		(url, page, filename) = identifier.identify (href)

		self.assertEqual (url, None)
		self.assertEqual (page, None)
		self.assertEqual (filename, path)
