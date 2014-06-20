# -*- coding: utf-8 -*-
"""
Тесты порядка сортировки страниц
"""

import unittest

from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.core.config import PageConfig
from outwiker.core.config import IntegerOption
from test.utils import removeWiki


class PageOrderTest (unittest.TestCase):
    """
    Тесты порядка сортировки страниц
    """
    def setUp (self):
        # Количество срабатываний особытий при изменении порядка страниц
        self.orderUpdateCount = 0
        self.orderUpdateSender = None

        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)
        Application.onPageOrderChange += self.onPageOrder
        Application.wikiroot = None


    def tearDown(self):
        Application.onPageOrderChange -= self.onPageOrder
        Application.wikiroot = None
        removeWiki (self.path)


    def onPageOrder (self, sender):
        self.orderUpdateCount += 1
        self.orderUpdateSender = sender


    def testFirstPage (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (len (self.rootwiki.children), 1)
        self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])


    def testCreateOrder1 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)

        self.assertEqual (len (self.rootwiki.children), 2)
        self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
        self.assertEqual (self.rootwiki.children[1], self.rootwiki[u"Страница 2"])


    def testCreateOrder2 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)

        self.assertEqual (len (self.rootwiki.children), 3)
        self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
        self.assertEqual (self.rootwiki.children[1], self.rootwiki[u"Страница 2"])
        self.assertEqual (self.rootwiki.children[2], self.rootwiki[u"Страница 3"])


    def testCreateOrder3 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)

        self.assertEqual (len (self.rootwiki.children), 2)
        self.assertEqual (self.rootwiki.children[0], self.rootwiki[u"Страница 1"])
        self.assertEqual (self.rootwiki.children[1], self.rootwiki[u"Страница 2"])


    def testCreateOrder4 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 5", [])
        TextPageFactory().create (self.rootwiki, u"Страница 7", [])

        self.rootwiki[u"Страница 7"].order = 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

        TextPageFactory().create (self.rootwiki, u"Страница 2", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 4)


    def testCreateOrder5 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 5", [])
        TextPageFactory().create (self.rootwiki, u"Страница 7", [])

        self.rootwiki[u"Страница 7"].order = 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

        TextPageFactory().create (self.rootwiki, u"Страница 8", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)
        self.assertEqual (self.rootwiki[u"Страница 8"].order, 4)


    def testCreateOrder6 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 5", [])
        TextPageFactory().create (self.rootwiki, u"Страница 7", [])

        self.rootwiki[u"Страница 7"].order = 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 4)


    def testCreateOrder7 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 5", [])
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 7", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])

        self.rootwiki[u"Страница 7"].order = 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)

        TextPageFactory().create (self.rootwiki, u"Страница 6", [])

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 7"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 5"].order, 3)
        self.assertEqual (self.rootwiki[u"Страница 6"].order, 4)


    def testCreateOrder8 (self):
        TextPageFactory().create (self.rootwiki, u"Плагины", [])
        TextPageFactory().create (self.rootwiki, u"Абырвалг", [])
        TextPageFactory().create (self.rootwiki, u"Тест", [])

        self.assertEqual (self.rootwiki[u"Абырвалг"].order, 0)
        self.assertEqual (self.rootwiki[u"Плагины"].order, 1)
        self.assertEqual (self.rootwiki[u"Тест"].order, 2)

        self.rootwiki[u"Абырвалг"].title = u"Ррррр"

        wiki = WikiDocument.load (self.path)

        self.assertEqual (wiki[u"Ррррр"].order, 0)
        self.assertEqual (wiki[u"Плагины"].order, 1)
        self.assertEqual (wiki[u"Тест"].order, 2)


    def testChangeOrder1 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 4"].order += 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)


    def testChangeOrder2 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вверх,хотя страница и так в самом верху
        self.rootwiki[u"Страница 1"].order -= 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)


    def testChangeOrder3 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 4"].order -= 1

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)


    def testChangeOrder4 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 4"].order -= 2

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)


    def testChangeOrder5 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 2"].order += 2

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 3)


    def testChangeOrder6 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 2"].order = 0

        self.assertEqual (self.rootwiki[u"Страница 2"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 1"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 3)


    def testChangeOrder7 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 2"].order = 3

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 3)


    def testChangeOrder8 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 2"].order = 100

        self.assertEqual (self.rootwiki[u"Страница 1"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 4"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 3)


    def testChangeOrder9 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        self.rootwiki[u"Страница 4"].order = -100

        self.assertEqual (self.rootwiki[u"Страница 4"].order, 0)
        self.assertEqual (self.rootwiki[u"Страница 1"].order, 1)
        self.assertEqual (self.rootwiki[u"Страница 2"].order, 2)
        self.assertEqual (self.rootwiki[u"Страница 3"].order, 3)


    def testEventOrder1 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        Application.wikiroot = self.rootwiki

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 4"].order += 1

        self.assertEqual (self.orderUpdateCount, 1)
        self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 4"])


    def testNoEventOrder1 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 4"].order += 1

        self.assertEqual (self.orderUpdateCount, 0)
        self.assertEqual (self.orderUpdateSender, None)


    def testEventOrder2 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        Application.wikiroot = self.rootwiki

        # Перемещаем вверх,хотя страница и так в самом верху
        self.rootwiki[u"Страница 1"].order -= 1

        self.assertEqual (self.orderUpdateCount, 1)
        self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])


    def testNoEventOrder2 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вверх,хотя страница и так в самом верху
        self.rootwiki[u"Страница 1"].order -= 1

        self.assertEqual (self.orderUpdateCount, 0)
        self.assertEqual (self.orderUpdateSender, None)


    def testEventOrder3 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        Application.wikiroot = self.rootwiki

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 1"].order += 1

        self.assertEqual (self.orderUpdateCount, 1)
        self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])


    def testNoEventOrder3 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 1"].order += 1

        self.assertEqual (self.orderUpdateCount, 0)
        self.assertEqual (self.orderUpdateSender, None)


    def testEventOrder4 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        Application.wikiroot = self.rootwiki

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 1"].order += 2

        self.assertEqual (self.orderUpdateCount, 1)
        self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])


    def testNoEventOrder4 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 1"].order += 2

        self.assertEqual (self.orderUpdateCount, 0)
        self.assertEqual (self.orderUpdateSender, None)


    def testEventOrder5 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        Application.wikiroot = self.rootwiki

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 1"].order = 2

        self.assertEqual (self.orderUpdateCount, 1)
        self.assertEqual (self.orderUpdateSender, self.rootwiki[u"Страница 1"])


    def testNoEventOrder5 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.rootwiki[u"Страница 1"].order = 2

        self.assertEqual (self.orderUpdateCount, 0)
        self.assertEqual (self.orderUpdateSender, None)


    def testLoading1 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 0", [])
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])

        wikiroot = WikiDocument.load (self.path)

        self.assertEqual (wikiroot[u"Страница 0"].order, 0)
        self.assertEqual (wikiroot[u"Страница 1"].order, 1)
        self.assertEqual (wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (wikiroot[u"Страница 3"].order, 3)


    def testLoading2 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 0", [])
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])

        self.rootwiki[u"Страница 0"].order += 1

        wikiroot = WikiDocument.load (self.path)

        self.assertEqual (wikiroot[u"Страница 1"].order, 0)
        self.assertEqual (wikiroot[u"Страница 0"].order, 1)
        self.assertEqual (wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (wikiroot[u"Страница 3"].order, 3)


    def testLoading3 (self):
        TextPageFactory().create (self.rootwiki, u"Страница 0", [])
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])

        self.rootwiki[u"Страница 0"].order += 1
        self.rootwiki[u"Страница 3"].order -= 1

        wikiroot = WikiDocument.load (self.path)

        self.assertEqual (wikiroot[u"Страница 1"].order, 0)
        self.assertEqual (wikiroot[u"Страница 0"].order, 1)
        self.assertEqual (wikiroot[u"Страница 3"].order, 2)
        self.assertEqual (wikiroot[u"Страница 2"].order, 3)


    def testLoadingOldVersion1 (self):
        """
        Тест на чтение вики старой версии, когда еще не было параметра order
        """
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 0", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])

        # Удалим параметры order
        IntegerOption (self.rootwiki[u"Страница 0"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()
        IntegerOption (self.rootwiki[u"Страница 1"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()
        IntegerOption (self.rootwiki[u"Страница 2"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()
        IntegerOption (self.rootwiki[u"Страница 3"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()

        wikiroot = WikiDocument.load (self.path)

        self.assertEqual (wikiroot[u"Страница 0"].order, 0)
        self.assertEqual (wikiroot[u"Страница 1"].order, 1)
        self.assertEqual (wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (wikiroot[u"Страница 3"].order, 3)


    def testLoadingOldVersion2 (self):
        """
        Тест на чтение вики старой версии, когда еще не было параметра order
        """
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        TextPageFactory().create (self.rootwiki, u"Страница 0", [])
        TextPageFactory().create (self.rootwiki, u"Страница 3", [])
        TextPageFactory().create (self.rootwiki, u"Страница 2", [])

        # Удалим параметры order
        IntegerOption (self.rootwiki[u"Страница 0"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()
        IntegerOption (self.rootwiki[u"Страница 1"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()
        IntegerOption (self.rootwiki[u"Страница 2"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()
        IntegerOption (self.rootwiki[u"Страница 3"].params, PageConfig.sectionName, PageConfig.orderParamName, -1).remove_option()

        wikiroot = WikiDocument.load (self.path)

        self.assertEqual (wikiroot[u"Страница 0"].order, 0)
        self.assertEqual (wikiroot[u"Страница 1"].order, 1)
        self.assertEqual (wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (wikiroot[u"Страница 3"].order, 3)
