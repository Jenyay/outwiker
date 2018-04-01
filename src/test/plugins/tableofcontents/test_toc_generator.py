# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikiconfig import WikiConfig
from test.basetestcases import BaseOutWikerGUIMixin


class TOC_GeneratorTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """Тесты плагина TableOfContents"""

    def setUp(self):
        dirlist = ["../plugins/tableofcontents"]
        self.initApplication()

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()

    def testEmpty(self):
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = []

        result = generator.make(items)

        result_valid = ''''''

        self.assertEqual(result, result_valid)

    def testToc_01(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [Section("Абырвалг 123", 1, "")]

        result = generator.make(items)

        result_valid = '''* Абырвалг 123'''

        self.assertEqual(result, result_valid)

    def testToc_02(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 123", 1, ""),
            Section("Абырвалг 12345", 1, ""),
        ]

        result = generator.make(items)

        result_valid = '''* Абырвалг 123
* Абырвалг 12345'''

        self.assertEqual(result, result_valid)

    def testToc_03(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 123", 1, ""),
            Section("Абырвалг 12345", 2, ""),
        ]

        result = generator.make(items)

        result_valid = '''* Абырвалг 123
** Абырвалг 12345'''

        self.assertEqual(result, result_valid)

    def testToc_04(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 123", 1, ""),
            Section("Абырвалг 12345", 5, ""),
        ]

        result = generator.make(items)

        result_valid = '''* Абырвалг 123
***** Абырвалг 12345'''

        self.assertEqual(result, result_valid)

    def testToc_05(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 1", 1, ""),
            Section("Абырвалг 2", 2, ""),
            Section("Абырвалг 3", 3, ""),
            Section("Абырвалг 1", 1, ""),
        ]

        result = generator.make(items)

        result_valid = '''* Абырвалг 1
** Абырвалг 2
*** Абырвалг 3
* Абырвалг 1'''

        self.assertEqual(result, result_valid)

    def testToc_06(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 123", 2, ""),
            Section("Абырвалг 12345", 3, ""),
        ]

        result = generator.make(items)

        result_valid = '''* Абырвалг 123
** Абырвалг 12345'''

        self.assertEqual(result, result_valid)

    def testToc_07(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 123", 5, ""),
            Section("Абырвалг 12345", 5, ""),
        ]

        result = generator.make(items)

        result_valid = '''* Абырвалг 123
* Абырвалг 12345'''

        self.assertEqual(result, result_valid)

    def testAnchors_01(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        WikiConfig(self.application.config).linkStyleOptions.value = 0

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 1", 1, "якорь1"),
            Section("Абырвалг 2", 2, "якорь2"),
        ]

        result = generator.make(items)

        result_valid = '''* [[Абырвалг 1 -> #якорь1]]
** [[Абырвалг 2 -> #якорь2]]'''

        self.assertEqual(result, result_valid)

    def testAnchors_02(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        WikiConfig(self.application.config).linkStyleOptions.value = 1

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 1", 1, "якорь1"),
            Section("Абырвалг 2", 2, "якорь2"),
        ]

        result = generator.make(items)

        result_valid = '''* [[#якорь1 | Абырвалг 1]]
** [[#якорь2 | Абырвалг 2]]'''

        self.assertEqual(result, result_valid)

    def testAnchors_03(self):
        from tableofcontents.contentsparser import Section
        from tableofcontents.tocwikigenerator import TOCWikiGenerator

        WikiConfig(self.application.config).linkStyleOptions.value = 2

        generator = TOCWikiGenerator(self.application.config)
        items = [
            Section("Абырвалг 1", 1, "якорь1"),
            Section("Абырвалг 2", 2, "якорь2"),
        ]

        result = generator.make(items)

        result_valid = '''* [[Абырвалг 1 -> #якорь1]]
** [[Абырвалг 2 -> #якорь2]]'''

        self.assertEqual(result, result_valid)
