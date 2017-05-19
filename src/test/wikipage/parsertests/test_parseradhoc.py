# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserAdHocTest(unittest.TestCase):
    def setUp(self):
        self.encoding = "866"

        self.filesPath = u"../test/samplefiles/"

        self.url1 = u"http://example.com"
        self.url2 = u"http://jenyay.net/Photo/Nature?action=imgtpl&G=1&upname=tsaritsyno_01.jpg"

        self.pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        self.pageComments = [u"Страницо 1", u"Страницо 1", u"Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]

    def tearDown(self):
        removeDir(self.path)

    def testBoldSubscript(self):
        text = u"бла-бла-бла '''x'_c_'''' бла-бла-бла"
        result = u'бла-бла-бла <b>x<sub>c</sub></b> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testSubscriptBold(self):
        text = u"бла-бла-бла '_'''xc'''_' бла-бла-бла"
        result = u'бла-бла-бла <sub><b>xc</b></sub> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldSuperscript(self):
        text = u"бла-бла-бла '''x'^c^'''' бла-бла-бла"
        result = u'бла-бла-бла <b>x<sup>c</sup></b> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testSuperscriptBold(self):
        text = u"бла-бла-бла '^'''xc'''^' бла-бла-бла"
        result = u'бла-бла-бла <sup><b>xc</b></sup> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testItalicSubscript(self):
        text = u"бла-бла-бла ''x'_c_''' бла-бла-бла"
        result = u'бла-бла-бла <i>x<sub>c</sub></i> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testItalicSuperscript(self):
        text = u"бла-бла-бла ''x'^c^''' бла-бла-бла"
        result = u'бла-бла-бла <i>x<sup>c</sup></i> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSubscript_01(self):
        text = u"бла-бла-бла ''''x'_c_''''' бла-бла-бла"
        result = u'бла-бла-бла <b><i>x<sub>c</sub></i></b> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSuperscript(self):
        text = u"бла-бла-бла ''''x'^c^''''' бла-бла-бла"
        result = u'бла-бла-бла <b><i>x<sup>c</sup></i></b> бла-бла-бла'
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSubscript_02(self):
        text = u"''курсив'' _'''должен быть жирный''' нормальный"
        result = u"<i>курсив</i> _<b>должен быть жирный</b> нормальный"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSubscript_03(self):
        text = u"''курсив'' _''''должен быть жирный'''' нормальный"
        result = u"<i>курсив</i> _<b><i>должен быть жирный</i></b> нормальный"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testItalicSubscript_03(self):
        text = u"'''_Бла-бла-бла_'''"
        result = u"<i><sub>Бла-бла-бла</sub></i>"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testItalicSuperscript_02(self):
        text = u"''курсив'' ^'''должен быть жирный''' нормальный"
        result = u"<i>курсив</i> ^<b>должен быть жирный</b> нормальный"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSuperscript_03(self):
        text = u"''курсив'' ^''''должен быть жирный'''' нормальный"
        result = u"<i>курсив</i> ^<b><i>должен быть жирный</i></b> нормальный"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testItalicSuperscript_03(self):
        text = u"'''^Бла-бла-бла^'''"
        result = u"<i><sup>Бла-бла-бла</sup></i>"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSuperscript_02(self):
        text = u"'''''^Бла-бла-бла^'''''"
        result = u"<b><i><sup>Бла-бла-бла</sup></i></b>"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))

    def testBoldItalicSubscript_04(self):
        text = u"'''''_Бла-бла-бла_'''''"
        result = u"<b><i><sub>Бла-бла-бла</sub></i></b>"
        self.assertEqual(self.parser.toHtml(text), result, self.parser.toHtml(text).encode(self.encoding))
