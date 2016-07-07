# -*- coding: UTF-8 -*-

import os.path
import unittest

from outwiker.core.application import Application
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import getTemplatesDir
from outwiker.core.htmlimprover import BrHtmlImprover
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.utilites.textfile import readTextFile


class HtmlTemplateTest(unittest.TestCase):
    def setUp(self):
        self.config = HtmlRenderConfig(Application.config)
        self.__clearConfig()
        self.maxDiff = None


    def tearDown(self):
        self.__clearConfig()


    def __clearConfig(self):
        Application.config.remove_section(HtmlRenderConfig.HTML_SECTION)


    def testDefault(self):
        content = u"бла-бла-бла"
        result_right = ur"""<body>
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
        content = u"бла-бла-бла"
        style = u"$userstyle $userhead $content"

        result_right = u"  бла-бла-бла"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)


    def test_text_02(self):
        content = u"бла-бла-бла"
        style = u"$userstyle $userhead $content $unknown"

        result_right = u"  бла-бла-бла $unknown"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)


    def test_text_03(self):
        content = u"бла-бла-бла"
        style = u"$userstyle $content"

        result_right = u" бла-бла-бла"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)


    def test_text_04(self):
        content = u"бла-бла-бла"
        style = u"$userstyle $content $"

        result_right = u" бла-бла-бла $"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)


    def test_text_05(self):
        content = u"бла-бла-бла"
        style = u"$userstyle $content $$"

        result_right = u" бла-бла-бла $$"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)


    def test_text_06(self):
        content = u"бла-бла-бла"
        style = u"$userstyle $content $$ $unknown"

        result_right = u" бла-бла-бла $$ $unknown"

        tpl = HtmlTemplate(style)
        result = tpl.substitute(content=content)

        self.assertEqual(result, result_right)


    def testChangeFontName(self):
        self.config.fontName.value = u"Arial"
        content = u"бла-бла-бла"

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertIn(u"font-family:Arial;", result)


    def testChangeFontSize(self):
        self.config.fontSize.value = 20
        content = u"бла-бла-бла"
        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertIn(u"font-size:20pt;", result)


    def testChangeUserStyle(self):
        style = u"p {background-color: maroon; color: white; }"

        self.config.userStyle.value = style

        content = u"бла-бла-бла"

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertTrue(style in result, result)


    def testChangeUserStyleRussian(self):
        style = (u"p {background-color: maroon; " +
                 u"/* Цвет фона под текстом параграфа */ color: white; " +
                 u"/* Цвет текста */ }")

        self.config.userStyle.value = style

        content = u"бла-бла-бла"

        templatepath = os.path.join(getTemplatesDir(),
                                    "__default",
                                    "__style.html")
        tpl = HtmlTemplate(readTextFile(templatepath).strip())
        result = tpl.substitute(content=content)

        self.assertTrue(style in result, result)


    def testImproved1(self):
        src = u"""<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>"""

        expectedResult = u"""<ul>
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
        src = ur"""<h2>Attach links</h2>Attach:file.odt<br><a href="__attach/file.odt">file.odt</a><br><a href="__attach/file.odt">alternative text</a><br><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><h2>Images</h2>"""

        expectedResult = ur"""<h2>Attach links</h2>
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
