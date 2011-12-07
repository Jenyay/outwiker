#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
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
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        self.testPage = self.rootwiki[u"Страница 2"]
        

    def tearDown(self):
        removeWiki (self.path)
    

    def testLineBreak1 (self):
        text = u"Строка 1[[<<]]Строка 2"
        result_right = u"Строка 1<BR>Строка 2"
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)
    

    def testLineBreak2 (self):
        text = u"Строка 1[[&lt;&lt;]]Строка 2"
        result_right = u"Строка 1<BR>Строка 2"
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

        result_right = ur"""<OL><LI>Первый элемент списка.</LI><LI>Второй элемент списка <BR>Вторая строка второго элемента списка.</LI><LI>Третий элемент списка <BR><BR> Вторая строка третьего элемента списка после двух отступов.</LI><LI>Четвертый элемент списка.</LI></OL>"""
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


    def testLineBreak5 (self):
        text = ur"""|| border=1
||Первая строка||
||Вторая строка [[<<]]продолжение второй строки||
||Третья строка [[<<]][[<<]] Продолжение третьей строки ||
||Четвертая \
строка ||"""

        result_right = ur"""<TABLE border=1><TR><TD>Первая строка</TD></TR><TR><TD>Вторая строка <BR>продолжение второй строки</TD></TR><TR><TD ALIGN="LEFT">Третья строка <BR><BR> Продолжение третьей строки</TD></TR><TR><TD ALIGN="LEFT">Четвертая строка</TD></TR></TABLE>"""
        result = self.parser.toHtml (text)

        self.assertEqual (result, result_right, result)


