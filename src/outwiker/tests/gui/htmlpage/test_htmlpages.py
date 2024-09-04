# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.tests.utils import removeDir


class HtmlPagesTest(unittest.TestCase):
    """
    Тесты HTML-страниц
    """

    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix="Абырвалг абыр")

        self.__eventcount = 0
        self.__eventSender = None

        self.wikiroot = createNotesTree(self.path)

        factory = HtmlPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])

        self.wikiroot.onPageUpdate += self.__onPageUpdate

    def tearDown(self):
        self.wikiroot.onPageUpdate -= self.__onPageUpdate
        removeDir(self.path)

    def __onPageUpdate(self, sender, **kwargs):
        self.__eventcount += 1
        self.__eventSender = sender

    def testAutoLineWrap(self):
        factory = HtmlPageFactory()
        page = self.wikiroot["Страница 1"]
        page_adapter = factory.createPageAdapter(page)
        self.assertTrue(page_adapter.autoLineWrap)

        page_adapter.autoLineWrap = False
        self.assertFalse(page_adapter.autoLineWrap)

    def testAutoLineWrapReload(self):
        factory = HtmlPageFactory()
        page = self.wikiroot["Страница 1"]
        page_adapter = factory.createPageAdapter(page)
        page_adapter.autoLineWrap = False
        self.assertFalse(page_adapter.autoLineWrap)

        wiki = loadNotesTree(self.path)
        page2 = wiki["Страница 1"]
        page_adapter2 = factory.createPageAdapter(page2)
        self.assertFalse(page_adapter2.autoLineWrap)

    def testAutoLineWrapRename(self):
        factory = HtmlPageFactory()
        page = self.wikiroot["Страница 1"]
        page_adapter = factory.createPageAdapter(page)
        page_adapter.autoLineWrap = False

        self.wikiroot["Страница 1"].title = "Страница 666"
        page2 = self.wikiroot["Страница 666"]
        page_adapter2 = factory.createPageAdapter(page2)
        self.assertFalse(page_adapter2.autoLineWrap)

        wiki = loadNotesTree(self.path)
        page3 = wiki["Страница 666"]
        page_adapter3 = factory.createPageAdapter(page3)
        self.assertFalse(page_adapter3.autoLineWrap)

    def testLineWrapEvent(self):
        page = self.wikiroot["Страница 1"]
        page_adapter = HtmlPageFactory().createPageAdapter(page)
        page_adapter.autoLineWrap = False

        self.assertEqual(self.__eventcount, 1)
        self.assertEqual(self.__eventSender, self.wikiroot["Страница 1"])
