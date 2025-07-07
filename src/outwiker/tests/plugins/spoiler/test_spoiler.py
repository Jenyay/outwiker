# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class SpoilerPluginTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.__pluginname = "Spoiler"
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])

        dirlist = ["plugins/spoiler"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, self.application)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testEmptyCommand(self):
        text = '''bla-bla-bla (:spoiler:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("bla-bla-bla" in result)

    def testSimple(self):
        text = "бла-бла-бла (:spoiler:)Текст(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue("Текст</div></div></div>" in result)

    def testSimpleNumbers(self):
        for index in range(10):
            text = "бла-бла-бла (:spoiler{index}:)Текст(:spoiler{index}end:)".format(
                index=index)

            self.testPage.content = text

            generator = HtmlGenerator(self.testPage, self.application)
            result = generator.makeHtml(Style().getPageStyle(self.testPage))

            self.assertTrue("бла-бла-бла" in result)
            self.assertTrue("Текст</div></div></div>" in result)

    def testWikiBoldContent(self):
        text = "бла-бла-бла (:spoiler:)'''Текст'''(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue("<b>Текст</b></div></div></div>" in result)

    def testExpandText(self):
        text = """бла-бла-бла (:spoiler expandtext="Раскукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue("Текст</div></div></div>" in result)
        self.assertTrue("Раскукожить</a></span></div>" in result)

    def testCollapseText(self):
        text = """бла-бла-бла (:spoiler collapsetext="Скукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue("Текст</div></div></div>" in result)
        self.assertTrue("Скукожить</a>" in result)

    def testExpandCollapseText(self):
        text = """бла-бла-бла (:spoiler expandtext="Раскукожить" collapsetext="Скукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertTrue("Текст</div></div></div>" in result)
        self.assertTrue("Раскукожить</a></span></div>" in result)
        self.assertTrue("Скукожить</a>" in result)

    def testInline(self):
        text = "бла-бла-бла (:spoiler inline:)Текст(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertFalse("Текст</div></div></div>" in result)
        self.assertTrue("<span><span" in result)

    def testInlineExpandText(self):
        text = """бла-бла-бла (:spoiler expandtext="Раскукожить" inline:)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertTrue("бла-бла-бла" in result)
        self.assertFalse("Текст</div></div></div>" in result)
        self.assertTrue("<span><span" in result)
        self.assertTrue("""<a href="#">Раскукожить</a>""" in result)
