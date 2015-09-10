# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory


class ParserFontTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"

        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        removeDir (self.path)


    def testBold (self):
        text = u"'''Полужирный'''"
        result = u"<b>Полужирный</b>"

        self.assertEqual (self.parser.toHtml (text), result)


    def testItalic (self):
        text = u"''Курсив''"
        result = u"<i>Курсив</i>"

        self.assertEqual (self.parser.toHtml (text), result)


    def testBoldItalic (self):
        text = u"''''Полужирный курсив''''"
        result = u"<b><i>Полужирный курсив</i></b>"

        self.assertEqual (self.parser.toHtml (text), result)


    def testComboBoldItalic (self):
        text = u"Обычный текст \n''курсив'' \n'''полужирный ''внутри \nкурсив'' ''' 111"
        result = u"Обычный текст \n<i>курсив</i> \n<b>полужирный <i>внутри \nкурсив</i> </b> 111"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUnderline (self):
        text = u'бла-бла-бла \nкхм {+ это подчеркивание+} %% бла-бла-бла\nбла-бла-бла'
        result = u'бла-бла-бла \nкхм <u> это подчеркивание</u> %% бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testStrike (self):
        text = u'бла-бла-бла \nкхм {-это зачеркнутый текст-} %% бла-бла-бла\nбла-бла-бла'
        result = u'бла-бла-бла \nкхм <strike>это зачеркнутый текст</strike> %% бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testStrikeUnderline (self):
        text = u'бла-бла-бла \nкхм {-{+это зачеркнутый подчеркнутый текст+}-} %% бла-бла-бла\nбла-бла-бла'
        result = u'бла-бла-бла \nкхм <strike><u>это зачеркнутый подчеркнутый текст</u></strike> %% бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSuperscript (self):
        text = u"бла-бла-бла \nкхм '^ это верхний индекс^' бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <sup> это верхний индекс</sup> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSubscript (self):
        text = u"бла-бла-бла \nкхм '_ это нижний индекс_' бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <sub> это нижний индекс</sub> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall1 (self):
        text = u"бла-бла-бла \nкхм [-мелкий шрифт-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:80%">мелкий шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall2 (self):
        text = u"бла-бла-бла \nкхм [--мелкий шрифт--] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:60%">мелкий шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall3 (self):
        text = u"бла-бла-бла \nкхм [---мелкий шрифт---] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:40%">мелкий шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall4 (self):
        text = u"бла-бла-бла \nкхм [----мелкий шрифт----] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:20%">мелкий шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall5 (self):
        text = u"бла-бла-бла \nкхм [-----мелкий шрифт-----] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:20%">-мелкий шрифт-</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall6 (self):
        text = u"бла-бла-бла \nкхм [--мелкий шрифт-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:80%">-мелкий шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmallLink (self):
        text = u"бла-бла-бла \nкхм [-[[мелкий шрифт -> http://jenyay.net]]-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:80%"><a href="http://jenyay.net">мелкий шрифт</a></span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmallHeading (self):
        text = u"бла-бла-бла \n!! Кхм [-мелкий шрифт-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<h1>Кхм <span style="font-size:80%">мелкий шрифт</span> бла-бла-бла</h1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig1 (self):
        text = u"бла-бла-бла \nкхм [+ крупный шрифт+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:120%"> крупный шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig2 (self):
        text = u"бла-бла-бла \nкхм [++крупный шрифт++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:140%">крупный шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig3 (self):
        text = u"бла-бла-бла \nкхм [+++крупный шрифт+++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:160%">крупный шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig4 (self):
        text = u"бла-бла-бла \nкхм [++++крупный шрифт++++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:180%">крупный шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig5 (self):
        text = u"бла-бла-бла \nкхм [+++++крупный шрифт+++++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:200%">крупный шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig6 (self):
        text = u"бла-бла-бла \nкхм [++++++крупный шрифт++++++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:200%">+крупный шрифт+</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig7 (self):
        text = u"бла-бла-бла \nкхм [++крупный шрифт+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:120%">+крупный шрифт</span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBigLink (self):
        text = u"бла-бла-бла \nкхм [+[[крупный шрифт -> http://jenyay.net]]+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <span style="font-size:120%"><a href="http://jenyay.net">крупный шрифт</a></span> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBigHeading (self):
        text = u"бла-бла-бла \n!! Кхм [+крупный шрифт+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<h1>Кхм <span style="font-size:120%">крупный шрифт</span> бла-бла-бла</h1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
