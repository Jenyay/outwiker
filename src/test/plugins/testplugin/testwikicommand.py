# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class PluginWikiCommandTest(unittest.TestCase):
    """
    Проверка плагина, добавляющего обработку команды TestCommand
    """
    def setUp(self):
        self.__createWiki()

        dirlist = [u"../plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        removeDir (self.path)


    def testCommandTest (self):
        text = u"""(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды"""

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)
