# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeWiki
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.commandchildlist import ChildListCommand
from outwiker.pages.wiki.parserfactory import ParserFactory


class WikiChildListCommandTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        factory = WikiPageFactory()
        factory.create (self.rootwiki, u"Страница 1", [])
        factory.create (self.rootwiki[u"Страница 1"], u"Страница 2", [])
        factory.create (self.rootwiki[u"Страница 1"], u"СТРАНИЦА 3", [])
        factory.create (self.rootwiki[u"Страница 1"], u"Страница 4", [])

        self.testPage = self.rootwiki[u"Страница 1"]


    def tearDown(self):
        removeWiki (self.path)


    def test1 (self):
        command = ChildListCommand (self.parser)
        result = command.execute ("", "")

        result_right = u"""<a href="Страница 2">Страница 2</a>
<a href="СТРАНИЦА 3">СТРАНИЦА 3</a>
<a href="Страница 4">Страница 4</a>"""

        self.assertEqual (result_right, result, result)


    def test2 (self):
        text = u"(:childlist:)"

        result = self.parser.toHtml (text)

        result_right = u"""<a href="Страница 2">Страница 2</a>
<a href="СТРАНИЦА 3">СТРАНИЦА 3</a>
<a href="Страница 4">Страница 4</a>"""

        self.assertEqual (result_right, result, result)


    def test3 (self):
        text = u"(:childlist:)"
        self.rootwiki[u"Страница 1/Страница 4"].order = 0

        result = self.parser.toHtml (text)

        result_right = u"""<a href="Страница 4">Страница 4</a>
<a href="Страница 2">Страница 2</a>
<a href="СТРАНИЦА 3">СТРАНИЦА 3</a>"""

        self.assertEqual (result_right, result, result)


    def test4 (self):
        text = u"(:childlist sort=name:)"
        self.rootwiki[u"Страница 1/Страница 4"].order = 0

        result = self.parser.toHtml (text)

        result_right = u"""<a href="Страница 2">Страница 2</a>
<a href="СТРАНИЦА 3">СТРАНИЦА 3</a>
<a href="Страница 4">Страница 4</a>"""

        self.assertEqual (result_right, result, result)


    def test5 (self):
        text = u"(:childlist sort=descendname:)"
        self.rootwiki[u"Страница 1/Страница 4"].order = 0

        result = self.parser.toHtml (text)

        result_right = u"""<a href="Страница 4">Страница 4</a>
<a href="СТРАНИЦА 3">СТРАНИЦА 3</a>
<a href="Страница 2">Страница 2</a>"""

        self.assertEqual (result_right, result, result)


    def test6 (self):
        text = u"(:childlist sort=descendorder:)"
        self.rootwiki[u"Страница 1/Страница 4"].order = 0

        result = self.parser.toHtml (text)

        result_right = u"""<a href="СТРАНИЦА 3">СТРАНИЦА 3</a>
<a href="Страница 2">Страница 2</a>
<a href="Страница 4">Страница 4</a>"""

        self.assertEqual (result_right, result, result)
