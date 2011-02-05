#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Тесты на перемещение заметок по дереву
"""

import os.path
import shutil
import unittest

from core.tree import RootWikiPage, WikiDocument
from pages.text.textpage import TextPageFactory
from core.event import Event
from test.utils import removeWiki
from core.application import Application
import core.exceptions


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

		self.assertEqual (len (self.wiki[u"Страница 2/Страница 3"]), 2)
		self.assertEqual (len (self.wiki), 2)
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].title, u"Страница 1")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].title, u"Страница 5")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1"].subpath, u"Страница 2/Страница 3/Страница 1")
		self.assertEqual (self.wiki[u"Страница 2/Страница 3/Страница 1/Страница 5"].subpath, u"Страница 2/Страница 3/Страница 1/Страница 5")

	
	def test3 (self):
		self.assertRaises (core.exceptions.DublicateTitle, self.wiki[u"Страница 2/Страница 3/Страница 4"].moveTo, self.wiki)

