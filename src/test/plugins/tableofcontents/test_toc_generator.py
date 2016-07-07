# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.pages.wiki.wikiconfig import WikiConfig


class TOC_GeneratorTest (unittest.TestCase):
    """Тесты плагина TableOfContents"""
    def setUp (self):
        dirlist = [u"../plugins/tableofcontents"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        self.loader.clear()


    def testEmpty (self):
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = []

        result = generator.make (items)

        result_valid = u''''''

        self.assertEqual (result, result_valid)


    def testToc_01 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [Section (u"Абырвалг 123", 1, u"")]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123'''

        self.assertEqual (result, result_valid)


    def testToc_02 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 123", 1, u""),
            Section (u"Абырвалг 12345", 1, u""),
        ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
* Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_03 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 123", 1, u""),
            Section (u"Абырвалг 12345", 2, u""),
        ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
** Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_04 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 123", 1, u""),
            Section (u"Абырвалг 12345", 5, u""),
        ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
***** Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_05 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 1", 1, u""),
            Section (u"Абырвалг 2", 2, u""),
            Section (u"Абырвалг 3", 3, u""),
            Section (u"Абырвалг 1", 1, u""),
        ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 1
** Абырвалг 2
*** Абырвалг 3
* Абырвалг 1'''

        self.assertEqual (result, result_valid)


    def testToc_06 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 123", 2, u""),
            Section (u"Абырвалг 12345", 3, u""),
        ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
** Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testToc_07 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 123", 5, u""),
            Section (u"Абырвалг 12345", 5, u""),
        ]

        result = generator.make (items)

        result_valid = u'''* Абырвалг 123
* Абырвалг 12345'''

        self.assertEqual (result, result_valid)


    def testAnchors_01 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        WikiConfig (Application.config).linkStyleOptions.value = 0

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 1", 1, u"якорь1"),
            Section (u"Абырвалг 2", 2, u"якорь2"),
        ]

        result = generator.make (items)

        result_valid = u'''* [[Абырвалг 1 -> #якорь1]]
** [[Абырвалг 2 -> #якорь2]]'''

        self.assertEqual (result, result_valid)


    def testAnchors_02 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        WikiConfig (Application.config).linkStyleOptions.value = 1

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 1", 1, u"якорь1"),
            Section (u"Абырвалг 2", 2, u"якорь2"),
        ]

        result = generator.make (items)

        result_valid = u'''* [[#якорь1 | Абырвалг 1]]
** [[#якорь2 | Абырвалг 2]]'''

        self.assertEqual (result, result_valid)


    def testAnchors_03 (self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        WikiConfig (Application.config).linkStyleOptions.value = 2

        generator = TOCWikiGenerator(Application.config)
        items = [
            Section (u"Абырвалг 1", 1, u"якорь1"),
            Section (u"Абырвалг 2", 2, u"якорь2"),
        ]

        result = generator.make (items)

        result_valid = u'''* [[Абырвалг 1 -> #якорь1]]
** [[Абырвалг 2 -> #якорь2]]'''

        self.assertEqual (result, result_valid)
