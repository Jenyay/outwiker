# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class TOC_GeneratorTest (unittest.TestCase):
    """Тесты плагина TableOfContents"""
    def setUp (self):
        self.pluginname = u"TableOfContents"
        dirlist = [u"../plugins/tableofcontents"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.plugin = self.loader[self.pluginname]


    def tearDown (self):
        self.loader.clear()


    def testEmpty (self):
        generator = self.plugin.TOCWikiGenerator()
        items = []

        result = generator.make (items)

        result_valid = u''''''

        self.assertEqual (result, result_valid)


    def testToc_01 (self):
        generator = self.plugin.TOCWikiGenerator()
        items = [self.plugin.Section (u"Абырвалг 123", 1, u"")]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123'''

        self.assertEqual (result, result_valid)


    def testToc_02 (self):
        generator = self.plugin.TOCWikiGenerator()
        items = [
                self.plugin.Section (u"Абырвалг 123", 1, u""),
                self.plugin.Section (u"Абырвалг 12345", 1, u""),
                ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
* Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_03 (self):
        generator = self.plugin.TOCWikiGenerator()
        items = [
                self.plugin.Section (u"Абырвалг 123", 1, u""),
                self.plugin.Section (u"Абырвалг 12345", 2, u""),
                ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
** Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_04 (self):
        generator = self.plugin.TOCWikiGenerator()
        items = [
                self.plugin.Section (u"Абырвалг 123", 1, u""),
                self.plugin.Section (u"Абырвалг 12345", 5, u""),
                ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
***** Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_05 (self):
        generator = self.plugin.TOCWikiGenerator()
        items = [
                self.plugin.Section (u"Абырвалг 1", 1, u""),
                self.plugin.Section (u"Абырвалг 2", 2, u""),
                self.plugin.Section (u"Абырвалг 3", 3, u""),
                self.plugin.Section (u"Абырвалг 1", 1, u""),
                ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 1
** Абырвалг 2
*** Абырвалг 3
* Абырвалг 1'''

        self.assertEqual (result, result_valid)
