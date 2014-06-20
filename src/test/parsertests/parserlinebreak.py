# -*- coding: UTF-8 -*-

import unittest

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserLineBreakTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

        self.__createWiki()

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


    def testLineBreak1 (self):
        text = u"Строка 1[[<<]]Строка 2"
        result_right = u"Строка 1<br>Строка 2"
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


    def testLineBreak2 (self):
        text = u"Строка 1[[&lt;&lt;]]Строка 2"
        result_right = u"Строка 1<br>Строка 2"
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


    def testLineBreak3 (self):
        text = u"Строка 1\\\nСтрока 2"
        result_right = u"Строка 1Строка 2"
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


    def testLineBreak4 (self):
        text = ur"""# Первый элемент списка.
# Второй элемент списка [[<<]]Вторая строка второго элемента списка.
# Третий элемент списка [[<<]][[<<]] Вторая строка третьего элемента списка после двух отступов.
# Четвертый элемент списка."""

        result_right = ur"""<ol><li>Первый элемент списка.</li><li>Второй элемент списка <br>Вторая строка второго элемента списка.</li><li>Третий элемент списка <br><br> Вторая строка третьего элемента списка после двух отступов.</li><li>Четвертый элемент списка.</li></ol>"""
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


    def testLineBreak5 (self):
        text = ur"""|| border=1
||Первая строка||
||Вторая строка [[<<]]продолжение второй строки||
||Третья строка [[<<]][[<<]] Продолжение третьей строки ||
||Четвертая \
строка ||"""

        result_right = ur"""<table border=1><tr><td>Первая строка</td></tr><tr><td>Вторая строка <br>продолжение второй строки</td></tr><tr><td align="left">Третья строка <br><br> Продолжение третьей строки</td></tr><tr><td align="left">Четвертая строка</td></tr></table>"""
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


    def testLineBreak6 (self):
        text = u"Строка 1\\r\nСтрока 2"
        result_right = u"Строка 1\\r\nСтрока 2"
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)
