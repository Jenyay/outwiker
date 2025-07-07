# -*- coding: utf-8 -*-

import time
import unittest
from tempfile import mkdtemp
from typing import List

from outwiker.api.core.tree import createNotesTree
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.commands.childlist import ChildListCommand
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir


class WikiChildListCommandTest (unittest.TestCase):
    def setUp(self):
        self._application = Application()
        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self._application)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        factory = WikiPageFactory()
        self.page_1 = factory.create(self.wikiroot, "Страница 1", [])
        time.sleep(0.1)

        self.page_2 = factory.create(
            self.wikiroot["Страница 1"], "Страница 2", [])
        time.sleep(0.1)

        self.page_4 = factory.create(
            self.wikiroot["Страница 1"], "Страница 4", [])
        time.sleep(0.1)

        self.page_3 = factory.create(self.wikiroot["Страница 1"], "СТРАНИЦА 3", [])

        self.testPage = self.wikiroot["Страница 1"]

    def tearDown(self):
        removeDir(self.path)

    def _check_items_order(self, result: str, items: List[str]):
        pos = -1
        for item in items:
            next_pos = result.find(item)
            self.assertNotEqual(-1, next_pos, item)
            self.assertGreater(next_pos, pos, item)
            pos = next_pos

    def test1(self):
        command = ChildListCommand(self.parser)
        result = command.execute("", "")

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            ])

    def test2(self):
        text = "(:childlist:)"
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            ])

    def test3(self):
        text = "(:childlist:)"
        self.wikiroot["Страница 1/Страница 4"].order = 0
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            ])

    def test4(self):
        text = "(:childlist sort=name:)"
        self.wikiroot["Страница 1/Страница 4"].order = 0
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            ])

    def test5(self):
        text = "(:childlist sort=descendname:)"
        self.wikiroot["Страница 1/Страница 4"].order = 0
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            ])

    def test6(self):
        text = "(:childlist sort=descendorder:)"
        self.wikiroot["Страница 1/Страница 4"].order = 0
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            ])

    def testSortCreation_01(self):
        text = "(:childlist sort=creation:)"
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            ])

    def testSortCreation_02(self):
        text = "(:childlist sort=descendcreation:)"
        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            ])

    def testSortEdit_01(self):
        text = "(:childlist sort=edit:)"

        self.wikiroot["Страница 1/Страница 2"].content = "111"
        time.sleep(0.1)
        self.wikiroot["Страница 1/СТРАНИЦА 3"].content = "111"
        time.sleep(0.1)
        self.wikiroot["Страница 1/Страница 4"].content = "111"

        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            ])

    def testSortEdit_02(self):
        text = "(:childlist sort=descendedit:)"

        self.wikiroot["Страница 1/Страница 2"].content = "111"
        time.sleep(0.1)
        self.wikiroot["Страница 1/СТРАНИЦА 3"].content = "111"
        time.sleep(0.1)
        self.wikiroot["Страница 1/Страница 4"].content = "111"

        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            ])

    def testSortEdit_03(self):
        text = "(:childlist sort=edit:)"

        self.wikiroot["Страница 1/Страница 2"].content = "111"
        time.sleep(0.1)
        self.wikiroot["Страница 1/Страница 4"].content = "111"
        time.sleep(0.1)
        self.wikiroot["Страница 1/СТРАНИЦА 3"].content = "111"

        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Страница 4</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            ])

    def testAlias_01(self):
        text = "(:childlist:)"

        self.page_2.order = 0
        self.page_3.order = 1
        self.page_4.order = 2

        self.page_4.alias = "Абырвалг"

        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">Страница 2</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">СТРАНИЦА 3</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">Абырвалг</a>',
            ])

    def testAlias_sort(self):
        text = "(:childlist sort=name:)"

        self.page_2.order = 0
        self.page_3.order = 1
        self.page_4.order = 2

        self.page_4.alias = "AAAA"
        self.page_2.alias = "BBBB"
        self.page_3.alias = "CCCC"

        result = self.parser.toHtml(text)

        self._check_items_order(result, [
            '<a class="ow-wiki ow-link-page" href="page://Страница 4">AAAA</a>',
            '<a class="ow-wiki ow-link-page" href="page://Страница 2">BBBB</a>',
            '<a class="ow-wiki ow-link-page" href="page://СТРАНИЦА 3">CCCC</a>',
            ])
