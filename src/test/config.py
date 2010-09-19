#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Тесты, связанные с конфигом
"""

import unittest
import os
import ConfigParser

from core.config import Config


class ConfigTest (unittest.TestCase):
	def setUp (self):
		self.path = u"test/testconfig.ini"

		if os.path.exists (self.path):
			os.remove (self.path)


	def testGetSet (self):
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		self.assertEqual (config.get (u"Секция 1", u"Параметр 1"), u"Значение 1")
		self.assertEqual (config.getint (u"Секция 1", u"Параметр 2"), 111)

	
	def testWrite (self):
		"""
		Тесты на то, что измененные значения сразу сохраняются в файл
		"""
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		config2 = Config (self.path)
		self.assertEqual (config2.get (u"Секция 1", u"Параметр 1"), u"Значение 1")
		self.assertEqual (config2.getint (u"Секция 1", u"Параметр 2"), 111)

	
	def testRemoveSection (self):
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		result = config.remove_section (u"Секция 1")

		config2 = Config (self.path)
		self.assertRaises (ConfigParser.NoSectionError, config2.get, u"Секция 1", u"Параметр 1")
	

	def testHasSection (self):
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		self.assertEqual (config.has_section (u"Секция 1"), True)
		
		result = config.remove_section (u"Секция 1")
		self.assertEqual (config.has_section (u"Секция 1"), False)
