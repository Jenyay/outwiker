# -*- coding: utf-8 -*-
"""
Тесты порядка сортировки страниц
"""

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.core.config import PageConfig
from outwiker.core.config import IntegerOption
from outwiker.tests.utils import removeDir
import outwiker.core.factory as ocf


class PageOrderTest(unittest.TestCase):
    """
    Тесты порядка сортировки страниц
    """

    def setUp(self):
        # Количество срабатываний особытий при изменении порядка страниц
        self.orderUpdateCount = 0
        self.orderUpdateSender = None
        self._application = Application()

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)
        self._application.onPageOrderChange += self.onPageOrder
        self._application.wikiroot = None

    def tearDown(self):
        self._application.onPageOrderChange -= self.onPageOrder
        self._application.wikiroot = None
        removeDir(self.path)

    def onPageOrder(self, sender):
        self.orderUpdateCount += 1
        self.orderUpdateSender = sender

    def testFirstPage(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(len(self.wikiroot.children), 1)
        self.assertEqual(self.wikiroot.children[0],
                         self.wikiroot["Страница 1"])

    def testCreateOrder1(self):
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 1", [])

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 1"].order, 1)

        self.assertEqual(len(self.wikiroot.children), 2)

        self.assertEqual(self.wikiroot.children[0],
                         self.wikiroot["Страница 2"])
        self.assertEqual(self.wikiroot.children[1],
                         self.wikiroot["Страница 1"])

    def testCreateOrder2(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)

        self.assertEqual(len(self.wikiroot.children), 3)

        self.assertEqual(self.wikiroot.children[0],
                         self.wikiroot["Страница 1"])
        self.assertEqual(self.wikiroot.children[1],
                         self.wikiroot["Страница 3"])
        self.assertEqual(self.wikiroot.children[2],
                         self.wikiroot["Страница 2"])

    def testCreateOrder4(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 5", [])
        TextPageFactory().create(self.wikiroot, "Страница 7", [])

        self.wikiroot["Страница 7"].order = 1

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 5"].order, 3)

        TextPageFactory().create(self.wikiroot, "Страница 2", [])

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 5"].order, 3)
        self.assertEqual(self.wikiroot["Страница 2"].order, 4)

    def testCreateOrder5(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 5", [])
        TextPageFactory().create(self.wikiroot, "Страница 7", [])

        self.wikiroot["Страница 7"].order = 1

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 5"].order, 3)

        TextPageFactory().create(self.wikiroot, "Страница 8", [])

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 5"].order, 3)
        self.assertEqual(self.wikiroot["Страница 8"].order, 4)

    def testCreateOrder6(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 5", [])
        TextPageFactory().create(self.wikiroot, "Страница 7", [])

        self.wikiroot["Страница 7"].order = 1

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 5"].order, 3)

        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 5"].order, 3)
        self.assertEqual(self.wikiroot["Страница 4"].order, 4)

    def testCreateOrder7(self):
        TextPageFactory().create(self.wikiroot, "Страница 5", [])
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 7", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 7"].order = 1

        self.assertEqual(self.wikiroot["Страница 5"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 1"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 3)

        TextPageFactory().create(self.wikiroot, "Страница 6", [])

        self.assertEqual(self.wikiroot["Страница 5"].order, 0)
        self.assertEqual(self.wikiroot["Страница 7"].order, 1)
        self.assertEqual(self.wikiroot["Страница 1"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 3)
        self.assertEqual(self.wikiroot["Страница 6"].order, 4)

    def testCreateOrder8(self):
        TextPageFactory().create(self.wikiroot, "Плагины", [])
        TextPageFactory().create(self.wikiroot, "Абырвалг", [])
        TextPageFactory().create(self.wikiroot, "Тест", [])

        self.assertEqual(self.wikiroot["Плагины"].order, 0)
        self.assertEqual(self.wikiroot["Абырвалг"].order, 1)
        self.assertEqual(self.wikiroot["Тест"].order, 2)

        self.wikiroot["Абырвалг"].title = "Ррррр"

        wiki = loadNotesTree(self.path)

        self.assertEqual(wiki["Плагины"].order, 0)
        self.assertEqual(wiki["Ррррр"].order, 1)
        self.assertEqual(wiki["Тест"].order, 2)

    def testCreateOrder9(self):
        TextPageFactory().create(self.wikiroot, "Страница 5",
                                 [], ocf.orderCalculatorAlphabetically)

        TextPageFactory().create(self.wikiroot, "Страница 1",
                                 [], ocf.orderCalculatorAlphabetically)

        TextPageFactory().create(self.wikiroot, "Страница 2",
                                 [], ocf.orderCalculatorAlphabetically)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Страница 5"].order, 2)

    def testCreateOrder10(self):
        TextPageFactory().create(self.wikiroot, "Страница 5",
                                 [], ocf.orderCalculatorTop)

        TextPageFactory().create(self.wikiroot, "Страница 1",
                                 [], ocf.orderCalculatorTop)

        TextPageFactory().create(self.wikiroot, "Страница 2",
                                 [], ocf.orderCalculatorTop)

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 1"].order, 1)
        self.assertEqual(self.wikiroot["Страница 5"].order, 2)

    def testCreateOrder11(self):
        TextPageFactory().create(self.wikiroot, "Страница 5",
                                 [], ocf.orderCalculatorBottom)

        TextPageFactory().create(self.wikiroot, "Страница 1",
                                 [], ocf.orderCalculatorBottom)

        TextPageFactory().create(self.wikiroot, "Страница 2",
                                 [], ocf.orderCalculatorBottom)

        self.assertEqual(self.wikiroot["Страница 5"].order, 0)
        self.assertEqual(self.wikiroot["Страница 1"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)

    def testChangeOrder1(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 4"].order += 1

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 4"].order, 3)

    def testChangeOrder2(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вверх,хотя страница и так в самом верху
        self.wikiroot["Страница 1"].order -= 1

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 4"].order, 3)

    def testChangeOrder3(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 4"].order -= 1

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Страница 4"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 3)

    def testChangeOrder4(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 4"].order -= 2

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 4"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 3)

    def testChangeOrder5(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 2"].order += 2

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 4"].order, 2)
        self.assertEqual(self.wikiroot["Страница 2"].order, 3)

    def testChangeOrder6(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 2"].order = 0

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 1"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 4"].order, 3)

    def testChangeOrder7(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 2"].order = 3

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 4"].order, 2)
        self.assertEqual(self.wikiroot["Страница 2"].order, 3)

    def testChangeOrder8(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 2"].order = 100

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 4"].order, 2)
        self.assertEqual(self.wikiroot["Страница 2"].order, 3)

    def testChangeOrder9(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self.wikiroot["Страница 4"].order = -100

        self.assertEqual(self.wikiroot["Страница 4"].order, 0)
        self.assertEqual(self.wikiroot["Страница 1"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 3)

    def testEventOrder1(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self._application.wikiroot = self.wikiroot

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 4"].order += 1

        self.assertEqual(self.orderUpdateCount, 0)

    def testNoEventOrder1(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 4"].order += 1

        self.assertEqual(self.orderUpdateCount, 0)
        self.assertEqual(self.orderUpdateSender, None)

    def testEventOrder2(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self._application.wikiroot = self.wikiroot

        # Перемещаем вверх,хотя страница и так в самом верху
        self.wikiroot["Страница 1"].order -= 1

        self.assertEqual(self.orderUpdateCount, 0)

    def testNoEventOrder2(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вверх,хотя страница и так в самом верху
        self.wikiroot["Страница 1"].order -= 1

        self.assertEqual(self.orderUpdateCount, 0)
        self.assertEqual(self.orderUpdateSender, None)

    def testEventOrder3(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self._application.wikiroot = self.wikiroot

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 1"].order += 1

        self.assertEqual(self.orderUpdateCount, 1)
        self.assertEqual(self.orderUpdateSender, self.wikiroot["Страница 1"])

    def testNoEventOrder3(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 1"].order += 1

        self.assertEqual(self.orderUpdateCount, 0)
        self.assertEqual(self.orderUpdateSender, None)

    def testEventOrder4(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self._application.wikiroot = self.wikiroot

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 1"].order += 2

        self.assertEqual(self.orderUpdateCount, 1)
        self.assertEqual(self.orderUpdateSender, self.wikiroot["Страница 1"])

    def testNoEventOrder4(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 1"].order += 2

        self.assertEqual(self.orderUpdateCount, 0)
        self.assertEqual(self.orderUpdateSender, None)

    def testEventOrder5(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        self._application.wikiroot = self.wikiroot

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 1"].order = 2

        self.assertEqual(self.orderUpdateCount, 1)
        self.assertEqual(self.orderUpdateSender, self.wikiroot["Страница 1"])

    def testNoEventOrder5(self):
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 4", [])

        # Перемещаем вниз,хотя страница и так в самом низу
        self.wikiroot["Страница 1"].order = 2

        self.assertEqual(self.orderUpdateCount, 0)
        self.assertEqual(self.orderUpdateSender, None)

    def testLoading1(self):
        TextPageFactory().create(self.wikiroot, "Страница 0", [])
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])

        wikiroot = loadNotesTree(self.path)

        self.assertEqual(wikiroot["Страница 0"].order, 0)
        self.assertEqual(wikiroot["Страница 1"].order, 1)
        self.assertEqual(wikiroot["Страница 2"].order, 2)
        self.assertEqual(wikiroot["Страница 3"].order, 3)

    def testLoading2(self):
        TextPageFactory().create(self.wikiroot, "Страница 0", [])
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 0"].order += 1

        wikiroot = loadNotesTree(self.path)

        self.assertEqual(wikiroot["Страница 1"].order, 0)
        self.assertEqual(wikiroot["Страница 0"].order, 1)
        self.assertEqual(wikiroot["Страница 2"].order, 2)
        self.assertEqual(wikiroot["Страница 3"].order, 3)

    def testLoading3(self):
        TextPageFactory().create(self.wikiroot, "Страница 0", [])
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 0"].order += 1
        self.wikiroot["Страница 3"].order -= 1

        wikiroot = loadNotesTree(self.path)

        self.assertEqual(wikiroot["Страница 1"].order, 0)
        self.assertEqual(wikiroot["Страница 0"].order, 1)
        self.assertEqual(wikiroot["Страница 3"].order, 2)
        self.assertEqual(wikiroot["Страница 2"].order, 3)

    def testLoadingOldVersion1(self):
        """
        Тест на чтение вики старой версии, когда еще не было параметра order
        """
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 0", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])

        # Удалим параметры order
        IntegerOption(self.wikiroot["Страница 0"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()
        IntegerOption(self.wikiroot["Страница 1"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()
        IntegerOption(self.wikiroot["Страница 2"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()
        IntegerOption(self.wikiroot["Страница 3"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()

        wikiroot = loadNotesTree(self.path)

        self.assertEqual(wikiroot["Страница 0"].order, 0)
        self.assertEqual(wikiroot["Страница 1"].order, 1)
        self.assertEqual(wikiroot["Страница 2"].order, 2)
        self.assertEqual(wikiroot["Страница 3"].order, 3)

    def testLoadingOldVersion2(self):
        """
        Тест на чтение вики старой версии, когда еще не было параметра order
        """
        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        TextPageFactory().create(self.wikiroot, "Страница 0", [])
        TextPageFactory().create(self.wikiroot, "Страница 3", [])
        TextPageFactory().create(self.wikiroot, "Страница 2", [])

        # Удалим параметры order
        IntegerOption(self.wikiroot["Страница 0"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()
        IntegerOption(self.wikiroot["Страница 1"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()
        IntegerOption(self.wikiroot["Страница 2"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()
        IntegerOption(self.wikiroot["Страница 3"].params,
                      PageConfig.sectionName,
                      PageConfig.orderParamName, -1).remove_option()

        wikiroot = loadNotesTree(self.path)

        self.assertEqual(wikiroot["Страница 0"].order, 0)
        self.assertEqual(wikiroot["Страница 1"].order, 1)
        self.assertEqual(wikiroot["Страница 2"].order, 2)
        self.assertEqual(wikiroot["Страница 3"].order, 3)
