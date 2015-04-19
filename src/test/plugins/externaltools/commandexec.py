# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class CommandExecTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.__createWiki()
        self.testPage = self.wikiroot[u'Страница 1']

        dirlist = [u'../plugins/externaltools']

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')
        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u'Страница 1', [])


    def tearDown(self):
        removeDir (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testEmpty (self):
        text = u'(:exec:)(:execend:)'
        validResult = u''

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testLinkSimple_01 (self):
        text = u'''(:exec:)gvim(:execend:)'''
        validResult = u'<a href="exec://exec/?com1=gvim">gvim</a>'

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testLinkSimple_02 (self):
        text = u'''(:exec:)

        gvim

(:execend:)'''
        validResult = u'<a href="exec://exec/?com1=gvim">gvim</a>'

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)


    def testLinkSimple_03 (self):
        text = u'''(:exec:)
gvim -d "Первый файл.txt" "Второй файл.txt"
(:execend:)'''
        validResult = ur'<a href="exec://exec/?com1=gvim&com1=-d&com1=%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9+%D1%84%D0%B0%D0%B9%D0%BB.txt&com1=%D0%92%D1%82%D0%BE%D1%80%D0%BE%D0%B9+%D1%84%D0%B0%D0%B9%D0%BB.txt">gvim</a>'

        result = self.parser.toHtml (text)
        self.assertEqual (result, validResult)
