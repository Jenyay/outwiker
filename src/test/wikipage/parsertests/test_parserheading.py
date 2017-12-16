# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserHeadingTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"

        self.pagelinks = ["Страница 1", "/Страница 1", "/Страница 2/Страница 3"]
        self.pageComments = ["Страницо 1", "Страницо 1", "Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]


    def tearDown(self):
        removeDir (self.path)


    def testHeader1 (self):
        text = "бла-бла-бла \n!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h1>Заголовок бла-бла-бла</h1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader2 (self):
        text = "бла-бла-бла \n!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок бла-бла-бла</h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader3 (self):
        text = "бла-бла-бла \n!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h3>Заголовок бла-бла-бла</h3>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader4 (self):
        text = "бла-бла-бла \n!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h4>Заголовок бла-бла-бла</h4>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader5 (self):
        text = "бла-бла-бла \n!!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h5>Заголовок бла-бла-бла</h5>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader6 (self):
        text = "бла-бла-бла \n!!!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h6>Заголовок бла-бла-бла</h6>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader7 (self):
        text = "бла-бла-бла \nкхм !! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм !! Заголовок бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader8 (self):
        text = "бла-бла-бла \nкхм !!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм !!! Заголовок бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader9 (self):
        text = "бла-бла-бла \nкхм !!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм !!!! Заголовок бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader10 (self):
        text = "бла-бла-бла \nкхм !!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм !!!!! Заголовок бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader11 (self):
        text = "бла-бла-бла \nкхм !!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм !!!!!! Заголовок бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeader12 (self):
        text = "бла-бла-бла \nкхм !!!!!!! Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \nкхм !!!!!!! Заголовок бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderItalic1 (self):
        text = "бла-бла-бла \n!! Заголовок ''бла-бла-бла''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h1>Заголовок <i>бла-бла-бла</i></h1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderItalic2 (self):
        text = "бла-бла-бла \n!!! Заголовок ''бла-бла-бла''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <i>бла-бла-бла</i></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderBold1 (self):
        text = "бла-бла-бла \n!! Заголовок '''бла-бла-бла'''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h1>Заголовок <b>бла-бла-бла</b></h1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderBold2 (self):
        text = "бла-бла-бла \n!!! Заголовок '''бла-бла-бла'''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <b>бла-бла-бла</b></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderBoldSubscript (self):
        text = "бла-бла-бла \n!!! Заголовок ''''_бла-бла-бла_''''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <b><sub>бла-бла-бла</sub></b></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderBoldSuperscript (self):
        text = "бла-бла-бла \n!!! Заголовок ''''^бла-бла-бла^''''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <b><sup>бла-бла-бла</sup></b></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderItalicSubscript (self):
        text = "бла-бла-бла \n!!! Заголовок '''_бла-бла-бла_'''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <i><sub>бла-бла-бла</sub></i></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderItalicSuperscript (self):
        text = "бла-бла-бла \n!!! Заголовок '''^бла-бла-бла^'''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <i><sup>бла-бла-бла</sup></i></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderBoldItalicSubscript (self):
        text = "бла-бла-бла \n!!! Заголовок '''''_бла-бла-бла_'''''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <b><i><sub>бла-бла-бла</sub></i></b></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderBoldItalicSuperscript (self):
        text = "бла-бла-бла \n!!! Заголовок '''''^бла-бла-бла^'''''\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <b><i><sup>бла-бла-бла</sup></i></b></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderSubscript (self):
        text = "бла-бла-бла \n!!! Заголовок '_бла-бла-бла_'\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <sub>бла-бла-бла</sub></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderSuperscript (self):
        text = "бла-бла-бла \n!!! Заголовок '^бла-бла-бла^'\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <sup>бла-бла-бла</sup></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderUnderline (self):
        text = "бла-бла-бла \n!!! Заголовок {+бла-бла-бла+}\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <u>бла-бла-бла</u></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderStrike (self):
        text = "бла-бла-бла \n!!! Заголовок {-бла-бла-бла-}\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <strike>бла-бла-бла</strike></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderNoFormat (self):
        text = "бла-бла-бла \n!!! Заголовок [={+бла-бла-бла+}=]\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок {+бла-бла-бла+}</h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderLink1 (self):
        text = "бла-бла-бла \n!!! Заголовок [[бла-бла-бла -> http://jenyay.net]]\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <a href="http://jenyay.net">бла-бла-бла</a></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderLink2 (self):
        text = "бла-бла-бла \n!!! Заголовок [[http://jenyay.net | бла-бла-бла]]\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок <a href="http://jenyay.net">бла-бла-бла</a></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderLink3 (self):
        text = "бла-бла-бла \n!!! [[Заголовок бла-бла-бла -> http://jenyay.net]]\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2><a href="http://jenyay.net">Заголовок бла-бла-бла</a></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderLink4 (self):
        text = "бла-бла-бла \n!!! [[http://jenyay.net | Заголовок бла-бла-бла]]\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2><a href="http://jenyay.net">Заголовок бла-бла-бла</a></h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderAnchor (self):
        text = "бла-бла-бла \n!!! [[#anchor]] Заголовок бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2><a id="anchor"></a> Заголовок бла-бла-бла</h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testHeaderLinebreak (self):
        text = "бла-бла-бла \n!!! Заголовок[[<<]] бла-бла-бла\nбла-бла-бла"
        result = 'бла-бла-бла \n<h2>Заголовок<br/> бла-бла-бла</h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLineJoin1 (self):
        text = """бла-бла-бла \n!!! Заголовок \\
бла-бла-бла бла-бла-бла"""
        result = 'бла-бла-бла \n<h2>Заголовок бла-бла-бла бла-бла-бла</h2>'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLineJoin2 (self):
        text = """бла-бла-бла \n!!! Заголовок \\
бла-бла-бла
бла-бла-бла"""
        result = 'бла-бла-бла \n<h2>Заголовок бла-бла-бла</h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testLineJoin3 (self):
        text = """бла-бла-бла \n!!! Заголовок \\
\\
\\
бла-бла-бла
бла-бла-бла"""
        result = 'бла-бла-бла \n<h2>Заголовок бла-бла-бла</h2>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
