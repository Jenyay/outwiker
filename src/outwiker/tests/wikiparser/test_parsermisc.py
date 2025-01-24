# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import ApplicationParams
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class ParserMiscTest (unittest.TestCase):
    def setUp(self):
        self._application = ApplicationParams()
        self.encoding = "utf8"

        self.filesPath = "testdata/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)
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
        parser = Parser(self.wikiroot[pagetitle], self._application.config)

        parser.toHtml("Attach:bla-bla-bla")
