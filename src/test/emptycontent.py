#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os
import os.path

from outwiker.core.config import Config
from pages.wiki.emptycontent import EmptyContent


class EmptyContentTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/testconfig.ini"

		if os.path.exists (self.path):
			os.remove (self.path)

		self.text = u"""Прикрепленные файлы:
(:attachlist:)
----
Дочерние страницы:
(:childlist:)
"""


	def tearDown (self):
		if os.path.exists (self.path):
			os.remove (self.path)


	def test1 (self):
		config = Config (self.path)
		content = EmptyContent (config)

		content.content = self.text
		self.assertEqual (content.content, self.text)


	def testDefault (self):
		config = Config (self.path)
		content = EmptyContent (config)

		# Проверим, что есть какое-то непустое значение по умолчанию
		self.assertNotEqual (len (content.content.strip()), 0)


	def testRead (self):
		config = Config (self.path)
		content1 = EmptyContent (config)
		content2 = EmptyContent (config)

		content1.content = self.text

		# Проверим, что есть какое-то непустое значение по умолчанию
		self.assertEqual (content2.content, self.text)
		self.assertEqual (content2.content, content1.content)


	def testRead2 (self):
		config = Config (self.path)
		content1 = EmptyContent (config)

		content1.content = self.text

		content2 = EmptyContent (config)

		# Проверим, что есть какое-то непустое значение по умолчанию
		self.assertEqual (content2.content, self.text)
		self.assertEqual (content2.content, content1.content)

