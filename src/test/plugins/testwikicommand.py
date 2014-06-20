# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeWiki


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
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory().create (self.rootwiki, u"Страница 2", [])
        self.testPage = self.rootwiki[u"Страница 2"]


    def tearDown(self):
        removeWiki (self.path)


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
