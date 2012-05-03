#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.style import Style
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki


class SpoilerPluginTest (unittest.TestCase):
    def setUp(self):
        self.__pluginname = u"Spoiler"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/spoiler"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        
        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __readFile (self, path):
        with open (path) as fp:
            result = unicode (fp.read(), "utf8")

        return result


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]
        

    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual ( len (self.loader), 1)


    def testEmptyCommand (self):
        text = u'''bla-bla-bla (:spoiler:) bla-bla-bla'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"bla-bla-bla" in result)


    def testSimple (self):
        text = u"бла-бла-бла (:spoiler:)Текст(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"Текст</div></div></div>" in result)


    def testSimpleNumbers (self):
        for index in range (10):
            text = u"бла-бла-бла (:spoiler{index}:)Текст(:spoiler{index}end:)".format (index=index)

            self.testPage.content = text

            generator = HtmlGenerator (self.testPage)
            htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
            result = self.__readFile (htmlpath)

            self.assertTrue (u"бла-бла-бла" in result)
            self.assertTrue (u"Текст</div></div></div>" in result)


    def testWikiBoldContent (self):
        text = u"бла-бла-бла (:spoiler:)'''Текст'''(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"<B>Текст</B></div></div></div>" in result)


    def testExpandText (self):
        text = u"""бла-бла-бла (:spoiler expandtext="Раскукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"Текст</div></div></div>" in result)
        self.assertTrue (u"Раскукожить</a></span></div>" in result)


    def testCollapseText (self):
        text = u"""бла-бла-бла (:spoiler collapsetext="Скукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"Текст</div></div></div>" in result)
        self.assertTrue (u"Скукожить</a>" in result)


    def testExpandCollapseText (self):
        text = u"""бла-бла-бла (:spoiler expandtext="Раскукожить" collapsetext="Скукожить":)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertTrue (u"Текст</div></div></div>" in result)
        self.assertTrue (u"Раскукожить</a></span></div>" in result)
        self.assertTrue (u"Скукожить</a>" in result)


    def testInline (self):
        text = u"бла-бла-бла (:spoiler inline:)Текст(:spoilerend:)"

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertFalse (u"Текст</div></div></div>" in result)
        self.assertTrue (u"<span><span" in result)


    def testInlineExpandText (self):
        text = u"""бла-бла-бла (:spoiler expandtext="Раскукожить" inline:)Текст(:spoilerend:)"""

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = self.__readFile (htmlpath)

        self.assertTrue (u"бла-бла-бла" in result)
        self.assertFalse (u"Текст</div></div></div>" in result)
        self.assertTrue (u"<span><span" in result)
        self.assertTrue (u"""<a href="#">Раскукожить</a>""" in result)
