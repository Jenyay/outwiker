# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class PluginWikiCommandTest(BaseOutWikerGUIMixin, unittest.TestCase):
    """
    Проверка плагина, добавляющего обработку команды TestCommand
    """

    def setUp(self):
        self.initApplication()
        self.__createWiki()

        dirlist = ["testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self.application)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def testCommandTest(self):
        text = """(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды"""

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)
