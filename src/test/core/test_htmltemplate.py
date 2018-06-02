# -*- coding: utf-8 -*-

import os.path
from unittest import TestCase

from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import getTemplatesDir
from outwiker.core.htmlimprover import BrHtmlImprover
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.utilites.textfile import readTextFile
from test.basetestcases import BaseOutWikerMixin


class HtmlTemplateTest(BaseOutWikerMixin, TestCase):
    def setUp(self):
        self.initApplication()
        self.config = HtmlRenderConfig(self.application.config)
        self.__clearConfig()
        self.maxDiff = None

    def tearDown(self):
        self.destroyApplication()

    def __clearConfig(self):
        self.application.config.remove_section(HtmlRenderConfig.HTML_SECTION)

    def testDefault(self):
        content = "бла-бла-бла"
        result_right = r"""<body>
бла-бла-бла
</body>
</html>"""

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertIn(result_right, result.replace("\r\n", "\n"))

    def test_text_01(self):
        content = "бла-бла-бла"
        style = "$userstyle $userhead $content"

        result_right = "  бла-бла-бла"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_02(self):
        content = "бла-бла-бла"
        style = "$userstyle $userhead $content $unknown"

        result_right = "  бла-бла-бла $unknown"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_03(self):
        content = "бла-бла-бла"
        style = "$userstyle $content"

        result_right = " бла-бла-бла"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_04(self):
        content = "бла-бла-бла"
        style = "$userstyle $content $"

        result_right = " бла-бла-бла $"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_05(self):
        content = "бла-бла-бла"
        style = "$userstyle $content $$"

        result_right = " бла-бла-бла $$"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_06(self):
        content = "бла-бла-бла"
        style = "$userstyle $content $$ $unknown"

        result_right = " бла-бла-бла $$ $unknown"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_07(self):
        content = "бла-бла-бла"
        style = "$content $title"

        result_right = "бла-бла-бла "

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)

    def test_text_08(self):
        content = "бла-бла-бла"
        style = "$content $title"

        result_right = "бла-бла-бла Заголовок"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content, title='Заголовок')

        self.assertEqual(result, result_right)

    def testChangeFontName(self):
        self.config.fontName.value = "Arial"
        content = "бла-бла-бла"

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertIn("font-family:Arial;", result)

    def testChangeFontSize(self):
        self.config.fontSize.value = 20
        content = "бла-бла-бла"
        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertIn("font-size:20pt;", result)

    def testChangeUserStyle(self):
        style = "p {background-color: maroon; color: white; }"

        self.config.userStyle.value = style

        content = "бла-бла-бла"

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertTrue(style in result, result)

    def testChangeUserStyleRussian(self):
        style = ("p {background-color: maroon; " +
                 "/* Цвет фона под текстом параграфа */ color: white; " +
                 "/* Цвет текста */ }")

        self.config.userStyle.value = style

        content = "бла-бла-бла"

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertTrue(style in result, result)

    def testImproved1(self):
        src = """<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>"""

        expectedResult = """<ul>
<li>Несортированный список. Элемент 1</li>
<li>Несортированный список. Элемент 2</li>
<li>Несортированный список. Элемент 3</li>
<ol>
<li>Вложенный сортированный список. Элемент 1</li>
<li>Вложенный сортированный список. Элемент 2</li>
<li>Вложенный сортированный список. Элемент 3</li>
<li>Вложенный сортированный список. Элемент 4</li>
<ul>
<li>Совсем вложенный сортированный список. Элемент 1</li>
<li>Совсем вложенный сортированный список. Элемент 2</li>
</ul>
<li>Вложенный сортированный список. Элемент 5</li>
</ol>
<ul>
<li>Вложенный несортированный список. Элемент 1</li>
</ul>
</ul>"""

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())

        result = tpl.substitute(BrHtmlImprover().run(src))
        self.assertIn(expectedResult, result)

    def testImproved2(self):
        src = r"""<h2>Attach links</h2>Attach:file.odt<br><a href="__attach/file.odt">file.odt</a><br><a href="__attach/file.odt">alternative text</a><br><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><h2>Images</h2>"""

        expectedResult = r"""<h2>Attach links</h2>
Attach:file.odt<br>
<a href="__attach/file.odt">file.odt</a><br>
<a href="__attach/file.odt">alternative text</a><br>
<a href="__attach/file with spaces.pdf">file with spaces.pdf</a>
<h2>Images</h2>"""

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())

        result = tpl.substitute(BrHtmlImprover().run(src))
        self.assertIn(expectedResult, result)
