# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class WikiStylesTest(unittest.TestCase):
    def setUp(self):
        self.filesPath = "../test/samplefiles/"

        self.__createWiki()
        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)
        self.maxDiff = None

    def tearDown(self):
        removeDir(self.path)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def testInline_style_01(self):
        text = "текст %red%бла-бла-бла%% текст"
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_space_01(self):
        text = "текст %red% бла-бла-бла %% текст"
        result = 'текст <span class="red"> бла-бла-бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_01(self):
        text = "текст %red%бла_red %blue%бла_blue%% бла%% текст"
        result = 'текст <span class="red">бла_red <span class="blue">бла_blue</span> бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_01_space(self):
        text = "текст %red% бла_red %blue% бла_blue %% бла %% текст"
        result = 'текст <span class="red"> бла_red <span class="blue"> бла_blue </span> бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_02(self):
        text = "текст %red%%blue%бла_blue%%%% текст"
        result = 'текст <span class="red"><span class="blue">бла_blue</span></span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_02_space(self):
        text = "текст %red% %blue% бла_blue %% %% текст"
        result = 'текст <span class="red"> <span class="blue"> бла_blue </span> </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_03(self):
        text = "текст %red%бла_red %blue%бла_blue%% %yellow%бла_yellow%% бла-бла %% текст"
        result_valid = 'текст <span class="red">бла_red <span class="blue">бла_blue</span> <span class="yellow">бла_yellow</span> бла-бла </span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_01(self):
        text = "текст %red%абыр валг [=%%=] проверка%% текст"
        result_valid = 'текст <span class="red">абыр валг %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_02(self):
        text = "текст %red%абырвалг %blue%текст blue%% [=%%=] проверка%% текст"
        result_valid = 'текст <span class="red">абырвалг <span class="blue">текст blue</span> %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_03(self):
        text = "текст %red%абырвалг %blue%текст blue%% 111 [=%%=] проверка%% текст"
        result_valid = 'текст <span class="red">абырвалг <span class="blue">текст blue</span> 111 %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_04(self):
        text = "текст %red%абырвалг [=%%=] %blue%текст blue%% проверка%% текст"
        result_valid = 'текст <span class="red">абырвалг %% <span class="blue">текст blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_05(self):
        text = "текст %red%абырвалг %yellow%текст yellow%% [=%%=] %blue%текст blue%% проверка%% текст"
        result_valid = 'текст <span class="red">абырвалг <span class="yellow">текст yellow</span> %% <span class="blue">текст blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)
