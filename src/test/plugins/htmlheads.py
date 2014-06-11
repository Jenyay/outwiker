#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.system import readTextFile
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki


class HtmlHeadsTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()
        self.testPage = self.rootwiki[u"Страница 1"]

        dirlist = [u"../plugins/htmlheads"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])


    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testTitle_01 (self):
        text = u'(:title Бла-бла-бла:)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u"<title>Бла-бла-бла</title>", result)


    def testTitle_02 (self):
        text = u'(:title    Бла-бла-бла бла-бла   :)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u"<title>Бла-бла-бла бла-бла</title>", result)


    def testDescription_01 (self):
        text = u'(:description Бла-бла-бла абырвалг:)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="description" content="Бла-бла-бла абырвалг"/>', result)


    def testDescription_02 (self):
        text = u'(:description    Бла-бла-бла абырвалг   :)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="description" content="Бла-бла-бла абырвалг"/>', result)


    def testDescription_03 (self):
        text = u'(:description:)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="description" content=""/>', result)


    def testKeywords_01 (self):
        text = u'(:keywords Бла-бла-бла, абырвалг:)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)


    def testKeywords_02 (self):
        text = u'(:keywords     Бла-бла-бла, абырвалг    :)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)


    def testKeywords_03 (self):
        text = u'(:keywords:)'

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="keywords" content=""/>', result)


    def testHtmlHead_01 (self):
        text = u'''(:htmlhead:)<meta name="keywords" content="Бла-бла-бла, абырвалг"/>(:htmlheadend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)
        self.assertNotIn ("(:htmlhead:)", result)


    def testHtmlHead_02 (self):
        text = u'''(:htmlhead:)
        <meta name="keywords" content="Бла-бла-бла, абырвалг"/>
        <meta name="description" content="Бла-бла-бла абырвалг"/>
(:htmlheadend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertIn (u'<meta name="keywords" content="Бла-бла-бла, абырвалг"/>', result)
        self.assertIn (u'<meta name="description" content="Бла-бла-бла абырвалг"/>', result)
        self.assertNotIn ("(:htmlhead:)", result)


    def testHtmlHead_03 (self):
        text = u'''(:htmlhead:)(:htmlheadend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        htmlpath = generator.makeHtml (Style().getPageStyle (self.testPage))
        result = readTextFile (htmlpath)

        self.assertNotIn ("(:htmlhead:)", result)
