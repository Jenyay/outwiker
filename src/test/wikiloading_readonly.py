#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument
from core.exceptions import ReadonlyException
from pages.text.textpage import TextPageFactory
from core.event import Event
from core.controller import Controller
from core.factory import FactorySelector
from test.utils import removeWiki
from test.utils import removeWiki

from test.utils import removeWiki

class ReadonlyLoadTest (unittest.TestCase):
	"""
	Тест на открытие вики
	"""
	def setUp(self):
		self.path = u"../test/samplewiki"
		self.root = WikiDocument.load (self.path, readonly=True)
		#print self.root


	def testLoadWiki(self):
		self.assertEqual ( len (self.root), 4, "Pages count == 4")


	def testPagesAccess (self):
		"""
		Проверка доступа к отдельным страницам и правильности установки заголовков
		"""
		self.assertEqual (self.root[u"page 4"].title, u"page 4")
		self.assertEqual (self.root[u"Страница 1"].title, u"Страница 1")
		self.assertEqual (self.root[u"стрАниЦа 3"].title, u"Страница 3")
		self.assertEqual (self.root[u"Страница 1/Страница 2"].title, u"Страница 2")
		self.assertEqual (self.root[u"СтраНица 1/стРаниЦА 2/СтраНицА 5"].title, u"Страница 5")
		self.assertEqual (self.root[u"Страница 1"][u"Страница 2"].title, u"Страница 2")

		self.assertEqual (self.root[u"Страница 111"], None)


	def testPagesParent (self):
		"""
		Проверка доступа к отдельным страницам и правильности установки заголовков
		"""
		self.assertEqual (self.root[u"page 4"].parent, self.root)
		self.assertEqual (self.root[u"Страница 1"].parent, self.root)
		self.assertEqual (self.root[u"Страница 1/Страница 2"].parent, self.root[u"Страница 1"])
		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].parent, self.root[u"Страница 1/Страница 2"])

		self.assertEqual (self.root.parent, None)


	def testPagesPath (self):
		"""
		Проверка правильности путей до страниц
		"""
		self.assertEqual (self.root[u"page 4"].path, os.path.join (self.path, u"page 4") )
		self.assertEqual (self.root[u"Страница 1"].path, os.path.join (self.path, u"Страница 1") )
		self.assertEqual (self.root[u"Страница 3"].path, os.path.join (self.path, u"Страница 3") )

		fullpath = os.path.join (self.path, u"Страница 1")
		fullpath = os.path.join (fullpath, u"Страница 2")

		self.assertEqual (self.root[u"Страница 1/Страница 2"].path, fullpath)



	def testTags (self):
		self.assertTrue (u"Тест" in self.root[u"Страница 1"].tags)
		self.assertTrue (u"test" in self.root[u"Страница 1"].tags, self.root[u"Страница 1"].tags)
		self.assertTrue (u"двойной тег" in self.root[u"Страница 1"].tags)
		self.assertEqual (len (self.root[u"Страница 1"].tags), 3)

		self.assertTrue (u"test" in self.root[u"Страница 1/Страница 2"].tags)
		self.assertEqual (len (self.root[u"Страница 1/Страница 2"].tags), 1)

		self.assertTrue (u"test" in self.root[u"Страница 3"].tags)
		self.assertTrue (u"тест" in self.root[u"Страница 3"].tags)
		self.assertEqual (len (self.root[u"Страница 3"].tags), 2)

		self.assertEqual (len (self.root[u"page 4"].tags), 0)


	def testTypes (self):
		self.assertEqual (self.root[u"Страница 1"].type, "html")
		self.assertEqual (self.root[u"Страница 1/Страница 2"].type, "text")
		self.assertEqual (self.root[u"Страница 3"].type, "html")
		self.assertEqual (self.root[u"page 4"].type, "text")
		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].type, "text")


	def testChildren (self):
		self.assertEqual (len (self.root[u"Страница 1"].children), 1)
		self.assertEqual (self.root[u"Страница 1"].children[0], self.root[u"Страница 1/Страница 2"])

		self.assertEqual (len (self.root[u"Страница 1/Страница 2"].children), 1)
		self.assertEqual (len (self.root[u"Страница 3"].children), 0)
		self.assertEqual (len (self.root[u"page 4"].children), 0)


	def testIcons (self):
		self.assertEqual (os.path.basename (self.root[u"Страница 1"].icon), "__icon.png")
		self.assertEqual (os.path.basename (self.root[u"Страница 1/Страница 2"].icon), "__icon.gif")
		self.assertEqual (self.root[u"Страница 3"].icon, None)


	def testParams (self):
		self.assertEqual (self.root[u"Страница 1"].getParameter (u"General", u"type"), u"html")
		self.assertEqual (self.root[u"Страница 1"].getParameter (u"General", u"tags"), u"Тест, test, двойной тег")
		

	def testGetRoot (self):
		self.assertEqual (self.root[u"Страница 1"].root, self.root)
		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].root, self.root)
	

	def testSubpath (self):
		self.assertEqual (self.root[u"Страница 1"].subpath, u"Страница 1")

		self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].subpath, 
				u"Страница 1/Страница 2/Страница 5")
	

class ReadonlyChangeTest (unittest.TestCase):
	"""
	Тест для проверки перемещения заметок по дереву
	"""
	def setUp (self):
		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		wiki = WikiDocument.create (self.path)

		TextPageFactory.create (wiki, u"Страница 1", [])
		TextPageFactory.create (wiki, u"Страница 2", [])
		TextPageFactory.create (wiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (wiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (wiki[u"Страница 1"], u"Страница 5", [])
		TextPageFactory.create (wiki, u"страница 4", [])

		filesPath = u"../test/samplefiles/"
		files = [u"accept.png", u"add.png", u"anchor.png"]

		fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

		wiki[u"Страница 4"].attach (fullFilesPath)
		wiki[u"Страница 1/Страница 5"].attach (fullFilesPath)

		self.wiki = WikiDocument.load (self.path, readonly=True)
	

	def tearDown(self):
		removeWiki (self.path)

	
	def testMoveTo (self):
		try:
			self.wiki[u"Страница 1/Страница 5"].moveTo (self.wiki)
		except ReadonlyException:
			pass
		else:
			self.fail()

	
	def testChangeTitle1 (self):
		try:
			self.wiki[u"Страница 1"].title = u"Страница 666"
		except ReadonlyException:
			pass
		else:
			self.fail()


	def testChangeTitle2 (self):
		try:
			self.wiki[u"Страница 2/Страница 3"].title = u"Страница 666"
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testChangeTags1 (self):
		try:
			self.wiki[u"Страница 1"].tags = ["111", "222"]
		except ReadonlyException:
			pass
		else:
			self.fail()


	def testChangeTags2 (self):
		try:
			self.wiki[u"Страница 2/Страница 3"].tags = ["111", "222"]
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testSetParameter1 (self):
		self.wiki[u"Страница 1"].setParameter ("section", "param", "value")


	def testSetParameter2 (self):
		self.wiki[u"Страница 2/Страница 3"].setParameter ("section", "param", "value")

	
	def testChangeIcon1 (self):
		try:
			self.wiki[u"Страница 1"].icon = "../test/images/feed.gif"
		except ReadonlyException:
			pass
		else:
			self.fail()


	def testChangeIcon2 (self):
		try:
			self.wiki[u"Страница 2/Страница 3"].icon = "../test/images/feed.gif"
		except ReadonlyException:
			pass
		else:
			self.fail()


	def testAttach1 (self):
		try:
			filesPath = u"../test/samplefiles/"
			files = [u"accept.png", u"add.png", u"anchor.png"]

			fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

			self.wiki[u"Страница 1"].attach (fullFilesPath)
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testAttach2 (self):
		try:
			filesPath = u"../test/samplefiles/"
			files = [u"accept.png", u"add.png", u"anchor.png"]

			fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

			self.wiki[u"Страница 2/Страница 3"].attach (fullFilesPath)
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testRemoveAttach1 (self):
		try:
			self.wiki[u"Страница 4"].removeAttach (u"add.png")
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testRemoveAttach2 (self):
		try:
			self.wiki[u"Страница 1/Страница 5"].removeAttach (u"anchor.png")
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testCreate1 (self):
		try:
			TextPageFactory.create (self.wiki[u"Страница 1"], u"Страница 666", [])
		except ReadonlyException:
			pass
		else:
			self.fail()


	def testCreate1 (self):
		try:
			TextPageFactory.create (self.wiki[u"Страница 2/Страница 3"], u"Страница 666", [])
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testChangeContent1 (self):
		try:
			self.wiki[u"Страница 1"].content = u"бла-бла-бла"
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testChangeContent2 (self):
		try:
			self.wiki[u"Страница 2/Страница 3"].content = u"бла-бла-бла"
		except ReadonlyException:
			pass
		else:
			self.fail()
	

	def testSelectedPage1 (self):
		self.wiki.root.selectedPage = self.wiki[u"Страница 1"]

	
	def testSelectedPage2 (self):
		self.wiki.root.selectedPage = self.wiki[u"Страница 2/Страница 3"]

	
	def testRemove1 (self):
		try:
			self.wiki[u"Страница 1"].remove()
		except ReadonlyException:
			pass
		else:
			self.fail()

		self.assertTrue (self.wiki[u"Страница 1"] != None)


	def testRemove2 (self):
		try:
			self.wiki[u"Страница 2/Страница 3"].remove()
		except ReadonlyException:
			pass
		else:
			self.fail()

		self.assertTrue (self.wiki[u"Страница 2/Страница 3"] != None)
