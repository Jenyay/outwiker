# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.parser.tokenwikistyle import StyleGenerator


class WikiStylesInlineTest(unittest.TestCase):
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

    def test_style_01(self):
        text = "текст %class-red%бла-бла-бла%% текст"
        result = 'текст <span class="class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_space_01(self):
        text = "текст %class-red% бла-бла-бла %% текст"
        result = 'текст <span class="class-red"> бла-бла-бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_01(self):
        text = "текст %class-red%бла_class-red %class-blue%бла_class-blue%% бла%% текст"
        result = 'текст <span class="class-red">бла_class-red <span class="class-blue">бла_class-blue</span> бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_01_space(self):
        text = "текст %class-red% бла_class-red %class-blue% бла_class-blue %% бла %% текст"
        result = 'текст <span class="class-red"> бла_class-red <span class="class-blue"> бла_class-blue </span> бла </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_02(self):
        text = "текст %class-red%%class-blue%бла_class-blue%%%% текст"
        result = 'текст <span class="class-red"><span class="class-blue">бла_class-blue</span></span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_02_space(self):
        text = "текст %class-red% %class-blue% бла_class-blue %% %% текст"
        result = 'текст <span class="class-red"> <span class="class-blue"> бла_class-blue </span> </span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_style_nested_03(self):
        text = "текст %class-red%бла_class-red %class-blue%бла_class-blue%% %class-yellow%бла_class-yellow%% бла-бла %% текст"
        result_valid = 'текст <span class="class-red">бла_class-red <span class="class-blue">бла_class-blue</span> <span class="class-yellow">бла_class-yellow</span> бла-бла </span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_01(self):
        text = "текст %class-red%абыр валг [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абыр валг %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_02(self):
        text = "текст %class-red%абырвалг %class-blue%текст class-blue%% [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-blue">текст class-blue</span> %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_03(self):
        text = "текст %class-red%абырвалг %class-blue%текст class-blue%% 111 [=%%=] проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-blue">текст class-blue</span> 111 %% проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_04(self):
        text = "текст %class-red%абырвалг [=%%=] %class-blue%текст class-blue%% проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг %% <span class="class-blue">текст class-blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_style_nested_skip_05(self):
        text = "текст %class-red%абырвалг %class-yellow%текст class-yellow%% [=%%=] %class-blue%текст class-blue%% проверка%% текст"
        result_valid = 'текст <span class="class-red">абырвалг <span class="class-yellow">текст class-yellow</span> %% <span class="class-blue">текст class-blue</span> проверка</span> текст'
        result = self.parser.toHtml(text)

        self.assertEqual(result_valid, result, result)

    def test_many_styles_01(self):
        text = "текст %class-red class-my%бла-бла-бла%% текст"
        result = 'текст <span class="class-red class-my">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_many_styles_02(self):
        text = "текст %class-my class-red%бла-бла-бла%% текст"
        result = 'текст <span class="class-my class-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))

    def test_red_color(self):
        text = "текст %red%бла-бла-бла%% текст"
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.red { color: red; }</style>\n',
                      self.parser.headItems)

    def test_red_color_upper(self):
        text = "текст %RED%бла-бла-бла%% текст"
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.red { color: red; }</style>\n',
                      self.parser.headItems)

    def test_red_color_param_upper(self):
        text = "текст %color=RED%бла-бла-бла%% текст"
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.red { color: red; }</style>\n',
                      self.parser.headItems)

    def test_red_color_param(self):
        text = "текст %color=red%бла-бла-бла%% текст"
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.red { color: red; }</style>\n',
                      self.parser.headItems)

    def test_red_color_param_quote_single(self):
        text = "текст %color='red'%бла-бла-бла%% текст"
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.red { color: red; }</style>\n',
                      self.parser.headItems)

    def test_red_color_param_quote_double(self):
        text = 'текст %color="red"%бла-бла-бла%% текст'
        result = 'текст <span class="red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.red { color: red; }</style>\n',
                      self.parser.headItems)

    def test_color_value_01(self):
        text = 'текст %color="#11AA55"%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_color_value_02(self):
        text = 'текст %color="#11AA55"%бла-бла-бла%% текст %color="#22BB66"%бла-бла-бла%%'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст <span class="style-2">бла-бла-бла</span>'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertIn('<style>span.style-2 { color: #22bb66; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 2)

    def test_color_value_03(self):
        text = 'текст %color=#11AA55%бла-бла-бла%% текст %color="#22BB66"%бла-бла-бла%%'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст <span class="style-2">бла-бла-бла</span>'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertIn('<style>span.style-2 { color: #22bb66; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 2)

    def test_color_value_repeat_01(self):
        text = 'текст %color=#11AA55%бла-бла-бла%% текст %color="#11AA55"%бла-бла-бла%%'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст <span class="style-1">бла-бла-бла</span>'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_color_value_number(self):
        text = 'текст %#11AA55%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_bgcolor_value_number_01(self):
        text = 'текст %bgcolor=#11AA55%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { background-color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_bgcolor_value_number_02(self):
        text = 'текст %bgcolor="#11AA55"%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { background-color: #11aa55; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_bgcolor_value_name(self):
        text = 'текст %bgcolor="red"%бла-бла-бла%% текст'
        result = 'текст <span class="bg-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.bg-red { background-color: red; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_bgcolor_standard_name_01(self):
        text = 'текст %bg-red%бла-бла-бла%% текст'
        result = 'текст <span class="bg-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.bg-red { background-color: red; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_bgcolor_standard_name_02(self):
        text = 'текст %bg_red%бла-бла-бла%% текст'
        result = 'текст <span class="bg-red">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.bg-red { background-color: red; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_color_bgcolor_standard(self):
        text = 'текст %blue bg_red%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: blue; background-color: red; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_color_bgcolor_01(self):
        text = 'текст %blue bgcolor=red%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: blue; background-color: red; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_user_style_01(self):
        text = 'текст %blue style="font-weight: bold;"%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: blue; font-weight: bold; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)

    def test_user_style_02(self):
        text = 'текст %blue style="font-weight: bold"%бла-бла-бла%% текст'
        result = 'текст <span class="style-1">бла-бла-бла</span> текст'

        self.assertEqual(result, self.parser.toHtml(text))
        self.assertIn('<style>span.style-1 { color: blue; font-weight: bold; }</style>\n',
                      self.parser.headItems)
        self.assertEqual(len(self.parser.headItems), 1)


class StyleGeneratorTest(unittest.TestCase):
    def test_style_color_name(self):
        style_generator = StyleGenerator({}, True)
        params = [('red', '')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['red'])
        self.assertEqual(css_list, ['span.red { color: red; }'])

    def test_style_color_name_repeat(self):
        style_generator = StyleGenerator({}, True)
        params = [('red', '')]

        classes, css_list = style_generator.getStyle(params)
        self.assertEqual(classes, ['red'])
        self.assertEqual(css_list, ['span.red { color: red; }'])

        name, css = style_generator.getStyle(params)
        self.assertEqual(classes, ['red'])
        self.assertEqual(css_list, ['span.red { color: red; }'])

    def test_style_color_name_param(self):
        style_generator = StyleGenerator({}, True)
        params = [('color', 'red')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['red'])
        self.assertEqual(css_list, ['span.red { color: red; }'])

    def test_style_color_value_01(self):
        style_generator = StyleGenerator({}, True)
        params = [('color', '#1A5')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: #1A5; }'])

    def test_style_color_value_02(self):
        style_generator = StyleGenerator({}, True)
        params = [('color', '#11AA55')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: #11AA55; }'])

    def test_style_color_value_repeat(self):
        style_generator = StyleGenerator({}, True)
        params = [('color', '#11AA55')]

        classes, css_list = style_generator.getStyle(params)
        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: #11AA55; }'])

        classes, css_list = style_generator.getStyle(params)
        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, [])

    def test_style_color_value_many(self):
        style_generator = StyleGenerator({}, True)

        params_1 = [('color', '#11AA55')]
        classes, css_list = style_generator.getStyle(params_1)
        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: #11AA55; }'])

        params_2 = [('color', '#22BB66')]
        classes, css_list = style_generator.getStyle(params_2)
        self.assertEqual(classes, ['style-2'])
        self.assertEqual(css_list, ['span.style-2 { color: #22BB66; }'])

    def test_style_bgcolor_name(self):
        style_generator = StyleGenerator({}, True)
        params = [('bgcolor', 'red')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

    def test_style_bgcolor_value(self):
        style_generator = StyleGenerator({}, True)
        params = [('bgcolor', '#10AA30')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { background-color: #10AA30; }'])

    def test_style_color_bgcolor_value(self):
        style_generator = StyleGenerator({}, True)

        params_1 = [('color', '#11AA55')]
        classes, css_list = style_generator.getStyle(params_1)
        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: #11AA55; }'])

        params_2 = [('bgcolor', '#11AA55')]
        classes, css_list = style_generator.getStyle(params_2)
        self.assertEqual(classes, ['style-2'])
        self.assertEqual(css_list, ['span.style-2 { background-color: #11AA55; }'])

    def test_style_color_bgcolor_name(self):
        style_generator = StyleGenerator({}, True)

        params_1 = [('color', 'red')]
        classes, css_list = style_generator.getStyle(params_1)
        self.assertEqual(classes, ['red'])
        self.assertEqual(css_list, ['span.red { color: red; }'])

        params_2 = [('bgcolor', 'red')]
        classes, css_list = style_generator.getStyle(params_2)
        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

    def test_style_bgcolor_name_01(self):
        style_generator = StyleGenerator({}, True)
        params = [('bg-red', '')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

    def test_style_bgcolor_name_02(self):
        style_generator = StyleGenerator({}, True)
        params = [('bg_red', '')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

    def test_style_color_name_repeat_01(self):
        style_generator = StyleGenerator({}, True)
        params = [('bg-red', '')]

        classes, css_list = style_generator.getStyle(params)
        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

        name, css = style_generator.getStyle(params)
        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

    def test_style_color_name_repeat_02(self):
        style_generator = StyleGenerator({}, True)
        params = [('bg_red', '')]

        classes, css_list = style_generator.getStyle(params)
        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

        name, css = style_generator.getStyle(params)
        self.assertEqual(classes, ['bg-red'])
        self.assertEqual(css_list, ['span.bg-red { background-color: red; }'])

    def test_style_color_bgcolor_name_01(self):
        style_generator = StyleGenerator({}, True)
        params = [('red', ''), ('bg_blue', '')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: red; background-color: blue; }'])

    def test_style_color_bgcolor_name_02(self):
        style_generator = StyleGenerator({}, True)
        params = [('red', ''), ('bgcolor', '#10aa30')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: red; background-color: #10aa30; }'])

    def test_user_style__01(self):
        style_generator = StyleGenerator({}, True)
        params = [('style', 'font-weight: bold;')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { font-weight: bold; }'])

    def test_user_style_02(self):
        style_generator = StyleGenerator({}, True)
        params = [('style', 'font-weight: bold;'), ('red', '')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: red; font-weight: bold; }'])

    def test_user_style_03(self):
        style_generator = StyleGenerator({}, True)
        params = [('style', 'font-weight: bold'), ('red', '')]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: red; font-weight: bold; }'])

    def test_user_style_04(self):
        style_generator = StyleGenerator({}, True)
        params = [
            ('style', 'font-weight: bold;'),
            ('red', ''),
            ('bg-blue', '')
        ]
        classes, css_list = style_generator.getStyle(params)

        self.assertEqual(classes, ['style-1'])
        self.assertEqual(css_list, ['span.style-1 { color: red; background-color: blue; font-weight: bold; }'])
