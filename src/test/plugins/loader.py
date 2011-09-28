#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from core.pluginsloader import PluginsLoader
from core.application import Application


class PluginsLoaderTest(unittest.TestCase):
	def setUp(self):
		pass


	def testEmpty (self):
		loader = PluginsLoader(Application)
		self.assertEqual (len (loader), 0)


	def testLoad (self):
		dirlist = [u"../plugins/testempty1", u"../plugins/testempty2"]
		loader = PluginsLoader(Application)
		loader.load (dirlist)

		self.assertEqual (len (loader), 2)
		self.assertEqual (loader[0].name, u"TestEmpty1")
		self.assertEqual (loader[0].version, u"0.1")
		self.assertEqual (loader[0].description, u"This plugin is empty")
		self.assertEqual (loader[0].application, Application)

		self.assertEqual (loader[1].name, u"TestEmpty2")
		self.assertEqual (loader[1].version, u"0.1")
		self.assertEqual (loader[1].description, u"This plugin is empty")

		loader.clear()
		self.assertEqual (len (loader), 0)


	def testLoadInvalid (self):
		dirlist = [u"../plugins/testinvalid",            # Нет такой директории
				u"../plugins/testinvalid1",
				u"../plugins/testinvalid2",
				u"../plugins/testinvalid3",
				u"../plugins/testinvalid4",
				u"../plugins/testinvalid5",
				u"../plugins/testinvalid6",
				u"../plugins/testempty1", 
				u"../plugins/testempty2",
				u"../plugins/testwikicommand"]

		loader = PluginsLoader(Application)
		loader.load (dirlist)

		self.assertEqual (len (loader), 3)
		self.assertEqual (loader[0].name, u"TestEmpty1")
		self.assertEqual (loader[0].version, u"0.1")
		self.assertEqual (loader[0].description, u"This plugin is empty")

		self.assertEqual (loader[1].name, u"TestEmpty2")
		self.assertEqual (loader[1].version, u"0.1")
		self.assertEqual (loader[1].description, u"This plugin is empty")

		self.assertEqual (loader[2].name, u"TestWikiCommand")
		self.assertEqual (loader[2].version, u"0.1")

