# -*- coding: utf-8 -*-

import unittest
import os.path
import shutil
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerMixin


class StylesTest (unittest.TestCase, BaseOutWikerMixin):
    def setUp(self):
        self.initApplication()
        # Количество срабатываний особытий при обновлении страницы
        self._pageUpdateCount = 0
        self._pageUpdateSender = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.eventcount = 0

        self.wikiroot = createNotesTree(self.path)
        WikiPageFactory().create(self.wikiroot, "Викистраница 1", [])
        HtmlPageFactory().create(self.wikiroot, "Html-страница 2", [])

        self._styleFname = "__style.html"
        self._styleDir = "__style"
        self._exampleStyleDir = "testdata/styles/example_jblog/example_jblog"
        self._exampleStyleDir2 = "testdata/styles/example_jnet/example_jnet"
        self._invalidStyleDir = "../styles/invalid"
        self._testStylePath = os.path.join(
            self._exampleStyleDir, self._styleFname)

        self.application.wikiroot = self.wikiroot
        self.application.onPageUpdate += self.onPageUpdate

    def onPageUpdate(self, sender, **kwargs):
        self._pageUpdateCount += 1
        self._pageUpdateSender = sender

    def tearDown(self):
        self.application.onPageUpdate -= self.onPageUpdate
        removeDir(self.path)
        self.destroyApplication()

    def testDefault(self):
        """
        Проверка того, что возвращается правильный путь до шаблона по умолчанию
        """
        style = Style()
        defaultStyle = style.getDefaultStyle()
        self.assertEqual(os.path.abspath(defaultStyle),
                         os.path.abspath("src/outwiker/data/styles/__default/__style.html"))

    def testStylePageDefault(self):
        """
        Проверка на то, что если у страницы нет файла стиля, то возвращается стиль по умолчанию
        """
        style = Style()
        defaultStyle = style.getDefaultStyle()
        style_page1 = style.getPageStyle(self.wikiroot["Викистраница 1"])
        style_page2 = style.getPageStyle(self.wikiroot["Html-страница 2"])

        self.assertEqual(style_page1, defaultStyle)
        self.assertEqual(style_page2, defaultStyle)

    def testStylePage1(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]
        shutil.copy(self._testStylePath, page.path)

        validStyle = os.path.abspath(os.path.join(page.path, self._styleFname))
        pageStyle = os.path.abspath(style.getPageStyle(page))

        self.assertEqual(pageStyle, validStyle)

    def testStylePage2(self):
        style = Style()
        page = self.wikiroot["Html-страница 2"]
        shutil.copy(self._testStylePath, page.path)

        validStyle = os.path.abspath(os.path.join(page.path, self._styleFname))
        pageStyle = os.path.abspath(style.getPageStyle(page))

        self.assertEqual(pageStyle, validStyle)

    def testFakeStyle(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]
        os.mkdir(os.path.join(page.path, self._styleFname))

        validStyle = os.path.abspath(style.getDefaultStyle())
        pageStyle = os.path.abspath(style.getPageStyle(page))

        self.assertEqual(pageStyle, validStyle)

    def testSetStyleAsDir(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]

        pageStyleFname = os.path.join(page.path, self._styleFname)
        pageStyleDir = os.path.join(page.path, self._styleDir)

        self.assertFalse(os.path.exists(pageStyleDir))
        self.assertFalse(os.path.exists(pageStyleFname))

        style.setPageStyle(page, self._exampleStyleDir)

        self.assertTrue(os.path.exists(pageStyleDir))
        self.assertTrue(os.path.exists(pageStyleFname))

        style.setPageStyleDefault(page)

        self.assertFalse(os.path.exists(pageStyleDir))
        self.assertFalse(os.path.exists(pageStyleFname))

    def testSetStyleAsFile(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]

        pageStyleFname = os.path.join(page.path, self._styleFname)
        pageStyleDir = os.path.join(page.path, self._styleDir)

        self.assertFalse(os.path.exists(pageStyleDir))
        self.assertFalse(os.path.exists(pageStyleFname))

        style.setPageStyle(page, os.path.join(
            self._exampleStyleDir, self._styleFname))

        self.assertTrue(os.path.exists(pageStyleDir))
        self.assertTrue(os.path.exists(pageStyleFname))

        style.setPageStyleDefault(page)

        self.assertFalse(os.path.exists(pageStyleDir))
        self.assertFalse(os.path.exists(pageStyleFname))

    def testSetStyle2(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]

        pageStyleFname = os.path.join(page.path, self._styleFname)
        pageStyleDir = os.path.join(page.path, self._styleDir)

        self.assertFalse(os.path.exists(pageStyleDir))
        self.assertFalse(os.path.exists(pageStyleFname))

        style.setPageStyle(page, self._exampleStyleDir)

        self.assertTrue(os.path.exists(pageStyleDir))
        self.assertTrue(os.path.exists(pageStyleFname))

        style.setPageStyle(page, style.getDefaultStyle())

        self.assertFalse(os.path.exists(pageStyleDir))
        self.assertFalse(os.path.exists(pageStyleFname))

    def testEvent(self):
        """
        Вызов событий при изменении стиля страницы
        """
        style = Style()
        page = self.wikiroot["Викистраница 1"]

        self.assertEqual(self._pageUpdateCount, 0)

        style.setPageStyle(page, self._exampleStyleDir)
        self.assertEqual(self._pageUpdateCount, 1)

        style.setPageStyleDefault(page)
        self.assertEqual(self._pageUpdateCount, 2)

        style.setPageStyle(page, self._exampleStyleDir2)
        self.assertEqual(self._pageUpdateCount, 3)

    def testInvalidPage(self):
        style = Style()
        style.setPageStyle(None, self._exampleStyleDir)
        style.setPageStyleDefault(None)

        style.setPageStyle(self.wikiroot, self._exampleStyleDir)
        style.setPageStyleDefault(self.wikiroot)

    def testInvalidPath(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]

        self.assertRaises(IOError, style.setPageStyle,
                          page, self._invalidStyleDir)

    def testSelfDefault(self):
        style = Style()

        page = self.wikiroot["Викистраница 1"]
        style.setPageStyle(page, style.getPageStyle(page))

        self.assertEqual(os.path.abspath(style.getPageStyle(page)),
                         os.path.abspath(style.getDefaultStyle()))

    def testSelfSpecial(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]
        style.setPageStyle(page, self._exampleStyleDir)
        style.setPageStyle(page, style.getPageStyle(page))

    def testInvalidStyle1(self):
        style = Style()
        page = self.wikiroot["Викистраница 1"]

        fname = os.path.join(page.path, style._styleFname)
        with open(fname, "w") as fp:
            fp.write("""<HTML>
<HEAD>
</HEAD>

<BODY>
<P>$content</P>

$invalidkey
</BODY>
</HTML>
""")

        generator = HtmlGenerator(page, self.application)
        generator.makeHtml(Style().getPageStyle(page))
