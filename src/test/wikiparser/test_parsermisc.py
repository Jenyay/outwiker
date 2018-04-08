# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserMiscTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        removeDir(self.path)

    def testHorLine(self):
        text = "бла-бла-бла \nкхм ---- бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм <hr> бла-бла-бла\nбла-бла-бла'

        self.assertEqual(
            self.parser.toHtml(text),
            result,
            self.parser.toHtml(text).encode(self.encoding))

    def testParseWithoutAttaches(self):
        pagetitle = "Страница 666"

        WikiPageFactory().create(self.wikiroot, pagetitle, [])
        parser = Parser(self.wikiroot[pagetitle], Application.config)

        parser.toHtml("Attach:bla-bla-bla")
