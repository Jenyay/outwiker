#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import unittest

import core.i18n


class I18nTest(unittest.TestCase):
	def setUp(self):
		self.path = "../test/locale"

	def testGetLang (self):
		langs = core.i18n.getLanguages()
		self.assertEqual (len (langs), 2)
		index1 = langs.index ("ru")
		index2 = langs.index ("en")

		self.assertRaises (ValueError, langs.index, "test")
	

	def testIsLang (self):
		self.assertTrue (core.i18n.isLangDir (self.path, "ru") )
		self.assertFalse (core.i18n.isLangDir (self.path, "test") )
		self.assertTrue (core.i18n.isLangDir (self.path, "test2") )

