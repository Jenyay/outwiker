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
        self.testPage = self.wikiroot['Страница 1']

        dirlist = ['../plugins/externaltools']

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, 'Страница 1', [])

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testEmpty(self):
        text = '(:exec:)(:execend:)'
        validResult = ''

        result = self.parser.toHtml(text)
        self.assertEqual(result, validResult)

    def testLinkSimple_01(self):
        text = '''(:exec:)gvim(:execend:)'''

        # <a href="exec://exec/?com1=gvim&title=gvim">gvim</a>
        result = self.parser.toHtml(text)
        self.assertIn('href="exec://exec/?', result)
        self.assertIn('com1=gvim', result)
        self.assertIn('title=gvim', result)
        self.assertIn('>gvim</a>', result)

    def testLinkSimple_02(self):
        text = '''(:exec:)

        gvim

(:execend:)'''

        # <a href="exec://exec/?com1=gvim&title=gvim">gvim</a>
        result = self.parser.toHtml(text)

        self.assertIn('href="exec://exec/?', result)
        self.assertIn('com1=gvim', result)
        self.assertIn('title=gvim', result)
        self.assertIn('>gvim</a>', result)

    def testLinkSimple_03(self):
        text = '''(:exec:)
gvim -d "Первый файл.txt" "Второй файл.txt"
(:execend:)'''
        # <a href="exec://exec/?com1=gvim&com1=-d&com1=%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9+%D1%84%D0%B0%D0%B9%D0%BB.txt&com1=%D0%92%D1%82%D0%BE%D1%80%D0%BE%D0%B9+%D1%84%D0%B0%D0%B9%D0%BB.txt&title=gvim">gvim</a>

        result = self.parser.toHtml(text)

        self.assertIn('href="exec://exec/?', result)
        self.assertIn(
            'com1=gvim&com1=-d&com1=%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9+%D1%84%D0%B0%D0%B9%D0%BB.txt&com1=%D0%92%D1%82%D0%BE%D1%80%D0%BE%D0%B9+%D1%84%D0%B0%D0%B9%D0%BB.txt',
            result)
        self.assertIn('title=gvim', result)
        self.assertIn('>gvim</a>', result)

    def testLinkTitle_01(self):
        text = '''(:exec title="Запуск gvim":)gvim(:execend:)'''

        # <a href="exec://exec/?com1=gvim&title=%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA">Запуск gvim</a>
        result = self.parser.toHtml(text)
        self.assertIn('href="exec://exec/?', result)
        self.assertIn('com1=gvim', result)
        self.assertIn('title=%D0%97%D0%B0%D0%BF%D1%83%D1%81%D0%BA', result)
        self.assertIn('>Запуск gvim</a>', result)

    def testButton_01(self):
        text = '''(:exec format="button":)gvim(:execend:)'''

        # exec://exec/?com1=gvim&title=gvim
        result = self.parser.toHtml(text)
        self.assertIn('location.href="exec://exec/?', result)
        self.assertIn('com1=gvim', result)
        self.assertIn('title=gvim', result)
        self.assertIn('<button', result)
        self.assertIn('>gvim</button>', result)

    def testButton_02(self):
        text = '''(:exec format="button" title="Запуск":)gvim(:execend:)'''

        result = self.parser.toHtml(text)
        self.assertIn('location.href="exec://exec/?', result)
        self.assertIn('com1=gvim', result)
        self.assertIn('<button', result)
        self.assertIn('>Запуск</button>', result)
