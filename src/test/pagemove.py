#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты на перемещение заметок по дереву
"""

import os.path
import shutil
import unittest

import core.exceptions
from core.application import Application
from core.tree import RootWikiPage, WikiDocument
from core.attachment import Attachment

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
	

	def tearDown(self):
		removeWiki (self.path)

	
	def onTreeUpdate (self, sender):
		self.treeUpdateCount += 1
		self.treeUpdateSender = sender

	
	def test1 (self):
		self.treeUpdateCount = 0
		Application.onTreeUpdate += self.onTreeUpdate

		self.wiki[u"Страница 1/Страница 5"].moveTo (self.wiki)

		self.assertEqual (self.treeUpdateCount, 1)

		self.assertEqual (len (self.wiki[u"Страница 1"]), 0)
		self.assertEqual (len (self.wiki), 4)
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
		self.assertEqual (len (self.wiki), 2)
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].title, u"Страница 1")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].title, u"Страница 5")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].subpath, u"Страница 2/Страница 3/Страница 1")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].subpath, u"Страница 2/Страница 3/Страница 1/Страница 5")

	
	def test3 (self):
		self.assertRaises (core.exceptions.DublicateTitle, self.wiki[u"Страница 2/Страница 3/Страница 4"].moveTo, self.wiki)


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
			except core.exceptions.TreeException:
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
				self.assertEqual (len (self.wiki), 2)
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].title, u"Страница 1")
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].title, u"Страница 5")
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].subpath, u"Страница 2/Страница 3/Страница 1")
				self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].subpath, u"Страница 2/Страница 3/Страница 1/Страница 5")

