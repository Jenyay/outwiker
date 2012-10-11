#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import unittest
import hashlib

from test.utils import removeWiki

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application

from outwiker.pages.wiki.parser.wikiparser import Parser
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
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        self.testPage = self.rootwiki[u"Страница 2"]
        

    def tearDown(self):
        removeWiki (self.path)


    def testBold (self):
        text = u"'''Полужирный'''"
        result = u"<B>Полужирный</B>"

        self.assertEqual (self.parser.toHtml (text), result)


    def testItalic (self):
        text = u"''Курсив''"
        result = u"<I>Курсив</I>"

        self.assertEqual (self.parser.toHtml (text), result)

    
    def testBoldItalic (self):
        text = u"''''Полужирный курсив''''"
        result = u"<B><I>Полужирный курсив</I></B>"

        self.assertEqual (self.parser.toHtml (text), result)
    

    def testComboBoldItalic (self):
        text = u"Обычный текст \n''курсив'' \n'''полужирный ''внутри \nкурсив'' ''' 111"
        result = u"Обычный текст \n<I>курсив</I> \n<B>полужирный <I>внутри \nкурсив</I> </B> 111"

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testUnderline (self):
        text = u'бла-бла-бла \nкхм {+ это подчеркивание+} %% бла-бла-бла\nбла-бла-бла'
        result = u'бла-бла-бла \nкхм <U> это подчеркивание</U> %% бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testStrike (self):
        text = u'бла-бла-бла \nкхм {-это зачеркнутый текст-} %% бла-бла-бла\nбла-бла-бла'
        result = u'бла-бла-бла \nкхм <STRIKE>это зачеркнутый текст</STRIKE> %% бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testStrikeUnderline (self):
        text = u'бла-бла-бла \nкхм {-{+это зачеркнутый подчеркнутый текст+}-} %% бла-бла-бла\nбла-бла-бла'
        result = u'бла-бла-бла \nкхм <STRIKE><U>это зачеркнутый подчеркнутый текст</U></STRIKE> %% бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
    

    def testSuperscript (self):
        text = u"бла-бла-бла \nкхм '^ это верхний индекс^' бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SUP> это верхний индекс</SUP> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

    
    def testSubscript (self):
        text = u"бла-бла-бла \nкхм '_ это нижний индекс_' бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SUB> это нижний индекс</SUB> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall1 (self):
        text = u"бла-бла-бла \nкхм [-мелкий шрифт-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:80%">мелкий шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall2 (self):
        text = u"бла-бла-бла \nкхм [--мелкий шрифт--] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:60%">мелкий шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall3 (self):
        text = u"бла-бла-бла \nкхм [---мелкий шрифт---] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:40%">мелкий шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall4 (self):
        text = u"бла-бла-бла \nкхм [----мелкий шрифт----] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:20%">мелкий шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall5 (self):
        text = u"бла-бла-бла \nкхм [-----мелкий шрифт-----] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:20%">-мелкий шрифт-</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmall6 (self):
        text = u"бла-бла-бла \nкхм [--мелкий шрифт-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:80%">-мелкий шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmallLink (self):
        text = u"бла-бла-бла \nкхм [-[[мелкий шрифт -> http://jenyay.net]]-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:80%"><A HREF="http://jenyay.net">мелкий шрифт</A></SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testSmallHeading (self):
        text = u"бла-бла-бла \n!! Кхм [-мелкий шрифт-] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<H1>Кхм <SPAN STYLE="font-size:80%">мелкий шрифт</SPAN> бла-бла-бла</H1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig1 (self):
        text = u"бла-бла-бла \nкхм [+ крупный шрифт+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:120%"> крупный шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig2 (self):
        text = u"бла-бла-бла \nкхм [++крупный шрифт++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:140%">крупный шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig3 (self):
        text = u"бла-бла-бла \nкхм [+++крупный шрифт+++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:160%">крупный шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig4 (self):
        text = u"бла-бла-бла \nкхм [++++крупный шрифт++++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:180%">крупный шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig5 (self):
        text = u"бла-бла-бла \nкхм [+++++крупный шрифт+++++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:200%">крупный шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig6 (self):
        text = u"бла-бла-бла \nкхм [++++++крупный шрифт++++++] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:200%">+крупный шрифт+</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBig7 (self):
        text = u"бла-бла-бла \nкхм [++крупный шрифт+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:120%">+крупный шрифт</SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBigLink (self):
        text = u"бла-бла-бла \nкхм [+[[крупный шрифт -> http://jenyay.net]]+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \nкхм <SPAN STYLE="font-size:120%"><A HREF="http://jenyay.net">крупный шрифт</A></SPAN> бла-бла-бла\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))


    def testBigHeading (self):
        text = u"бла-бла-бла \n!! Кхм [+крупный шрифт+] бла-бла-бла\nбла-бла-бла"
        result = u'бла-бла-бла \n<H1>Кхм <SPAN STYLE="font-size:120%">крупный шрифт</SPAN> бла-бла-бла</H1>\nбла-бла-бла'

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))
