# -*- coding: UTF-8 -*-

"""
Тесты для проверки фабрик страниц
"""

import unittest

from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.core.factoryselector import FactorySelector


class FactorySelectorTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/samplewiki"
        self.root = WikiDocument.load (self.path)


    def testSelection (self):
        html_page = self.root [u"Типы страниц/HTML-страница"]
        self.assertEqual (type (FactorySelector.getFactory (html_page.getTypeString())),
                          HtmlPageFactory)

        text_page = self.root [u"Типы страниц/Текстовая страница"]
        self.assertEqual (type (FactorySelector.getFactory (text_page.getTypeString())),
                          TextPageFactory)

        wiki_page = self.root [u"Типы страниц/wiki-страница"]
        self.assertEqual (type (FactorySelector.getFactory (wiki_page.getTypeString())),
                          WikiPageFactory)

        search_page = self.root [u"Типы страниц/Страница поиска"]
        self.assertEqual (type (FactorySelector.getFactory (search_page.getTypeString())),
                          SearchPageFactory)
