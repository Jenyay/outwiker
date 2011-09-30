#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты на перемещение заметок по дереву
"""

import os.path
import shutil
import unittest

from outwiker.core.exceptions import DublicateTitle, TreeException
from outwiker.core.application import Application
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.attachment import Attachment

from pages.text.textpage import TextPageFactory
from test.utils import removeWiki


class MoveTest (unittest.TestCase):
	"""
	Тест для проверки перемещения заметок по дереву
	"""
	def setUp (self):
		# Количество срабатываний особытий при обновлении страницы
		self.treeUpdateCount = 0
		self.treeUpdateSender = None

		# Здесь будет создаваться вики
		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.wiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.wiki, u"Страница 1", [])
		TextPageFactory.create (self.wiki, u"Страница 2", [])
		TextPageFactory.create (self.wiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.wiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.wiki[u"Страница 1"], u"Страница 5", [])
		TextPageFactory.create (self.wiki, u"страница 4", [])
		TextPageFactory.create (self.wiki, u"страница 444", [])

		Application.wikiroot = None
	

	def tearDown(self):
		removeWiki (self.path)
		Application.wikiroot = None

	
	def onTreeUpdate (self, sender):
		self.treeUpdateCount += 1
		self.treeUpdateSender = sender

	
	def test1 (self):
		self.treeUpdateCount = 0
		Application.wikiroot = self.wiki

		Application.onTreeUpdate += self.onTreeUpdate

		self.wiki[u"Страница 1/Страница 5"].moveTo (self.wiki)

		self.assertEqual (self.treeUpdateCount, 1)

		self.assertEqual (len (self.wiki[u"Страница 1"]), 0)
		self.assertEqual (len (self.wiki), 5)
		self.assertEqual (self.wiki[u"Страница 5"].title, u"Страница 5")
		self.assertEqual (self.wiki[u"Страница 5"].parent, self.wiki)
		self.assertEqual (self.wiki[u"Страница 5"].parent, self.wiki)
		self.assertEqual (self.wiki[u"Страница 5"].subpath, u"Страница 5")

		Application.onTreeUpdate += self.onTreeUpdate


	def testNoEvent (self):
		self.treeUpdateCount = 0
		Application.wikiroot = None

		Application.onTreeUpdate += self.onTreeUpdate

		self.wiki[u"Страница 1/Страница 5"].moveTo (self.wiki)

		self.assertEqual (self.treeUpdateCount, 0)

		self.assertEqual (len (self.wiki[u"Страница 1"]), 0)
		self.assertEqual (len (self.wiki), 5)
		self.assertEqual (self.wiki[u"Страница 5"].title, u"Страница 5")
		self.assertEqual (self.wiki[u"Страница 5"].parent, self.wiki)
		self.assertEqual (self.wiki[u"Страница 5"].parent, self.wiki)
		self.assertEqual (self.wiki[u"Страница 5"].subpath, u"Страница 5")

		Application.onTreeUpdate += self.onTreeUpdate


	def test2 (self):
		self.wiki[u"Страница 1"].moveTo (self.wiki[u"Страница 2/Страница 3"])

		self.assertEqual (self.wiki[u"Страница 1"], None )
		self.assertTrue (os.path.exists (os.path.join (self.wiki[u"Страница 2/Страница 3"].path, u"Страница 1") ) )

		self.assertEqual (len (self.wiki[u"Страница 2/Страница 3"]), 2)
		self.assertEqual (len (self.wiki), 3)
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].title, u"Страница 1")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].title, u"Страница 5")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].subpath, u"Страница 2/Страница 3/Страница 1")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].subpath, u"Страница 2/Страница 3/Страница 1/Страница 5")

	
	def test3 (self):
		self.assertRaises (DublicateTitle, 
				self.wiki[u"Страница 2/Страница 3/Страница 4"].moveTo, 
				self.wiki)


	def test4 (self):
		self.wiki[u"страница 4"].moveTo (self.wiki[u"страница 444"])

		self.assertEqual (self.wiki[u"страница 4"], None )
		self.assertTrue (os.path.exists (os.path.join (self.wiki[u"страница 444"].path, u"страница 4") ) )
		self.assertEqual (len (self.wiki[u"страница 444"]), 1)
		self.assertEqual (self.wiki[u"страница 444/страница 4"].title, u"страница 4")


	def testMoveToSelf (self):
		self.assertRaises (TreeException, 
				self.wiki[u"Страница 1"].moveTo, 
				self.wiki[u"Страница 1"])

		self.assertNotEqual (self.wiki[u"Страница 1"], None)
		self.assertEqual (len (self.wiki), 4)


	def testMoveToChild1 (self):
		#self.wiki[u"Страница 2"].moveTo (self.wiki[u"Страница 2/Страница 3"])
		self.assertRaises (TreeException, 
				self.wiki[u"Страница 2"].moveTo, 
				self.wiki[u"Страница 2/Страница 3"])

		self.assertNotEqual (self.wiki[u"Страница 2"], None)
		self.assertEqual (len (self.wiki), 4)


	def testMoveToChild2 (self):
		#self.wiki[u"Страница 2"].moveTo (self.wiki[u"Страница 2/Страница 3/Страница 4"])
		self.assertRaises (TreeException, 
				self.wiki[u"Страница 2"].moveTo, 
				self.wiki[u"Страница 2/Страница 3/Страница 4"])

		self.assertNotEqual (self.wiki[u"Страница 2"], None)
		self.assertEqual (len (self.wiki), 4)


	def testMoveInvalid (self):
		"""
		А что, если кто-то блокирует папку с заметкой?
		"""
		page = self.wiki[u"Страница 1"]
		attachname = u"add.png"

		attach = Attachment (page)
		attach.attach ([os.path.join (u"../test/samplefiles", attachname)])

		# Откроем на запись файл в папке с вложениями, чтобы нельзя было переместить папку
		with open (attach.getFullPath (u"lock.tmp", True), "w"):
			try:
				page.moveTo (self.wiki[u"Страница 2/Страница 3"])
			except TreeException:
				# Если не удалось переместить страницу
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"], None)
				self.assertNotEqual (self.wiki[u"Страница 1"], None)
				self.assertEqual (len (self.wiki[u"Страница 2/Страница 3"]), 1)

				self.assertTrue (os.path.exists (page.path))
				self.assertFalse (os.path.exists (os.path.join (self.wiki[u"Страница 2/Страница 3"].path, u"Страница 1") ) )

				self.assertTrue (os.path.exists (attach.getFullPath (attachname) ) )
			else:
				# А если страницу переместить удалось, то проверим, что она действительно перенеслась
				self.assertEqual (self.wiki[u"Страница 1"], None )
				self.assertTrue (os.path.exists (os.path.join (self.wiki[u"Страница 2/Страница 3"].path, u"Страница 1") ) )

				self.assertEqual (len (self.wiki[u"Страница 2/Страница 3"]), 2)
				self.assertEqual (len (self.wiki), 3)
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].title, u"Страница 1")
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].title, u"Страница 5")
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].subpath, u"Страница 2/Страница 3/Страница 1")
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].subpath, u"Страница 2/Страница 3/Страница 1/Страница 5")

