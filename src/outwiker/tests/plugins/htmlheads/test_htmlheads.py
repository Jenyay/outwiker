# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class HtmlHeadsTest(BaseOutWikerGUIMixin, unittest.TestCase):
    def setUp(self):
        self.initApplication()
        self.maxDiff = None

        self.filesPath = "testdata/samplefiles/"
        self.__createWiki()
        self.testPage = self.wikiroot["Страница 1"]

        dirlist = ["plugins/htmlheads"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, self.application)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix="Абырвалг абыр")

        self.wikiroot = createNotesTree(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()
        self.destroyApplication()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testTitle_01(self):
        text = "(:title Бла-бла-бла:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn("<title>Бла-бла-бла</title>", result)

    def testTitle_02(self):
        text = "(:title    Бла-бла-бла бла-бла   :)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn("<title>Бла-бла-бла бла-бла</title>", result)

    def testDescription_01(self):
        text = "(:description Бла-бла-бла абырвалг:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn(
            '<meta name="description" content="Бла-бла-бла абырвалг"/>', result
        )

    def testDescription_02(self):
        text = "(:description    Бла-бла-бла абырвалг   :)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn(
            '<meta name="description" content="Бла-бла-бла абырвалг"/>', result
        )

    def testDescription_03(self):
        text = "(:description:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('<meta name="description" content=""/>', result)

    def testKeywords_01(self):
        text = "(:keywords Бла-бла-бла, абырвалг:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)

    def testKeywords_02(self):
        text = "(:keywords     Бла-бла-бла, абырвалг    :)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)

    def testKeywords_03(self):
        text = "(:keywords:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('<meta name="keywords" content=""/>', result)

    def testHtmlHead_01(self):
        text = """(:htmlhead:)<meta name="keywords" content="Бла-бла-бла, абырвалг"/>(:htmlheadend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)
        self.assertNotIn("(:htmlhead:)", result)

    def testHtmlHead_02(self):
        text = """(:htmlhead:)
        <meta name="keywords" content="Бла-бла-бла, абырвалг"/>
        <meta name="description" content="Бла-бла-бла абырвалг"/>
(:htmlheadend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn('<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)
        self.assertIn(
            '<meta name="description" content="Бла-бла-бла абырвалг"/>', result
        )
        self.assertNotIn("(:htmlhead:)", result)

    def testHtmlHead_03(self):
        text = """(:htmlhead:)(:htmlheadend:)"""

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertNotIn("(:htmlhead:)", result)

    def testStyle_01(self):
        text = "(:style:)body {color: blue};(:styleend:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn("""<style>body {color: blue};</style>""", result)
        self.assertNotIn("(:style:)", result)

    def testStyle_02(self):
        text = "(:style:)   body {color: blue};   (:styleend:)"

        self.testPage.content = text

        generator = HtmlGenerator(self.testPage, self.application)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))

        self.assertIn("""<style>body {color: blue};</style>""", result)
        self.assertNotIn("(:style:)", result)
