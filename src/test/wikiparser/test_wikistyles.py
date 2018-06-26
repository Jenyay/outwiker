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
        text = "текст %class-red%бла-бла-бла%% текст"
        result = 'текст <span class="class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_space_01(self):
        text = "текст %class-red% бла-бла-бла %% текст"
        result = 'текст <span class="class-red"> бла-бла-бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_01(self):
        text = "текст %class-red%бла_class-red %class-blue%бла_class-blue%% бла%% текст"
        result = 'текст <span class="class-red">бла_class-red <span class="class-blue">бла_class-blue</span> бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_01_space(self):
        text = "текст %class-red% бла_class-red %class-blue% бла_class-blue %% бла %% текст"
        result = 'текст <span class="class-red"> бла_class-red <span class="class-blue"> бла_class-blue </span> бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_02(self):
        text = "текст %class-red%%class-blue%бла_class-blue%%%% текст"
        result = 'текст <span class="class-red"><span class="class-blue">бла_class-blue</span></span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_02_space(self):
        text = "текст %class-red% %class-blue% бла_class-blue %% %% текст"
        result = 'текст <span class="class-red"> <span class="class-blue"> бла_class-blue </span> </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def testInline_style_nested_03(self):
        text = "текст %class-red%бла_class-red %class-blue%бла_class-blue%% %class-yellow%бла_class-yellow%% бла-бла %% текст"
        result_valid = 'текст <span class="class-red">бла_class-red <span class="class-blue">бла_class-blue</span> <span class="class-yellow">бла_class-yellow</span> бла-бла </span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_01(self):
        text = "текст %class-red%абыр валг [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абыр валг %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_02(self):
        text = "текст %class-red%абырвалг %class-blue%текст class-blue%% [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-blue">текст class-blue</span> %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_03(self):
        text = "текст %class-red%абырвалг %class-blue%текст class-blue%% 111 [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-blue">текст class-blue</span> 111 %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_04(self):
        text = "текст %class-red%абырвалг [=%%=] %class-blue%текст class-blue%% проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг %% <span class="class-blue">текст class-blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def testInline_style_nested_skip_05(self):
        text = "текст %class-red%абырвалг %class-yellow%текст class-yellow%% [=%%=] %class-blue%текст class-blue%% проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-yellow">текст class-yellow</span> %% <span class="class-blue">текст class-blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)
